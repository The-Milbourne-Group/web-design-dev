# SOP: SOLUTION DESIGN

**System:** Sales
**Purpose:** Convert discovery findings into a recommended solution without introducing requirements the discovery does not support.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `SALES.md` §5, `SERVICES.md` §6
**Applies to:** Every opportunity between discovery and proposal.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Recurring scope disputes traced to the proposal; package or pricing revision.
**Related:** `sops/sales/DISCOVERY.md`, `SERVICES.md`, `templates/sales/PROPOSAL_OUTLINE.md`

---

## 1. Purpose

This is the step where fabrication enters a commercial engagement. Discovery
produces findings; a proposal requires a scope. Between them, an operator must
decide what to build — and the temptation is to fill gaps with plausible
requirements the client never expressed.

Every requirement in a proposal must trace to a discovery finding, an explicit
client statement, or a documented assumption. **Nothing else is admissible.**

`SALES.md` §5 sets the policy: recommend the minimum viable scope that
responsibly solves the problem. This procedure enforces it.

## 2. Trigger

Discovery is complete and playback confirmed (`sops/sales/DISCOVERY.md` §5.9).

## 3. Owner

Founder. Solution architecture is founder-led work (D-010). Agents may prepare
the traceability matrix and draft options; they may not decide the solution.

## 4. Inputs

- `clients/<client>/DISCOVERY.md` — confirmed findings, assumptions, open
  questions
- `SERVICES.md` §2 — the commercial progression and what each stage covers
- `ICP.md` fit assessment from qualification
- `SERVICES.md` §2.4 and §7 — the approved price bands and package contents

## 5. Procedure

1. **Restate the problem** from discovery, in the client's words. If it cannot
   be stated in one sentence, discovery is incomplete — return to it.

2. **Build the traceability matrix.** For every proposed requirement, record
   its source. This is the core control of this SOP.

   | Requirement | Source | Type |
   |---|---|---|
   | | Discovery §N / client statement / assumption A-# | Confirmed / Assumed |

   **A requirement with no source is removed, not justified.** If it is
   genuinely necessary, it is an *assumption* — record it in the client's
   directory and label it in the proposal.

3. **Identify the minimum viable scope.** What is the smallest set of
   requirements that responsibly solves the stated problem? Everything else is
   a candidate for a later stage, not this engagement.

4. **Locate the engagement** in the commercial progression (`SERVICES.md` §2).
   Entry engagements do not silently absorb expansion work — that is a
   separate engagement, and proposing it as one is `SERVICES.md` §6 compliance,
   not a lost sale.

5. **Separate the deferred.** List what was considered and deliberately left
   out, with the reason. This becomes the exclusions section of the proposal
   and the expansion opportunity list at closure.

6. **Check feasibility** against current capability and capacity. A capability
   the company does not have is not a stretch goal.

7. **Record open dependencies.** Any requirement that cannot be specified
   because a company decision is genuinely absent is marked as dependent —
   never filled with a default.

8. **Verify against discovery.** Re-read the discovery notes and confirm that
   nothing in the solution contradicts what the client actually said, and that
   no stated problem is left unaddressed.

## 6. Outputs

**Location:** `clients/<client>/SOLUTION.md`. Set `Status: Proposal`.

- Problem restatement
- Requirement traceability matrix
- Minimum viable scope
- Deferred items with reasons (feeds proposal exclusions)
- Feasibility assessment
- Open dependencies
- Recommended engagement stage

## 7. Quality Checks

- [ ] **Every requirement traces to a source.** No unsourced requirement
      survives.
- [ ] Assumed requirements are labelled as assumed, not stated as client needs.
- [ ] The scope is the minimum that solves the problem, not the maximum the
      client might buy.
- [ ] Every problem raised in discovery is addressed or explicitly deferred.
- [ ] Nothing contradicts what the client said.
- [ ] No requirement depends on a value nobody has decided.
- [ ] Deferred items are recorded, not discarded.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Requirement has no discovery source | Remove it, or convert it to a labelled assumption and confirm with the client |
| Scope grew beyond the stated problem | Return to §5.3; move the excess to deferred |
| Solution addresses a problem the client did not raise | Either the discovery was incomplete or the solution is being sold — determine which |
| A discovery problem is unaddressed | Address it or record it as an explicit exclusion; silence becomes a dispute later |
| Scope stated beyond the approved packages | Return to `SERVICES.md` §7; a proposal does not extend the offer set |
| Entry engagement absorbing expansion work | Split it; propose expansion as a separate stage (`SERVICES.md` §2) |

## 9. Escalation

Escalate when: the solution requires capability the company does not have; the
minimum viable scope still exceeds what the client can invest; the problem
cannot be responsibly solved; the engagement does not fit any stage of the
progression; or specification depends on an open company decision.

## 10. Automation Potential

**Can be assisted:** building the traceability matrix from discovery notes,
detecting requirements with no source, detecting discovery problems left
unaddressed, drafting option sets.

**Must not be automated:** deciding the solution, judging minimum viable
scope, and assessing feasibility. Automated traceability checking is
genuinely valuable here — the unsourced-requirement check in §7 is mechanical
and catches the failure mode this SOP exists to prevent.
