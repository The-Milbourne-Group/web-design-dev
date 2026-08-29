# SYSTEM MAP

**System:** Governance
**Purpose:** Show how the operating system fits together — architecture, authority, knowledge domains, and the core business flows.
**Authority:** Tier 3. Authoritative for repository architecture.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme)
**Applies to:** Anyone orienting in this repository.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Structural change; document added or retired.
**Related:** `CLAUDE.md`, `governance/AUTHORITY.md`, `governance/DOCUMENT_REGISTRY.md`

---

## 1. Repository Architecture

```
/
├── MASTER.md                    ULTIMATE AUTHORITY — how the company operates
├── CLAUDE.md                    AI entry point and context-loading protocol
├── README.md                    Human entry point
├── SYSTEM_MAP.md                This file
│
├── STRATEGIC_CONFIGURATION.md   Founder-approved strategy (Tier 2)
├── EXECUTIVE_SUMMARY.md         One-page brief (no authority)
│
├── DECISIONS.md                 Decision register (Confirmed = Tier 2)
├── OPEN_QUESTIONS.md            What is NOT known — check before inventing
├── ASSUMPTIONS.md               Unconfirmed premises in use
├── RISKS.md                     Company and system risk
├── GLOSSARY.md                  Terminology
├── SOP_INDEX.md                 SOP catalogue and structure standard
│
├── BUSINESS.md                  Business model, market, pricing principles
├── BRAND.md                     Voice, messaging, claims standard
├── SERVICES.md                  Offers and scope discipline
├── ICP.md                       Target clients and qualification criteria
├── MARKETING.md                 Demand generation
├── SALES.md                     Sales process
├── DELIVERY.md                  Delivery lifecycle (sole definition)
├── WEB_STANDARDS.md             Web product craft standards
├── TECH_STACK.md                Technology selection and governance
├── AUTOMATION.md                Automation and autonomy levels
├── SECURITY.md                  Security governance
├── METRICS.md                   Metric definitions
├── ROADMAP.md                   Capability sequencing
│
├── governance/
│   ├── AUTHORITY.md             Precedence, scope, decision rights
│   ├── CHANGE_MANAGEMENT.md     How knowledge changes
│   ├── DOCUMENT_REGISTRY.md     Subject ownership and dependencies
│   ├── KNOWLEDGE_ARCHITECTURE.md Knowledge classes and placement
│   └── SYSTEM_QA.md             Consistency checks
│
├── sops/                        Procedures (Tier 4)
├── agents/                      AI role definitions (Tier 5)
├── templates/                   Reusable starting points (Tier 6)
├── clients/                     Client and opportunity knowledge (Tier 7), isolated
└── exports/                     Generated artifacts — no authority
```

## 2. Authority Flow

```
                        ┌──────────────────────────┐
                        │       MASTER.md          │
                        │   ULTIMATE AUTHORITY     │
                        │  imposes §7 absolute     │
                        │  constraints on all      │
                        └────────────┬─────────────┘
                    delegates        │        delegates
              strategic identity     │     domain substance
                        ┌────────────┴────────────┐
                        ▼                         ▼
          ┌─────────────────────────┐   ┌──────────────────────┐
          │ STRATEGIC_CONFIGURATION │   │  DOMAIN SOURCES OF   │
          │ DECISIONS (Confirmed)   │──►│  TRUTH  (Tier 3)     │
          │        Tier 2           │   └──────────┬───────────┘
          └─────────────────────────┘              │
                                                   ▼
                                        ┌──────────────────────┐
                                        │   SOPs   (Tier 4)    │
                                        └──────────┬───────────┘
                                                   ▼
                                        ┌──────────────────────┐
                                        │  AGENTS  (Tier 5)    │
                                        └──────────┬───────────┘
                                                   ▼
                                        ┌──────────────────────┐
                                        │ TEMPLATES (Tier 6)   │
                                        └──────────┬───────────┘
                                                   ▼
                                        ┌──────────────────────┐
                                        │  PROJECTS (Tier 7)   │
                                        │     EXECUTION        │
                                        └──────────┬───────────┘
                                                   │ evidence
                                                   ▼
                                        CHANGE_MANAGEMENT.md
                                        proposes change upward
```

Full rules: `governance/AUTHORITY.md`.

## 3. The Commercial Flow

The trace from strategy to expansion, with the governing document at each step.

