# Philippine PFM Atlas

A set of diagrams and descriptions that map public financial management (PFM) of the Philippine national government: the process, the authorities that participate in it, and their information systems. Facts on current events are as of 8 October 2026.

The atlas is based mainly on five texts that were read in full as files: the three volumes of the Government Accounting Manual, the Government Auditing Code, and the Implementing Rules of the procurement law. Book VI of the Administrative Code, the release rules of the budget, the issuances of the GPPB after the Implementing Rules and many other sources were read through a tool that returns a summary with short quotations. [Reference F](reference/F_sources_and_verification.md) lists every source and the way it was read, and in section 5 the decisions that shape the atlas.

This atlas is not an official publication of the Philippine government. It does not replace the laws, circulars and manuals that it cites.

## 1. Where to start

1. Read [00_BIG_PICTURE.md](00_BIG_PICTURE.md). It gives the whole on a few pages and contains the eight overview diagrams.
2. Open the chapter of the phase or the step that you need (section 4 below). The chapters follow the budget cycle in the illustration of DBM: four phases with 32 steps. Each phase has a chapter that describes it as a whole, and each step has a chapter of its own.
3. Use the reference files for the authorities, the information systems, the documents, the laws, the terms, the sources, and the open questions (section 5).
4. Before a diagram is reused for another purpose, read section 5.1 of the big picture. It names the nine kinds of arrows of this atlas and, for each kind, an observation that would show an arrow to be wrong.
5. To see what is not settled, read [Reference G](reference/G_open_questions_and_known_gaps.md): 18 differences between sources and 68 facts that I could not verify, each with a number.

## 2. What the atlas contains

| Folder or file | Content | Number of files |
|---|---|---|
| `00_BIG_PICTURE.md` | The big picture | 1 |
| `README.md` | This file | 1 |
| `chapters/` | One chapter for each phase and for each step of the budget cycle, and two chapters on the information systems and on UACS | 38 |
| `reference/` | Reference files A to G in Markdown | 7 |
| `reference/` | Three tables in CSV form, for use by a program (section 9) | 3 |
| `diagrams/mermaid/` | Diagram code in Mermaid (`.mmd`) | 77 |
| `diagrams/plantuml/` | Diagram code in PlantUML (`.puml`) | 8 |
| `rendered/` | A PNG image of every diagram | 85 |

In the repository these files are in the folder `docs/atlas/`. They are built from the sources in the folder `src/` by the script `tools/build_atlas.py`, and the website of the atlas is built from them (section 10, and the README of the repository).

## 3. All diagrams

The part of an ID before the hyphen names the chapter that shows the diagram. BP is the big picture.

{{index:diagrams}}

## 4. The chapters

