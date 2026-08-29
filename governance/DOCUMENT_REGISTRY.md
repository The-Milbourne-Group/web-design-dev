# DOCUMENT REGISTRY

**System:** Governance
**Purpose:** Record every document in the system, the subject it exclusively owns, its authority tier, its owner, and which documents depend on it.
**Authority:** Tier 3 governance. Authoritative for *which document owns which subject*.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Anyone adding, changing, or retiring a document; every downstream impact pass.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Any document created, retired, or given a new subject.
**Related:** `governance/CHANGE_MANAGEMENT.md`, `governance/KNOWLEDGE_ARCHITECTURE.md`, `SYSTEM_MAP.md`

---

## 1. How to Use This Registry

**Before creating a document:** check whether its subject is already owned. If
it is, extend the existing document instead. Two documents owning one subject
is the defect this registry exists to prevent (`MASTER.md` §5.3).

**Before changing a document:** read its "Depended on by" column. Those are the
documents your change may falsify — the downstream impact pass in
`governance/CHANGE_MANAGEMENT.md` §3.

---

## 2. Constitutional and Governance

| Document | Tier | Exclusively owns | Depended on by | Owner |
|---|---|---|---|---|
| `MASTER.md` | 1 | Universal operating rules, execution protocol, quality standard, absolute constraints, agent governance, authorization boundaries | **Everything** | Founder |
| `governance/AUTHORITY.md` | 3 | Precedence model, scope rule, decision rights, conflict procedure | All documents; every agent | Founder |
| `governance/CHANGE_MANAGEMENT.md` | 3 | How knowledge changes; promotion and retirement | All documents; all agents | Founder |
| `governance/KNOWLEDGE_ARCHITECTURE.md` | 3 | Knowledge classes and placement rules | `SYSTEM_MAP.md`, `CLAUDE.md` | Founder |
| `governance/DOCUMENT_REGISTRY.md` | 3 | Subject ownership and dependency map | `CHANGE_MANAGEMENT.md` | Founder |
| `governance/SYSTEM_QA.md` | 3 | System-level consistency checks | Agents completing work | Founder |
| `SYSTEM_MAP.md` | 3 | Architecture, flows, and traces | `README.md`, `CLAUDE.md` | Founder |
| `CLAUDE.md` | 3 | AI context-loading protocol | All AI sessions | Founder |
| `README.md` | — | Human navigation | — | Founder |

## 3. Strategy

| Document | Tier | Exclusively owns | Depended on by | Owner |
|---|---|---|---|---|
| `STRATEGIC_CONFIGURATION.md` | 2 | Strategic identity, positioning, market, commercial model, competitive position | `BUSINESS.md`, `SERVICES.md`, `ICP.md`, `BRAND.md`, `MARKETING.md`, `SALES.md`, `ROADMAP.md`, `MASTER.md` §2 | Founder |
| `DECISIONS.md` | 2 | The permanent record of significant decisions | All documents citing a D-### | Founder |
| `EXECUTIVE_SUMMARY.md` | — | *Nothing.* Summary only — no authority | — | Founder |
| `ROADMAP.md` | 3 | Capability sequencing and phase priority | `MASTER.md` §12.2 | Founder |

## 4. Domain Sources of Truth

| Document | Tier | Exclusively owns | Depended on by | Owner |
|---|---|---|---|---|
| `BUSINESS.md` | 3 | Business model, market selection criteria, offer architecture, pricing principles, revenue quality | `SERVICES.md`, `ICP.md`, `METRICS.md`, `MARKETING.md`, `agents/STRATEGY_AGENT.md` | Founder |
| `BRAND.md` | 3 | Brand positioning, voice, messaging hierarchy, claims standard, visual direction | `MARKETING.md`, `SALES.md`, `SERVICES.md`, `agents/SEO_AGENT.md`, `agents/DESIGN_AGENT.md` | Founder |
| `SERVICES.md` | 3 | Service definitions, offer boundaries, scope discipline | `SALES.md`, `ICP.md`, `MARKETING.md`, `DELIVERY.md`, `templates/sales/PROPOSAL_OUTLINE.md` | Founder |
| `ICP.md` | 3 | Target-client definition, fit and disqualification signals, qualification criteria | `SALES.md`, `MARKETING.md`, `sops/sales/QUALIFICATION.md`, `agents/SALES_AGENT.md` | Founder |
| `MARKETING.md` | 3 | Demand generation, channels, content policy, experimentation | `agents/SEO_AGENT.md`, `METRICS.md` | Founder |
| `SALES.md` | 3 | Sales pipeline, qualification standard, proposal standard, sales ethics, handoff | `sops/sales/`, `templates/sales/`, `agents/SALES_AGENT.md`, `DELIVERY.md` | Founder |
| `DELIVERY.md` | 3 | **Delivery lifecycle and phases**, scope control, quality gates, client communication, escalation | `sops/delivery/`, `templates/delivery/`, `clients/_CLIENT_TEMPLATE/`, all delivery agents | Founder |
| `WEB_STANDARDS.md` | 3 | Web product craft: page standard, design priority, accessibility baseline, implementation and performance standards | `DELIVERY.md`, `TECH_STACK.md`, `sops/delivery/QA.md`, `agents/DESIGN_AGENT.md`, `agents/DEV_AGENT.md` | Founder |
| `TECH_STACK.md` | 3 | Technology selection, repository standards, technical change control, technical debt | `agents/DEV_AGENT.md`, `templates/development/` | Founder |
| `AUTOMATION.md` | 3 | **Automation levels**, workflow standard, AI output handling, automation review | `agents/AUTOMATION_AGENT.md`, `sops/automation/`, `templates/automation/`, `MASTER.md` §11 | Founder |
| `SECURITY.md` | 3 | Security controls, secrets handling, access, incident response | All agents; all projects | Founder |
| `METRICS.md` | 3 | **Metric definitions** and measurement governance | `MARKETING.md`, `SALES.md`, `DELIVERY.md`, `AUTOMATION.md`, `BUSINESS.md` | Founder |

