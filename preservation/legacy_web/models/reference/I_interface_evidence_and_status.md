# Reference I — IFMIS and interface evidence protocol

## 1. The minimum assertion

Do not write `A → B (API)` merely because both applications are mentioned in an integration roadmap. An assertion about integration must state **source and destination application**, **specific owner and deployment context**, **type of payload**, **transmission mechanism**, **operational status**, **date**, and **evidence level**.

The original [interface register](interface_register.csv) is preserved verbatim. The [interface evidence register](interface_evidence_register.csv) re-expresses each legacy row as a *claim requiring validation*; its blank mechanism, deployment and protocol fields are intentional, not signs of failure. It does **not** assert that blank fields mean an interface is absent.

## 2. Orthogonal evidence axes

| Dimension | Controlled vocabulary | Meaning |
|---|---|---|
| Deployment | `production_confirmed`, `pilot_reported`, `planned`, `retired`, `unknown` | Whether operational rollout has been proved for the specified agency/scope |
| Mechanism | `api`, `batch`, `file_import`, `web_portal`, `manual_reentry`, `paper`, `bank_network`, `unknown` | How a record moves |
| Evidence | `primary_operational`, `official_policy`, `official_announcement`, `secondary_report`, `atlas_inference`, `unverified` | Why the model makes a claim |
| Authoritative data | `source_record`, `copy`, `transform`, `unknown` | Which is the record of authority |
| Reconciliation | `automated`, `manual`, `none_verified`, `unknown` | How cross-system equality is checked |

An agency can be in a BTMS rollout without every companion system operating an API. Official [DBM FY 2026 statement](https://www.dbm.gov.ph/index.php/the-secretary-2/speeches/3800-the-2026-people-s-budget-a-catalyst-for-a-future-ready-philippine-economy) says BTMS piloted in seven agencies in 2025, intended expansion to 155 in 2026. The [midterm roadmap](https://www.dbm.gov.ph/wp-content/uploads/DBM%20Publications/PFM-Reforms/Midterm-Update/PHIL%20PFM%20Roadmap%20Midterm%20Update%20v2.pdf) schedules longer implementation of integration, migration and UACS revision. These official statements are evidence of **program rollout/plan**, not successful agency-by-agency data exchange.

## 3. Proof hierarchy and negative claims

- A **current production log, agency acceptance record, bank confirmation, or system transaction record** with a specified scope proves an operational interface for that scope and date.
- A **current approved system manual or integration specification** supports a design; it may not prove operation.
- An **official roadmap** proves an intention or implementation work plan; it does not prove completed deployment.
- Two systems named in a common diagram do not prove an electronic interface. A reusable classification code does not prove shared database keys.
- An absent public source is not proof that an exchange is impossible. Mark `unknown` unless there is explicit verified negative evidence.

## 4. Interface failure contract

Every confirmed or proposed interface needs identifier translation, immutable source references, idempotency/duplicate detection, cutoff and retry policy, reconciliation ownership, exception queue, and data dictionary versioning. Treat these as recommended technical requirements unless an actual legal or technical document mandates them.

**Diagrams:** [16h](../diagrams/mermaid/16h_ifmis_deployment_confidence.mmd), [16i](../diagrams/mermaid/16i_interface_failure_and_reconciliation.mmd), [16j](../diagrams/plantuml/16j_system_of_record_vs_interfaces.puml).
