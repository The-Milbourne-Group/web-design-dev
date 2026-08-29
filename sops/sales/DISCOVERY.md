# SOP: CLIENT DISCOVERY

**System:** Sales
**Purpose:** Understand the prospect's business well enough to design a solution that addresses the real problem.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `SALES.md`
**Applies to:** Every qualified opportunity before solution design.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Recurring solution mismatch; ICP configuration.
**Related:** `SALES.md` §4, `ICP.md` §8, `templates/sales/DISCOVERY_NOTES.md`

---

## 1. Purpose

Understand the business before prescribing a solution. `BUSINESS.md` §6 is
explicit: do not sell implementation without sufficient understanding of the
problem.

## 2. Trigger

An opportunity marked **Qualified** by `sops/sales/QUALIFICATION.md`.

## 3. Owner

Founder. Discovery is founder-led work (D-010) and is not delegated.

## 4. Inputs

- The qualification record and its reasoning
- Prospect's website, digital presence, and any public information
- `templates/sales/DISCOVERY_NOTES.md`
- `ICP.md` §8 question set

## 5. Procedure

1. **Prepare.** Review the qualification record and research the business.
   Arrive with informed questions, not a blank form.

2. **Understand current state.** What exists now? What is working? What is
   not? What has already been attempted, and why did it not hold?

3. **Establish the desired outcome.** What should be different, and how would
   they recognise it? Push past "a new website" to the business result behind
   it.

4. **Quantify the cost of inaction.** What happens if nothing changes? An
   opportunity with no cost of inaction rarely converts, regardless of stated
   interest.

5. **Map stakeholders.** Who decides, who influences, who must be convinced,
   who will be affected during delivery, and who supplies content or access.

6. **Identify constraints.** Timeline, technical, organisational, brand,
   regulatory, and capacity constraints — theirs and the company's.

7. **Define success indicators.** How will success be evaluated, by whom, and
   over what period? Record measurement feasibility: an indicator with no data
   source cannot be reported against (`METRICS.md` §2).

8. **Record assumptions and open questions** explicitly, separated from facts.

9. **Play it back and obtain correction** before any solution design. This
   step is mandatory — a misunderstanding corrected here costs a conversation;
   corrected after proposal it costs the engagement.

## 6. Outputs

**Location:** `clients/<prospect-name>/DISCOVERY.md` — the directory created at
qualification. Set `Status: Discovery`.

- Completed discovery notes (structure: `templates/sales/DISCOVERY_NOTES.md`)
- Explicit list of assumptions, labelled as assumptions
- Open questions requiring answers before proposal
- Stakeholder and decision map
- Identified risks
- Prospect's confirmation that the understanding is correct

## 7. Quality Checks

- [ ] Facts and assumptions are visibly distinguished.
- [ ] The problem is stated in the client's language, not reframed into a
      service the company happens to sell.
- [ ] Success indicators are measurable and have a data source.
- [ ] The accountable decision-maker is confirmed.
- [ ] Playback occurred and correction was obtained.
- [ ] Notes are stored in the opportunity directory, not left as session output.
- [ ] No solution was promised and no price discussed.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Solution designed before understanding | Stop; return to §5.2–§5.7 |
| Client describes a solution, not a problem | Ask what it would change for the business; work back to the problem |
| Discovery expanding into unpaid consulting | `SERVICES.md` §3 — convert to a paid engagement or close the scope |
| Key stakeholder never available | Record as a risk; an absent decision-maker predicts a stalled proposal |
| Playback reveals major misunderstanding | Correct now and re-play back; this is discovery working, not failing |

## 9. Escalation

Escalate when: the real problem is outside the company's capability; the
engagement would require a commitment the founder has not authorized; the
client's expectations cannot be responsibly met; or legal, security, or
compliance obligations appear.

## 10. Automation Potential

**Can be assisted:** pre-call research, question preparation, note structuring,
drafting the playback summary, extracting assumptions and open questions from
notes.

**Must not be automated:** the conversation itself, interpreting what the
client means, and the judgement that understanding is sufficient to proceed.
