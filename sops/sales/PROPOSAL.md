# SOP: PROPOSAL

**System:** Sales
**Purpose:** Convert an approved solution design into a proposal that can be issued without stating anything the company has not decided, and record what was proposed and what happened to it.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `SALES.md` §6 and §7, `SERVICES.md` §4
**Applies to:** Every opportunity between solution design and agreement.
**Owner:** Founder
**Status:** Active — issuance blocked by Q-007 and Q-011 (§9).
**Last reviewed:** 2026-08-29
**Review trigger:** Pricing configuration (Q-007); package configuration (Q-011); recurring loss pattern; scope disputes traced to the proposal.
**Related:** `sops/sales/SOLUTION_DESIGN.md`, `templates/sales/PROPOSAL_OUTLINE.md`, `sops/delivery/ONBOARDING.md`, `SALES.md`, `SERVICES.md`

---

## 1. Purpose

The proposal is the company's only binding client-facing commercial document.
It is where an open value becomes a commitment, and it is the scope baseline
every later dispute is measured against.

Three things previously had no procedure: assembling the proposal from the
solution design without adding scope, checking it against values the founder
has not decided, and recording what was issued and how it resolved. This SOP
does those three things. It sets no commercial policy — `SALES.md` §6 and §7
and `SERVICES.md` §4 do that.

**The proposal is also the record of what was sold.** `sops/delivery/ONBOARDING.md`
§5.3 reconciles the project brief against it, and `sops/delivery/SCOPE_CHANGE.md`
§8 resolves "this was always in scope" against it. Neither works if the
proposal exists only in the founder's sent mail.

## 2. Trigger

`clients/<client>/SOLUTION.md` is complete and the founder has approved the
recommended scope (`sops/sales/SOLUTION_DESIGN.md` §6).

## 3. Owner

Founder. Issuing a proposal is a client-facing commercial commitment and is
reserved to the founder (`governance/AUTHORITY.md` §7). An agent drafts; only
the founder approves and sends.

## 4. Inputs

- `clients/<client>/SOLUTION.md` — traceability matrix, minimum viable scope,
  deferred items, open dependencies
- `clients/<client>/DISCOVERY.md` — the client's own words
- `SALES.md` §6 (commercial constraints) and §7 (proposal standard)
- `SERVICES.md` §4 (offer definition standard) and §2 (progression)
- `OPEN_QUESTIONS.md` — **mandatory**; Q-007 and Q-011 gate issuance
- `templates/sales/PROPOSAL_OUTLINE.md`

## 5. Procedure

1. **Run the issuance gate before drafting.** `SERVICES.md` §4 requires a
   pricing model and defined deliverables before an offer is presented
   commercially. Both are open (Q-007, Q-011). Confirm with the founder that
   the commercial terms for *this* engagement have been decided and recorded.
   If they have not, **stop and escalate (§9)** — do not draft a proposal
   around a gap and do not write a figure to fill it.

2. **Carry the scope across unchanged.** Every deliverable in the proposal
   comes from the minimum viable scope in `SOLUTION.md` §3. Adding anything
   here defeats the traceability control that `SOLUTION.md` exists to enforce
   (`sops/sales/SOLUTION_DESIGN.md` §5.2).

3. **Carry the exclusions across.** The deferred items in `SOLUTION.md` §4
   become the proposal's exclusions. An unstated exclusion becomes an assumed
   inclusion.

4. **Label every assumed requirement as assumed.** Requirements typed
   *Assumed* in the traceability matrix are presented as assumptions the client
   must confirm, never as established needs (`MASTER.md` §8.2).

5. **Draft from `templates/sales/PROPOSAL_OUTLINE.md`**, covering the eleven
   elements of `SALES.md` §7. Mark the draft **DRAFT — FOR FOUNDER REVIEW**.

6. **Check it against the commercial constraints** in `SALES.md` §6: no price
   unless the founder has decided it, no undefined deliverable, no outcome
   guarantee, forecasts labelled as estimates, and the engagement located in
   one stage of the progression (`SERVICES.md` §2).

7. **Record the proposal** in `clients/<client>/PROPOSAL.md`: what was
   proposed, the scope and exclusions as issued, the assumptions the client is
   being asked to confirm, and the commercial terms as stated. Set
   `Status: Proposal`.