| File | Subject | Diagrams |
|---|---|---|
| [chapters/P0_preparation.md](chapters/P0_preparation.md) | The phase as a whole: the Budget Call, the proposals in two tiers and the budget of the President. Authorities, steps, systems, controls and calendar | P0-a to P0-c |
| [chapters/P1_budget_call.md](chapters/P1_budget_call.md) | The Budget Call, and what sets its frame: the development plan and the investment program, the DBCC and the fiscal program, fiscal risks, partnerships with private firms and promises under conditions | P1-a to P1-e |
| [chapters/P2_citizen_engagement_in_preparation.md](chapters/P2_citizen_engagement_in_preparation.md) | BP Form D: the inputs of civil society organizations | None |
| [chapters/P3_rdc_consultations.md](chapters/P3_rdc_consultations.md) | BP Form C: the inputs of the Regional Development Councils | None |
| [chapters/P4_program_convergence.md](chapters/P4_program_convergence.md) | BP Form 206: programs that several agencies implement jointly | None |
| [chapters/P5_tier_1_proposals.md](chapters/P5_tier_1_proposals.md) | The forms of the proposal, and Tier 1: the cost of ongoing programs | None |
| [chapters/P6_tier_1_deliberations.md](chapters/P6_tier_1_deliberations.md) | The technical budget hearings | None |
| [chapters/P7_budget_priorities_framework.md](chapters/P7_budget_priorities_framework.md) | The framework of the budget priorities | None |
| [chapters/P8_tier_2_proposals.md](chapters/P8_tier_2_proposals.md) | Tier 2: new or expanded programs and projects, and the approvals that a project needs | None |
| [chapters/P9_tier_2_deliberations.md](chapters/P9_tier_2_deliberations.md) | The evaluation and the executive review of the Tier 2 proposals | None |
| [chapters/P10_presentation_to_the_president.md](chapters/P10_presentation_to_the_president.md) | The proposed budget levels before the DBCC, the President and the Cabinet | None |
| [chapters/P11_confirmation_and_finalization.md](chapters/P11_confirmation_and_finalization.md) | The approval of the budget, and the preparation of the budget documents | None |
| [chapters/P12_presidents_budget.md](chapters/P12_presidents_budget.md) | The documents that go to Congress | P12-a |
| [chapters/L0_legislation.md](chapters/L0_legislation.md) | The phase as a whole: Congress, the veto, reenactment, and what Congress and the President may change | L0-a, L0-b |
| [chapters/L1_house_deliberations.md](chapters/L1_house_deliberations.md) | The House: hearings, committee report, plenary and three readings | None |
| [chapters/L2_senate_deliberations.md](chapters/L2_senate_deliberations.md) | The Senate: hearings, committee report and plenary | None |
| [chapters/L3_bicameral_deliberations.md](chapters/L3_bicameral_deliberations.md) | The bicameral conference committee | None |
| [chapters/L4_ratification_and_enrolment.md](chapters/L4_ratification_and_enrolment.md) | Ratification by both chambers, and the enrolled bill | None |
| [chapters/L5_enactment_of_the_gaa.md](chapters/L5_enactment_of_the_gaa.md) | The signature and the item veto, and the kinds of appropriation that the law contains | L5-a |
| [chapters/E0_execution.md](chapters/E0_execution.md) | The phase as a whole: the two authorities, allotment and cash authority, the law behind them, the steps of release, the states of one budget line | E0-a, E0-b |
| [chapters/E1_early_procurement.md](chapters/E1_early_procurement.md) | Procurement under Republic Act No. 12009 and the guidelines of the GPPB to August 2026: the procurement plans, early procurement, competitive bidding, the eleven modes, contracts for more than one year, framework agreements, the election period of 2026 | E1-a to E1-g |
| [chapters/E2_budget_execution_program.md](chapters/E2_budget_execution_program.md) | The budget execution documents: financial plan, physical plan and monthly disbursement program | None |
| [chapters/E3_allotment_release.md](chapters/E3_allotment_release.md) | Which release document applies, and changes during the year. Local governments: their budget cycle, their money, the limits of national law, and their contacts with the national system | E3-a to E3-h |
| [chapters/E4_obligation.md](chapters/E4_obligation.md) | The obligation and the claim: who certifies what, from the obligation request to the voucher. Salaries and the payroll | E4-a to E4-e |
| [chapters/E5_cash_allocation.md](chapters/E5_cash_allocation.md) | The kinds of cash authority. The Treasury Single Account, cash programming, borrowing and debt. Revenue, collections and refunds | E5-a to E5-i |
| [chapters/E6_disbursement.md](chapters/E6_disbursement.md) | Payment through the bank, the kinds of claim, advance payment and retention, cash advances, what happens when a step fails. Other routes of public money: government corporations, transfers, disaster funds, cash aid, fund clusters | E6-a to E6-l |
| [chapters/A0_accountability.md](chapters/A0_accountability.md) | The phase as a whole: the layers of control around one agency, four examinations, five measures of the same spending | A0-a to A0-c |
| [chapters/A1_performance_targets.md](chapters/A1_performance_targets.md) | Performance information: targets, plans and reports, and their path through one year | A1-a |
| [chapters/A2_citizen_engagement_in_accountability.md](chapters/A2_citizen_engagement_in_accountability.md) | The public portal of budget and performance information | None |
| [chapters/A3_monitoring_and_evaluation.md](chapters/A3_monitoring_and_evaluation.md) | The evaluation of programs | None |
| [chapters/A4_accountability_reports.md](chapters/A4_accountability_reports.md) | Records and reports of agencies: registries, books of accounts, reports, closing of a period. Assets and property | A4-a to A4-d |
| [chapters/A5_performance_review.md](chapters/A5_performance_review.md) | The yearly review of performance, and the bonus of the personnel | None |
| [chapters/A6_in_year_reports.md](chapters/A6_in_year_reports.md) | From the reports of each body to national totals | A6-a |
| [chapters/A7_dbcc_mid_year_report.md](chapters/A7_dbcc_mid_year_report.md) | The mid-year report of the DBCC | None |
| [chapters/A8_dbcc_year_end_report.md](chapters/A8_dbcc_year_end_report.md) | The year-end report of the DBCC | None |
| [chapters/A9_audit_report.md](chapters/A9_audit_report.md) | External audit by COA: steps, findings, notices, and the use of the reports by Congress | A9-a, A9-b |
| [chapters/IS_information_systems.md](chapters/IS_information_systems.md) | Systems, data flows, BTMS, the planned IFMIS, the COMPASS portal | IS-a to IS-g |
| [chapters/UACS_uacs_and_record_identifiers.md](chapters/UACS_uacs_and_record_identifiers.md) | UACS and the numbers that connect records | UACS-a to UACS-d |