## 5. Registers

| Document | Tier | Exclusively owns | Depended on by | Owner |
|---|---|---|---|---|
| `OPEN_QUESTIONS.md` | 3 | **The single list of unresolved decisions** | All documents; all agents before supplying a strategic value | Founder |
| `ASSUMPTIONS.md` | 3 | Working assumptions and their consequence-if-wrong | Documents relying on an unconfirmed premise | Founder |
| `RISKS.md` | 3 | Company and system risk | `MASTER.md` §12.3, quarterly review | Founder |
| `GLOSSARY.md` | 3 | Term definitions | All documents | Founder |
| `SOP_INDEX.md` | 3 | SOP catalogue and routing | `sops/`, all agents | Founder |

## 6. Procedural, Agent, and Asset Layers

| Location | Tier | Owns | Owner |
|---|---|---|---|
| `sops/**` | 4 | Execution procedure for one named process | Founder |
| `agents/README.md` | 5 | Agent registry and task routing | Founder |
| `agents/*.md` | 5 | One agent's mission, authority, and boundaries | Founder |
| `templates/**` | 6 | Reusable structure — no factual authority | Founder |
| `clients/_CLIENT_TEMPLATE/` | 6 | Opportunity and project initialization scaffold | Founder |
| `clients/<client>/**` | 7 | One client or opportunity's knowledge, from qualification to closure | Founder |
| `exports/` | — | Generated presentation artifacts — **no authority** | Founder |

---

## 7. Subjects With a Single Named Owner

These were duplicated across documents before 2026-08-29. Each now has exactly
one owner; any other document mentioning them must reference, not restate.

| Subject | Sole owner | Previously also in |
|---|---|---|
| Delivery lifecycle and phases | `DELIVERY.md` | `MASTER.md` §14 (9 phases, conflicting order) |
| Automation autonomy levels | `AUTOMATION.md` | `MASTER.md` §12.2 |
| Metric definitions | `METRICS.md` | former `MASTER.md` §16.1 |
| Web implementation standards | `WEB_STANDARDS.md` | former `MASTER.md` §11.3 and `TECH_STACK.md` §5 |
| SOP structure standard | `SOP_INDEX.md` | former `MASTER.md` §15.2 and `sops/README.md` |
| Authority and precedence | `governance/AUTHORITY.md` | `MASTER.md` §5.1, both READMEs, `STRATEGIC_CONFIGURATION.md` |
| Open configuration items | `OPEN_QUESTIONS.md` | `BUSINESS.md` §15, `ICP.md` §8, `SERVICES.md` §6, `TECH_STACK.md` §3, `EXECUTIVE_SUMMARY.md`, `STRATEGIC_CONFIGURATION.md`, `.docx` §11 |
| Repository architecture | `SYSTEM_MAP.md` | former `MASTER.md` §19 (specified files that did not exist) |
| Requirement traceability (discovery → scope) | `sops/sales/SOLUTION_DESIGN.md` | *nothing — the step was undocumented* |
| Engagement closure and expansion review | `sops/delivery/CLOSURE.md` | *nothing — `DELIVERY.md` §9/§11 stated intent only* |
| Pre-agreement opportunity knowledge | `clients/<client>/` from qualification | *nothing — artifacts had no home* |

---

## 8. Retired

| Document | Retired | Reason |
|---|---|---|
| `Milbourne_Group_FINAL_BUSINESS_SYSTEM/README.md` | 2026-08-29 | Packaging artifact stating a precedence model that conflicted with `MASTER.md`. Replaced by root `README.md`. |
| `THE-MILBOURNE-GROUP-FINAL/README.md` | 2026-08-29 | Second conflicting precedence statement. Merged into root `README.md`. |
| `EXECUTIVE_STRATEGIC_CONFIGURATION.docx` as an authority | 2026-08-29 | Demoted to `exports/`. Unique content ported to markdown (D-013). |

**Never created, though the former `MASTER.md` §19 mandated them:**
`FOUNDER_BRAIN_DUMP.md` (superseded by `STRATEGIC_CONFIGURATION.md` and the
registers), `prompts/` and `knowledge/` (no current content justifies them —
recreate only when real material exists).
