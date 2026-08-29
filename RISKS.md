# RISK REGISTER

**System:** Operations / Governance
**Purpose:** Track material risks to the business and to the operating system, with owners, mitigations, and review triggers.
**Authority:** Tier 3.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Company-level risk. Project-specific risk belongs in the project brief.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Quarterly; any risk materializing; Discovery Round 2.
**Related:** `DECISIONS.md`, `OPEN_QUESTIONS.md`, `ASSUMPTIONS.md`, `SECURITY.md`

---

## Scoring

**Likelihood** and **Impact** are rated Low / Medium / High. Severity is the
combination. A risk rated High/High requires an active mitigation owner and a
named review date, not monitoring alone.

---

## Strategic Risks

### R-001 — Commercial focus still incomplete
**Likelihood:** High · **Impact:** High · **Owner:** Founder

The adopted strategy resolved capability-versus-positioning, but initial
market focus is unresolved. A decision is still needed on whether to narrow by
industry, business maturity, buyer type, or a more specific recurring problem.

**Mitigation.** Resolved by D-019, D-020, D-023 and D-036. The residual risk is that the broad initial market never narrows;
acquisition stays deliberately small and evidence-gathering.

**Source:** `.docx` §10 Risk 1.

---

### R-002 — AI positioning drifting above client value
**Likelihood:** Medium · **Impact:** High · **Owner:** Founder

AI and automation are operating advantages. If public messaging leads with
them, the company is compared against commodity AI vendors — the category
D-007 explicitly excludes.

**Mitigation.** D-002 corrected the identity statements in `MASTER.md` and
`BUSINESS.md`. `BRAND.md` §2 and §6 prohibit exaggerated AI claims. The brand
review checklist and `agents/SEO_AGENT.md` enforce it per artifact.

**Materialized once already:** `MASTER.md` §2.1 and `BUSINESS.md` §2 both
carried AI-first identity claims until 2026-08-29.

**Source:** `.docx` §10 Risk 2.

---

### R-003 — Pricing and acquisition cannot yet be finalized
**Likelihood:** High · **Impact:** Medium · **Owner:** Founder

Pricing, packaging, acquisition channels, and capacity planning depend on
detailed ICP, buying triggers, founder advantages, revenue urgency, and
capacity.

**Mitigation.** Resolved by D-038 and D-036. The residual risk is that the bands prove wrong (A-007), rather than that they are
generic assumptions. `BUSINESS.md` §10 enforces "pricing to be determined."

**Source:** `.docx` §10 Risk 3.

---

### R-004 — Revenue concentration
**Likelihood:** Medium · **Impact:** High · **Owner:** Founder

A boutique model with few concurrent engagements concentrates revenue in a
small number of clients. Losing one is materially disruptive.

**Mitigation.** `METRICS.md` §3 tracks revenue concentration. The D-005
recurring stage is the structural answer; prioritize it once delivery capacity
is proven.

---

### R-005 — Founder capacity is the binding constraint
**Likelihood:** High · **Impact:** High · **Owner:** Founder

D-010 places strategy, sales, discovery, architecture, relationships, and QA
with the founder. Sales and delivery compete for the same person, producing
the feast-famine cycle typical of founder-led services businesses.

**Mitigation.** `ROADMAP.md` Phase 4 automation; `MASTER.md` bottleneck
analysis; D-037 sets one major engagement at a time (A-008) before committing to
concurrent engagements.

---

## Operating System Risks

### R-006 — Agents fabricating open configuration values
**Likelihood:** High · **Impact:** High · **Owner:** Founder

The highest-frequency AI failure mode in this system. An agent asked to draft
a proposal or landing page will be tempted to supply a price, a niche, a
client size, or a guarantee that has never been decided. The output looks
complete and is false.

**Mitigation.** `OPEN_QUESTIONS.md` is the single authoritative list of what
is unknown. The status vocabulary in `governance/AUTHORITY.md` §9 makes
`Open` a hard stop. Every agent definition carries an explicit forbidden
action against it. `governance/SYSTEM_QA.md` checks for it before work is
declared complete.

---

### R-007 — Documentation drift between tiers
**Likelihood:** Medium · **Impact:** Medium · **Owner:** Founder

A change to a domain document leaves SOPs, agents, and templates describing
the old policy. The system then contains two truths — the failure that
produced the four competing precedence statements found in this audit.

**Mitigation.** `governance/CHANGE_MANAGEMENT.md` requires a downstream-impact
pass on every Tier 1–3 change. `governance/DOCUMENT_REGISTRY.md` records
dependencies so the impact set is discoverable rather than remembered.

---

### R-008 — Client context contamination
**Likelihood:** Medium · **Impact:** High · **Owner:** Founder

An AI operator carrying context between engagements may leak one client's
strategy, credentials, or data into another's deliverable.

**Mitigation.** Absolute constraint under `MASTER.md` §7. `SECURITY.md` §4, `MASTER.md` §7.1,
`clients/_CLIENT_TEMPLATE/` isolation structure, and the context-loading rules
in `CLAUDE.md`. Load exactly one client's directory per session.

---

### R-009 — Process theatre
**Likelihood:** Medium · **Impact:** Medium · **Owner:** Founder

A single-operator company can accumulate governance overhead that consumes
more capacity than it protects, causing operators to bypass the system.

**Mitigation.** `ROADMAP.md` §7 — a document existing is not completion.
`governance/CHANGE_MANAGEMENT.md` §2 routes routine edits with no ceremony.
Retire any control that has not changed an outcome within two quarters.

---

## Materialized Risks

*Record here when a risk occurs, with date, actual impact, and the corrective
action taken.*

- **2026-08-29 — R-002 materialized.** Two Tier 2/3 documents carried AI-first
  identity claims contradicting founder-approved positioning. Corrected under
  D-002. No client-facing material had been produced from them.

---

### R-010 — Tax and legal jurisdiction unstated
**Category:** Legal / commercial · **Likelihood:** Medium · **Impact:** Medium

**Risk.** D-038 sets prices in USD, but no tax treatment or governing legal
jurisdiction is recorded. Proposal and agreement templates therefore carry no
jurisdiction-specific commercial or legal terms.

**Consequence.** A first agreement could be executed without terms appropriate
to the jurisdiction it operates in, or priced without accounting for applicable
tax.

**Mitigation.** Establish tax treatment and governing jurisdiction before the
first agreement is executed. This is execution work, not a strategic decision —
it does not block sales activity, only contract execution.

**Owner:** Founder. **Review trigger:** Before the first executed agreement.