Each chapter of a step starts with a table that places the step in the budget cycle: its phase, its timing in the illustration of DBM, its documents, its place on the four lines, the steps from which it receives documents and to which it passes them, and where to read more. A chapter that describes a whole process, for example a phase, has the same parts as the descriptions of processes inside the longer chapters of the steps: the question it answers, the idea in plain words with one case where the process works and one where it fails, the authorities and their roles, the steps, the documents and identifiers, the information systems, the controls (what each one checks and what it does not check), the timing, the reported weaknesses, the diagrams, and the verification status.

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

**Arrows.** In diagrams that show exchanges: a thin solid arrow is a decision or a document, a thick arrow is money, a dotted arrow is information. In the two component diagrams of chapter IS, a solid black arrow means that a source describes an electronic channel, and a dashed grey arrow means paper, an entry by staff in a record of their own body, or a carrier that the sources do not state. The label of each arrow says which. In diagram UACS-b the colour of an arrow says whether a field of a form holds the number that links two records. Section 5.1 of the big picture lists all kinds of arrows.

**Numbers in sequence diagrams.** The steps are numbered by Mermaid. The tables of steps in the chapters use the same numbers.

**One technical mark in sequence diagrams.** A step that an actor performs alone (a message from an actor to itself) ends with a line that contains only `#nbsp;`. This code means a non-breaking space, which is a space character that the program does not delete. The empty line moves the text away from the step number in the picture. It has no other meaning.

**Why some diagrams are in PlantUML.** Mermaid is the main notation. Eight diagrams are in PlantUML because Mermaid cannot draw them well: six lane diagrams with parallel bars or decision points (BP-e, P0-b, E1-d, E4-b, E3-f, P1-e), and two component diagrams that place systems inside frames of their owner institutions (IS-b, IS-c).

## 8. How to render the diagrams

The images in `rendered/` were made with Mermaid 11.16 (through the command-line tool `mmdc`, version 11.16.0) and PlantUML 1.2026.8. Afterwards each image was reduced to 256 colours, which makes the files smaller and does not change what is shown.

In the repository the script `tools/render_diagrams.py` draws the images from the code files in `src/diagrams/` and reduces their colours. Its first lines say which programs it needs. One diagram can also be drawn by hand:

```
# Mermaid: needs Node.js and the package @mermaid-js/mermaid-cli
mmdc -i diagrams/mermaid/E4-a_obligation_to_payment_sequence.mmd -o E4-a.png -b white -s 2 -w 2000

# PlantUML: needs Java and plantuml.jar. The two component diagrams also need Graphviz
java -DPLANTUML_LIMIT_SIZE=16384 -jar plantuml.jar -tpng diagrams/plantuml/E4-b_obligation_to_payment_swimlane.puml
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
