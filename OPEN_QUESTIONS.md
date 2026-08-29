# OPEN QUESTIONS REGISTER

**System:** Operations / Governance
**Purpose:** The single register of decisions requiring founder input, and the permanent record of how each was resolved.
**Authority:** Tier 3. Authoritative about *what is undecided*. It does not decide anything.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Every agent and operator. Before inventing a value, check here.
**Owner:** Founder
**Status:** Active — **no pending founder decisions.** Strategic configuration complete.
**Last reviewed:** 2026-08-29
**Review trigger:** A genuine new blocking unknown requiring founder decision. Ordinary execution decisions do not belong here.
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

## No Pending Decisions

**Strategic configuration is complete.** Every question this register has held
is resolved and recorded in `DECISIONS.md`. The company has moved from
discovery into commercial execution.

### What this register is not for

This register holds **founder decisions that block work**. It is not a place to
postpone ordinary execution decisions. Future uncertainty is handled where it
belongs:

| Kind of uncertainty | Where it goes |
|---|---|
| An unconfirmed premise being relied on | `ASSUMPTIONS.md` |
| A threat to be tracked and mitigated | `RISKS.md` |
| Something to be learned from real delivery | `METRICS.md`, and the retrospective in `sops/delivery/CLOSURE.md` §5.9 |
| An operational choice inside existing policy | Decide and proceed (`governance/AUTHORITY.md` §7) |

Reopening this register requires a genuine new blocking unknown — a decision
reserved to the founder under `governance/AUTHORITY.md` §7 that no existing
decision answers. **Add an entry only when work actually stops without it.**

---

## Resolved — Complete History

### Launch configuration (2026-08-29) — values

| Question | Decision | Outcome |
|---|---|---|
| Q-013 · Founder advantage inventory | D-036 | Capability-based advantage; six confirmed strengths; initial market; diversified acquisition |
| Q-014 · Capacity and financial requirements | D-037 | One major build at a time; max two active; revenue-prioritized validation; three-project target |
| Q-015 · Price points and engagement economics | D-038 | $5,000 minimum; entry $7,500–25,000; assessment $1,500–5,000; recurring from $750/mo; 50/25/25 |
| Q-016 · Named technology stack | D-039 | Next.js + TypeScript, Tailwind, PostgreSQL, Vercel or equivalent |
| Q-017 · Brand asset values | D-040 | Inter; `#111111` `#F7F7F5` `#6B7280` `#E5E7EB` `#1D4ED8`; 4px spacing; 4–8px radius |

*The residuals opened during Round 3 — Q-018 to Q-022 — were resolved by the
same decisions and never required separate founder input.*

### Discovery Round 3 (2026-08-29) — method and specification

| Question | Decision | Resolved as to |
|---|---|---|
| Q-013 · Founder advantage inventory | D-031 | Five required categories, case-study policy, market-selection scoring |
| Q-014 · Capacity and financial requirements | D-032 | Hours split, capacity matrix, urgency levels, governance rule |
| Q-015 · Price points and engagement economics | D-033 | Three layers, minimum-engagement formula, margin and target rules |
| Q-016 · Named technology stack | D-034 | Categories, selection rule, exception process |
| Q-017 · Brand asset values | D-035 | Required assets and governance |

### Discovery Round 2 (2026-08-29) — strategic configuration

| Question | Decision | Outcome |
|---|---|---|
| Q-001 · Industry focus | D-019 | Controlled market testing; specialize on evidence |
| Q-002 · Business maturity target | D-020 | Yes — the digital maturity gap |
| Q-003 · ICP and buyer roles | D-021 | Size bands and buyer roles; retires A-005 |
| Q-004 · Primary buying trigger | D-022 | Yes — outgrown digital infrastructure |
| Q-005 · Founder advantages | D-023 | Market selection incorporates founder advantage |
| Q-006 · Revenue urgency and capacity | D-024 | Balanced with override — *override now active per D-037* |
| Q-007 · Pricing and engagement economics | D-025 | Value-oriented fixed-scope model |
| Q-008 · Acquisition channels | D-026 | Concentrated multi-channel — *priority order amended by D-036* |
| Q-009 · Approved technology stack | D-027 | Default architecture with controlled exceptions |
| Q-010 · Visual identity | D-028 | Competence over trend |
| Q-011 · Service package contents | D-029 | Five-stage progression with explicit boundaries |
| Q-012 · Escalation contact and response | D-030 | Founder authority; response targets; retires A-004 |

---

## How Pricing Was Resolved

Worth recording, because the chain was long and the failure mode it created was
real.

```
Q-007 → D-025 (model)  → Q-015 → D-033 (structure) → Q-020 → D-038 (values)
```

Each round approved an architecture and deferred the number. Three times, an
operator reading `Q-007 · Resolved` could have concluded pricing was known when
no figure existed. The runtime guard therefore keyed on the **live residual**
rather than the resolved parent, and moved each time a value was deferred again.

**That chain is now closed.** D-038 holds real figures, and the guard no longer
blocks issuance on pricing — it validates against the approved bands instead.
