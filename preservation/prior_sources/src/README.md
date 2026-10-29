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

{{index:diagrams}}

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