| Step | Governed by | Procedure | Produces |
|---|---|---|---|
| Business strategy | `STRATEGIC_CONFIGURATION.md`, `BUSINESS.md` | — | Confirmed positioning |
| Positioning | `STRATEGIC_CONFIGURATION.md`, `BRAND.md` | — | Messaging platform |
| ICP | `ICP.md` | — | Fit criteria |
| Services | `SERVICES.md` | — | Offer set |
| Marketing | `MARKETING.md` | — | Qualified demand |
| Qualification | `ICP.md`, `SALES.md` | `sops/sales/QUALIFICATION.md` | Qualified / nurture / disqualified |
| Discovery | `SALES.md` §4 | `sops/sales/DISCOVERY.md` | Discovery notes, confirmed understanding |
| Solution | `SALES.md` §5, `SERVICES.md` | `sops/sales/SOLUTION_DESIGN.md` | Requirement traceability matrix, minimum viable scope |
| Proposal | `SALES.md` §6–§7 | `sops/sales/PROPOSAL.md` | Founder-issued proposal, filed with its outcome |
| Agreement | Founder only | — | Executed agreement |
| Onboarding | `DELIVERY.md` §3 | `sops/delivery/ONBOARDING.md` | Client workspace, project brief |
| Delivery | `DELIVERY.md` §2 | `sops/delivery/` | Built deliverable |
| QA | `WEB_STANDARDS.md` | `sops/delivery/QA.md` | Verification record |
| Launch | `DELIVERY.md` §8 | `sops/delivery/LAUNCH.md` | Live, verified deliverable |
| Measurement | `METRICS.md` | `sops/delivery/CLOSURE.md` | Baseline, delivery metrics |
| Optimization | `MARKETING.md`, `WEB_STANDARDS.md` | — | Improvements |
| Closure | `DELIVERY.md` §9 | `sops/delivery/CLOSURE.md` | Acceptance, handover, retrospective, buyer evidence |
| Expansion | `SERVICES.md` §2.2–2.3 | `sops/delivery/CLOSURE.md` §5.11 → qualification | Next engagement |

**Scope changes** at any delivery step route through
`sops/delivery/SCOPE_CHANGE.md`.

## 4. Information Flow

```
Founder decision ──► DECISIONS.md ──► domain documents ──► SOPs ──► execution
                          ▲                                            │
                          │                                            │
                     approval                                     evidence
                          │                                            ▼
                  DECISION_BRIEF ◄──── OPEN_QUESTIONS / ASSUMPTIONS / RISKS
```

Nothing becomes a company fact without passing through founder approval and
`DECISIONS.md` (`governance/CHANGE_MANAGEMENT.md` §5).

## 5. Agent Relationships

```
                        CEO / Orchestrator
                     (prioritizes, routes, escalates)
                                 │
        ┌────────────┬───────────┼───────────┬────────────┐
        ▼            ▼           ▼           ▼            ▼
    Strategy      Sales        SEO       Design         Dev
   (analysis)   (drafts)   (discovery)  (specifies)  (implements)
        │            │           │           │            │
        └────────────┴───────────┴─────┬─────┴────────────┘
                                       ▼
                                      QA
                              (verifies, reports)
                                       │
                                       ▼
                                   FOUNDER
                          (decides, approves, accepts)

                  Automation ── spans all: maps, automates, monitors
```

Every arrow terminates at the founder for anything reserved under
`governance/AUTHORITY.md` §7. Routing and overlap resolution:
`agents/README.md`.

## 6. Client Lifecycle

```
Prospect → Qualified → Discovery → Proposal → Agreement
    │                                                        │
    └── clients/<client>/ created HERE                       ▼
        (at qualification, not onboarding)   Onboarding → Delivery → QA → Launch
                                                                          │
                                                            Closure ──────┘
                                                               │
                                    acceptance · handover · measurement
                                    access revocation · retrospective
                                    buyer evidence · expansion review
                                                               │
                                                               ▼
                                                    Expansion / Recurring
```

The directory is created at **qualification** so that qualification records,
discovery notes, and solution traceability have a home before an agreement
exists. It is retained after closure — including for disqualified
opportunities, whose reasoning is the evidence base for Q-001 and Q-003.

The `Status` vocabulary itself is owned by `clients/README.md` — this diagram
shows the flow, not the permitted values.

Client knowledge lives in `clients/<client>/` for the entire lifecycle and
never leaves it (`MASTER.md` §7.1).

## 7. What Changed in the 2026-08-29 Audit

| Before | After |
|---|---|
| Four competing precedence statements | One — `MASTER.md`, detailed in `governance/AUTHORITY.md` |
| `MASTER.md` §1.1 vs §5.1 self-contradiction | `MASTER.md` supreme, stated consistently |
| `MASTER.md` 1,529 lines holding domain content | Constitution only; domain content relocated to its owners |
| "AI-first company" vs founder-approved positioning | Aligned to founder-approved positioning (D-002) |
| Delivery defined in two places, differently | `DELIVERY.md` §2 only |
| Open questions scattered across 7 documents | `OPEN_QUESTIONS.md` only |
| `DECISIONS.md`, `SOP_INDEX.md` referenced but absent | Created |
| SOPs as 1–3 sentence stubs | Nine SOPs at the ten-element standard |
| No agent met the required definition | All eight meet `MASTER.md` §10.2 |
| No project initialization or client isolation | `clients/_CLIENT_TEMPLATE/` |
| Strategy authoritative in a binary `.docx` | Markdown source of truth; `.docx` demoted to `exports/` |
