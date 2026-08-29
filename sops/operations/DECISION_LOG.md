# SOP: DECISION LOGGING

**System:** Operations
**Purpose:** Record significant decisions so reasoning survives the moment it was made.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme)
**Applies to:** Every significant company decision.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Decisions being re-litigated; register falling out of use.
**Related:** `DECISIONS.md`, `templates/strategy/DECISION_BRIEF.md`, `governance/CHANGE_MANAGEMENT.md`

---

## 1. Purpose

Preserve *why* a decision was made, not merely what was decided. Without the
reasoning, a future operator cannot tell whether changed circumstances warrant
revisiting it, and the decision gets silently re-litigated.

## 2. Trigger

A decision that changes strategy, commits money or capacity, creates an
obligation, sets policy, changes an authority boundary, or would be expensive
to reverse.

**Do not log** routine execution choices. Over-logging makes the register
unusable, which is a slower version of not having one.

## 3. Owner

Founder. Only the founder may record a decision as `Confirmed`.

## 4. Inputs

- The decision and the reasoning behind it
- Alternatives that were genuinely considered
- Relevant evidence
- `templates/strategy/DECISION_BRIEF.md` where analysis preceded it

## 5. Procedure

1. **Confirm significance** against §2. If uncertain, log it — a short
   unnecessary entry costs less than a missing one.

2. **Assign the next `D-###`.** Sequential, never reused.

3. **Record the decision** in `DECISIONS.md` with: date, decision stated in
   one sentence, context, alternatives considered, reasoning, consequences
   and what it governs, owner, status, and confidence.

4. **State alternatives honestly.** "No alternatives considered" is a valid
   and useful entry. Inventing rejected options to appear rigorous corrupts
   the record.

5. **Set the status** — `Confirmed` (founder-approved, binding) or
   `Provisional` (working direction). Only the founder sets `Confirmed`.

6. **Run the downstream impact pass** (`governance/CHANGE_MANAGEMENT.md` §3):
   identify documents the decision affects and correct them in the same change.

7. **Close related register entries.** If the decision answers an open
   question, move it to Resolved in `OPEN_QUESTIONS.md` with the decision ID.
   If it confirms an assumption, retire it in `ASSUMPTIONS.md`.

8. **Never delete a superseded decision.** Mark it `Superseded`, name the
   decision replacing it, and keep the history.

## 6. Outputs

- New `D-###` entry in `DECISIONS.md`
- Downstream documents corrected
- Related register entries closed
- Prior decision marked `Superseded` where applicable

## 7. Quality Checks

- [ ] Decision is stated in one unambiguous sentence.
- [ ] Reasoning would be intelligible in a year to someone who was not present.
- [ ] Alternatives are honestly recorded.
- [ ] Status and confidence are set.
- [ ] Downstream impact pass completed.
- [ ] Superseded decisions are marked, not deleted.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Decision made but never logged | Log it retroactively with the actual date and note the delay |
| Reasoning too thin to interpret later | Expand while it is still recallable |
| Two decisions conflict | Resolve per `governance/AUTHORITY.md` §8; mark the superseded one |
| Register becoming noise | Tighten §2; move routine entries to project logs |
| Agent recorded a decision as `Confirmed` | Revert to `Provisional`; only the founder confirms |

## 9. Escalation

Every entry with status `Confirmed` requires founder approval. Escalate when a
decision would change strategy, positioning, pricing, authority boundaries, or
anything reserved under `governance/AUTHORITY.md` §7.

## 10. Automation Potential

**Can be assisted:** drafting entries from a decision brief, assigning IDs,
identifying downstream documents, detecting register entries that a decision
should close.

**Must not be automated:** the decision itself, and setting status to
`Confirmed`.