8. **Founder reviews, approves, and sends.** Record the issue date and the
   version issued. What the client received is what onboarding will reconcile
   against — if it is not written down, it did not happen.

9. **Record the outcome** when it resolves, with reasoning:

   | Outcome | Status | Next |
   |---|---|---|
   | **Accepted** | `Onboarding` | `sops/delivery/ONBOARDING.md` |
   | **Negotiated** | `Proposal` | Re-run §2–§8 for the revised scope; record what changed and why |
   | **Declined** | `Lost` | Record the reason (§5.10) |
   | **No decision** | `Nurture` | Record the revisit trigger |

10. **Capture loss reasoning.** For a declined or stalled proposal record what
    the client actually objected to — scope, price, timing, trust, a competitor,
    or no decision — and complete the Buyer Evidence table in
    `clients/<client>/README.md`. Lost proposals are the strongest available
    evidence for Q-001 and Q-003 (`ICP.md` §7), for the same reason
    disqualifications are (D-015). A loss recorded only as "lost" teaches the
    company nothing.

## 6. Outputs

**Location:** `clients/<client>/PROPOSAL.md`.

- The proposal as issued, with scope, exclusions, and assumptions
- Issue date and version
- Founder approval recorded
- Outcome with reasoning
- Buyer evidence completed in the directory `README.md`
- `Status` set per §5.9

## 7. Quality Checks

- [ ] The issuance gate (§5.1) was run and passed, or the proposal was not
      issued.
- [ ] No price, package content, timeline guarantee, or deliverable appears
      that the founder has not decided (`SALES.md` §6, Q-007, Q-011).
- [ ] Every deliverable traces to `SOLUTION.md` §3 — nothing was added.
- [ ] Deferred items appear as exclusions.
- [ ] Assumed requirements are labelled as assumptions.
- [ ] All eleven elements of `SALES.md` §7 are present.
- [ ] No placeholder from the template survives — an unfilled field is a
      defect (`templates/README.md`, Rules).
- [ ] The issued version is recorded in the client directory, not only sent.
- [ ] Outcome and reasoning recorded; buyer evidence captured.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| A price was stated that the founder had not decided | Correct in writing immediately and escalate — the company has made a commitment it did not authorize (`SALES.md` §6) |
| Scope in the proposal exceeds `SOLUTION.md` §3 | Remove it, or return to solution design; unsourced scope is the failure `sops/sales/SOLUTION_DESIGN.md` exists to prevent |
| Proposal issued but never filed | File it from the sent copy now; onboarding and scope change both depend on it |
| Client treats an assumption as a commitment | Return to the labelled assumption in writing; if it must hold, it is a scope change, not a clarification |
| Proposal lost with no reason recorded | Ask; a lost opportunity that teaches nothing has cost twice |
| Negotiation quietly changed the scope | Re-issue and re-file; the last issued version is the baseline, and an unrecorded revision breaks onboarding reconciliation |
| Package contents invented to complete the document | Stop — Q-011 is open (`SERVICES.md` §7) |

## 9. Escalation

**Standing escalation — issuance is currently blocked.** `SERVICES.md` §4
requires a pricing model and defined deliverables before an offer is presented
commercially; Q-007 (Blocking) and Q-011 (High) leave both open. Until the
founder decides them, no proposal can be issued that satisfies `SERVICES.md`
§4, and every proposal is a founder escalation rather than a procedure an
agent completes. This is a real constraint on the commercial chain, not a
documentation gap — recorded in `RISKS.md` R-003.

Also escalate when: the client requests terms outside what was approved; the
minimum viable scope exceeds what the client can invest; the client asks for a
guarantee; the engagement fits no stage of the progression (`SERVICES.md` §2);
or negotiation would move the engagement into a different stage.

## 10. Automation Potential

**Can be assisted:** assembling the draft from `SOLUTION.md`, checking every
deliverable against the traceability matrix, detecting unfilled placeholders,
detecting figures where an open value should read "to be determined",
verifying the eleven elements of `SALES.md` §7 are present, and drafting the
outcome record. The scope-versus-matrix check is mechanical and catches the
failure mode this SOP exists to prevent.

**Must not be automated:** the issuance decision, any commercial term, sending
the proposal, and negotiating it. All are founder decisions
(`governance/AUTHORITY.md` §7).
