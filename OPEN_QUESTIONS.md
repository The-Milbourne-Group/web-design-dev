# OPEN QUESTIONS REGISTER

**System:** Operations / Governance
**Purpose:** The single register of unresolved decisions requiring founder input. Consolidates the open items previously scattered across seven documents.
**Authority:** Tier 3. Authoritative about *what is undecided*. It does not decide anything.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Every agent and operator. Before inventing a value, check here.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Discovery Round 2; any question answered; any new blocking unknown.
**Related:** `DECISIONS.md`, `STRATEGIC_CONFIGURATION.md`, `ASSUMPTIONS.md`, `RISKS.md`

---

## The Rule

If a value is registered here, it is **not known**. Do not invent it, do not
infer it from an example, and do not copy it from a template.

When work requires an open value:

1. State which question blocks the work.
2. Complete every part of the work that does not depend on it.
3. Either escalate to the founder, or proceed under an explicit assumption
   recorded in `ASSUMPTIONS.md` and labelled in the output.

Fabricating an answer to an open question is a governance failure, not a
shortcut. It creates false company facts that propagate into client-facing
material.

**Before this register existed,** these questions were duplicated across
`STRATEGIC_CONFIGURATION.md`, `EXECUTIVE_SUMMARY.md`, `BUSINESS.md` §15,
`ICP.md` §8, `SERVICES.md` §6, `TECH_STACK.md` §3, and the `.docx` §11 — in
overlapping but non-identical lists. Those documents now link here.

---

## Priority Definitions

| Priority | Meaning |
|---|---|
| **Blocking** | Named downstream work cannot responsibly proceed at all |
| **High** | Work can proceed under an explicit assumption, but quality is materially degraded |
| **Medium** | Useful to resolve; sensible defaults exist |

---

## Discovery Round 2 — Founder Input Required

These are the founder's own deferred questions, ported from
`exports/EXECUTIVE_STRATEGIC_CONFIGURATION.docx` §11. They are deliberate
dependencies, not oversights.

### Q-001 — Industry focus · Blocking
**Question.** Should the company remain industry-agnostic initially, select
one primary industry, focus on a cluster of related industries, or test
multiple markets and specialize based on evidence?

**Why it matters.** Determines ICP detail, messaging specificity, acquisition
channel selection, and portfolio strategy. Nearly all marketing and sales
configuration depends on it.

**Founder's recorded default.** Start controlled and evidence-driven, then
specialize based on traction.

**Blocks.** `ICP.md` §8, `MARKETING.md` channel strategy, acquisition build-out (`ROADMAP.md` Phase 2).

---

### Q-002 — Business maturity target · High
**Question.** Should the company target businesses that have proven they can
sell and operate successfully, but whose digital infrastructure has not kept
pace with growth?

**Why it matters.** Sharpens qualification criteria and the buying trigger.

**Founder's recorded default.** Yes.

**Blocks.** `ICP.md` detailed profile.

---

### Q-003 — Detailed ICP and buyer roles · Blocking
**Question.** What are the exact company-size bands, revenue or headcount
ranges, buyer titles, and buying-committee composition?

**Why it matters.** Qualification, outreach targeting, proposal structure, and
discovery all need a concrete buyer. `ICP.md` §6 currently — and correctly —
refuses to invent buyer titles.

**Depends on.** Q-001, Q-002.

**Blocks.** Outreach, qualification scoring, proposal targeting.

---

### Q-004 — Primary buying trigger · High
**Question.** Should the primary commercial trigger be: *"Our business has
outgrown our current website and digital systems, and they are now becoming a
constraint on growth"*?

**Secondary triggers under consideration.** Rebranding, expansion, poor
website performance, weak conversion, operational inefficiency, disconnected
tools, excessive manual work.

**Why it matters.** The trigger is the core of messaging and the opening of
every qualification conversation.

---

### Q-005 — Founder advantages · Blocking
**Question.** What existing founder advantages should influence market
selection — industry experience, professional relationships, technical
capabilities, sales experience, past projects, geographic relationships,
communities, potential referral partners?

**Why it matters.** The founder's own analysis identifies this, with Q-006, as
the **highest-leverage input** because it may materially alter market
selection. Answering Q-001 before Q-005 risks selecting a market that ignores
the company's strongest unfair advantage.

**Blocks.** Q-001 should not be finalized before this is answered.

---

### Q-006 — Revenue urgency and capacity · Blocking
**Question.** Which best reflects the business: validate carefully, generate
revenue quickly, build a scalable platform with slower commercialization, or
balance revenue generation with deliberate system-building? What are the
founder's actual weekly hours and concurrent-project capacity?

**Why it matters.** Determines roadmap sequencing, acceptable engagement size,
whether to prioritize acquisition over systems, and how much delivery the
company can safely commit to. `ROADMAP.md` phase ordering assumes an answer.

**Founder's recorded default.** Balanced, unless actual financial constraints
require a revenue-first approach.

---

### Q-007 — Pricing and engagement economics · Blocking
**Question.** What is the pricing model, minimum engagement size, package
economics, margin target, and revenue target?

**Why it matters.** No proposal can be issued without it. `BUSINESS.md` §10
mandates "pricing to be determined" until configured, and `SERVICES.md`
withholds package definitions.

**Depends on.** Q-003, Q-005, Q-006.

**Blocks.** Proposals, `SERVICES.md` package definitions, `METRICS.md` revenue
targets, all commercial forecasting.

---

### Q-008 — Acquisition channels · High
**Question.** Which specific channels are the initial focus, and in what
order?

**Why it matters.** `MARKETING.md` §3 lists candidate channels but states none
are mandatory. Without a decision, marketing effort disperses.

**Depends on.** Q-001, Q-005.

---

## Operational Open Questions

### Q-009 — Approved technology stack · High
**Question.** What is the company-wide approved stack for websites, web
applications, hosting, CMS, and integrations?

**Why it matters.** `TECH_STACK.md` §3 forbids claiming any technology is
standard until authorized. Every project currently re-decides its stack,
preventing reusable assets — a `ROADMAP.md` Phase 3 objective.

---

### Q-010 — Visual identity · Medium
**Question.** What are the official colours, typography, logo, and visual
system?

**Why it matters.** `BRAND.md` §8 forbids inventing these. Company website and
all collateral depend on it.

---

### Q-011 — Service package contents · High
**Question.** For each stage in the D-005 progression, what are the exact
deliverables, inclusions, exclusions, timelines, and guarantees?

**Why it matters.** The progression is confirmed; its contents are not.
Proposals cannot be standardized without it.

**Depends on.** Q-007.

---

### Q-012 — Escalation contact and response expectations · Medium
**Question.** For security incidents and delivery escalations, who is the
named responsible authority and what response time applies?

**Why it matters.** `SECURITY.md` §7 says "escalate to the responsible
authority" without naming one. In a founder-led company this is presumed to be
the founder, recorded as an assumption (A-004) pending confirmation.

---

## Resolved

*None yet. When a question is answered, move it here with the resolution date
and the `DECISIONS.md` ID that records the decision.*
