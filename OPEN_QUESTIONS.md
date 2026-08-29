# OPEN QUESTIONS REGISTER

**System:** Operations / Governance
**Purpose:** The single register of unresolved decisions requiring founder input. Consolidates the open items previously scattered across seven documents.
**Authority:** Tier 3. Authoritative about *what is undecided*. It does not decide anything.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Every agent and operator. Before inventing a value, check here.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Any question answered; any new blocking unknown.
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

## Open

*Discovery Round 2 resolved Q-001 – Q-012 (D-019 – D-030). What remains are the
inputs the founder's own answers identified as still required — several
decisions approved an architecture and explicitly deferred its values. **An
approved model is not an approved number.***

### Q-013 — Founder advantage inventory · Blocking
**Question.** What are the founder's actual industry and professional
experience, existing relationships and referral opportunities, and past
projects with the strongest case-study potential?

**Why it matters.** D-023 makes founder advantage an explicit input to market
selection and states no industry is chosen because it looks attractive in
theory. The decision rule is the intersection of *founder access + technical
advantage + market pain + project economics*, and one of those four terms is
currently unknown.

**Blocks.** Market selection under D-019; warm-network channel activation
(D-026 priority 1); any claim of relevant prior work.

---

### Q-014 — Founder capacity and financial requirements · Blocking
**Question.** What are the founder's actual available weekly hours, maximum
safe concurrent-project capacity, revenue urgency, and minimum income
requirement?

**Why it matters.** D-024 sets a capacity policy and a revenue-first override
but records the concurrent-project figure as an assumption to be measured.
Delivery commitments made without it are commitments made on a guess.

**Blocks.** Q-015; any commitment to concurrent delivery.

---

### Q-015 — Price points and engagement economics · Blocking
**Question.** What are the actual price points for each commercial layer, the
exact minimum engagement value, and the monthly, quarterly and annual revenue
and pipeline-coverage targets?

**Why it matters.** D-025 approved the pricing **architecture** and stated
explicitly that exact price points require founder financial inputs before
becoming policy. D-029 defers final package contents until pricing economics
exist. **Until this is answered no proposal may state a figure**, and
`SERVICES.md` §4 continues to bar presenting an offer without a pricing model.

**Depends on.** Q-013, Q-014.

**Blocks.** Proposal issuance; `SERVICES.md` package contents; `METRICS.md`
revenue targets; all commercial forecasting.

---

### Q-016 — Named technology stack · High
**Question.** Which specific technologies are the approved defaults for
marketing websites, custom web applications, CMS, hosting and integrations?

**Why it matters.** D-027 approved the stack **policy** — default architecture
with documented exceptions — but states the named technologies are to be
finalized in `TECH_STACK.md` based on what the company can confidently support.
Until then every project still re-decides, and reusable assets cannot
accumulate.

---

### Q-017 — Brand asset values · Medium
**Question.** What are the official logo, colour palettes, typography system
and spacing conventions?

**Why it matters.** D-028 approved the visual **direction** and the required
asset list, not the assets. `BRAND.md` §8 continues to forbid inventing them.

---

## Resolved

| Question | Resolved | Decision | Note |
|---|---|---|---|
| Q-001 — Industry focus | 2026-08-29 | D-019 | Controlled market testing; specialize on evidence |
| Q-002 — Business maturity target | 2026-08-29 | D-020 | Yes — the digital maturity gap |
| Q-003 — ICP and buyer roles | 2026-08-29 | D-021 | Size bands and buyer roles set; retires A-005 |
| Q-004 — Primary buying trigger | 2026-08-29 | D-022 | Yes — outgrown digital infrastructure |
| Q-005 — Founder advantages | 2026-08-29 | D-023 | Policy set; the inventory itself is Q-013 |
| Q-006 — Revenue urgency and capacity | 2026-08-29 | D-024 | Balanced, with revenue override; figures are Q-014 |
| Q-007 — Pricing and engagement economics | 2026-08-29 | D-025 | **Model only** — price points are Q-015 |
| Q-008 — Acquisition channels | 2026-08-29 | D-026 | Concentrated multi-channel, first three |
| Q-009 — Approved technology stack | 2026-08-29 | D-027 | **Policy only** — named technologies are Q-016 |
| Q-010 — Visual identity | 2026-08-29 | D-028 | **Policy only** — asset values are Q-017 |
| Q-011 — Service package contents | 2026-08-29 | D-029 | **Structure only** — contents follow Q-015 |
| Q-012 — Escalation contact and response | 2026-08-29 | D-030 | Founder; response targets set; retires A-004 |

**Three of these resolved a policy and deferred its values.** Q-007, Q-009,
Q-010 and Q-011 each approved an architecture whose numbers or assets are still
unknown, and those residuals are Q-015, Q-016 and Q-017. Treating the parent as
fully answered is how an invented price reaches a client.
