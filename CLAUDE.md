# CLAUDE.md — AI OPERATING INSTRUCTIONS

**System:** Governance
**Purpose:** Orient an AI session in this repository and define what to load, what may be decided, and what must be escalated.
**Authority:** Tier 3. Derived from `MASTER.md` §5.4 and §10.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme)
**Applies to:** Every AI session operating on this repository.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Structural change; recurring AI failure mode.
**Related:** `governance/AUTHORITY.md`, `agents/README.md`, `SYSTEM_MAP.md`

---

## 1. What This Repository Is

The operating system for **The Milbourne Group** — a boutique strategic
digital systems partner. It is a business operating system, not a codebase.

`MASTER.md` is the **ultimate authority**. Nothing here outranks it.

## 2. Start Here — Always Load

Read these three before any substantive work. Together they are short.

1. **`MASTER.md`** — how the company operates. Supreme.
2. **`governance/AUTHORITY.md`** — which document wins in a conflict.
3. **`OPEN_QUESTIONS.md`** — what is **not** known and must never be invented.

Then load only what the task needs (§3). More context is not better context
(`MASTER.md` §5.4).

## 3. Layered Context Loading

| Working on | Also load |
|---|---|
| Strategy, positioning, market | `STRATEGIC_CONFIGURATION.md`, `DECISIONS.md`, `BUSINESS.md` |
| Sales, qualification, proposals | `SALES.md`, `ICP.md`, `SERVICES.md`, `sops/sales/` |
| Marketing, content, SEO | `MARKETING.md`, `BRAND.md`, `ICP.md` |
| Delivery, project execution | `DELIVERY.md`, `sops/delivery/`, the client's directory |
| Design | `WEB_STANDARDS.md`, `BRAND.md` |
| Development | `WEB_STANDARDS.md`, `TECH_STACK.md`, the repository's own `CLAUDE.md` |
| QA | `sops/delivery/QA.md`, `WEB_STANDARDS.md`, the project brief |
| Automation | `AUTOMATION.md`, `SECURITY.md` |
| Anything touching client data | `SECURITY.md` — mandatory |
| Changing any document | `governance/CHANGE_MANAGEMENT.md`, `governance/DOCUMENT_REGISTRY.md` |
| Acting in an agent role | `agents/README.md` and that agent's file |

Lost? `SYSTEM_MAP.md` shows the whole architecture.

## 4. The Four Rules That Matter Most

### 4.1 Never invent an open value

If something is registered in `OPEN_QUESTIONS.md`, it is **not known**. Never
supply a price, niche, client size, buyer title, timeline guarantee, package
contents, metric, or brand asset that the founder has not decided.

This is the highest-frequency and most damaging failure mode in this system
(`RISKS.md` R-006). The output looks complete and is false.

**When blocked:** name the question, do everything that does not depend on it,
then either escalate or proceed under an assumption recorded in
`ASSUMPTIONS.md` and labelled in the output.

### 4.2 Never contradict confirmed strategy

`STRATEGIC_CONFIGURATION.md` and `Confirmed` entries in `DECISIONS.md` are
founder decisions. In particular: **never describe the company as AI-first, and
never lead with AI as the value proposition** (D-002).

If evidence suggests a confirmed decision is wrong, write a decision brief —
do not act on the contradiction.

### 4.3 Never claim unperformed verification

State what was actually checked and what was not (`MASTER.md` §9.3). A false
completion claim is worse than an incomplete deliverable because it removes
the chance to correct it.

### 4.4 Never mix client contexts

One client per session. No credential values anywhere — names and locations
only. Absolute constraints under `MASTER.md` §7.

## 5. Decide or Escalate

**Decide and proceed:** applying documented policy to a specific case;
drafting for review; analysis and research; work following an existing SOP;
correcting a document to match a higher-tier document; recording a finding in a
register.

**Escalate to the founder:** strategy, positioning, market, ICP, services,
pricing, brand identity, financial or contractual commitments, hiring, major
technology commitments, autonomy increases, and anything irreversible,
externally visible, or client-facing.

**Default: if it is not clearly delegated, it is reserved**
(`governance/AUTHORITY.md` §7).

## 6. Where Output Goes

Use the placement decision tree in
`governance/KNOWLEDGE_ARCHITECTURE.md` §3. Briefly:

- Client-specific → `clients/<client>/`
- A founder decision → `DECISIONS.md`
- An unknown → `OPEN_QUESTIONS.md`
- An unconfirmed premise being relied on → `ASSUMPTIONS.md`
- A threat → `RISKS.md`
- A repeatable procedure → `sops/<domain>/`
- True across all clients in one domain → that domain's document
- A universal operating rule → `MASTER.md` (founder approval required)

**Never** create a second document on a subject that already has an owner
(`governance/DOCUMENT_REGISTRY.md`).

## 7. Changing Documents

Editorial fixes: just make them. Anything substantive: follow
`governance/CHANGE_MANAGEMENT.md`, including the **downstream impact pass** —
a change that leaves dependent documents contradicting it is not finished.

Changes to `MASTER.md`, `STRATEGIC_CONFIGURATION.md`, or a `Confirmed`
decision require explicit founder approval.

## 8. Before Declaring Work Complete

Run the Fast Check in `governance/SYSTEM_QA.md` §3:

- [ ] Changes match their higher-tier parent
- [ ] No open value was invented
- [ ] Assumptions recorded and labelled
- [ ] Dependent documents still consistent
- [ ] No credentials, client data, or cross-client context leaked
- [ ] Every verification claim is true

## 9. Conventions

- Reference documents by path in backticks: `` `SALES.md` ``
- Decisions as `D-###`, questions as `Q-###`, assumptions as `A-###`, risks as
  `R-###`
- Status vocabulary: `Confirmed` · `Provisional` · `Open` · `Deprecated`
  (`governance/AUTHORITY.md` §10)
- Update `Last reviewed` when changing a document substantively
