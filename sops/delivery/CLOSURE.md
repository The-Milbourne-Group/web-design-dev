# SOP: PROJECT CLOSURE

**System:** Delivery
**Purpose:** Close an engagement cleanly — accepted, documented, measured, secured, and reviewed for expansion.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `DELIVERY.md` §9 and §11
**Applies to:** Every engagement reaching launch or termination.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Engagements ending without acceptance or without expansion review.
**Related:** `sops/delivery/LAUNCH.md`, `SERVICES.md` §2, `METRICS.md`, `SECURITY.md` §5

---

## 1. Purpose

An engagement that is merely "finished" leaves value on the table and risk in
place: access stays granted, acceptance is never confirmed, no measurement
baseline exists, and the recurring relationship stage — the company's
confirmed commercial model (D-005) — never begins.

This procedure closes those four gaps.

## 2. Trigger

Launch is complete and monitoring has elapsed, **or** an engagement is
terminated early for any reason.

## 3. Owner

Founder. Acceptance and access revocation are founder decisions.

## 4. Inputs

- `clients/<client>/PROJECT_BRIEF.md` — acceptance criteria
- QA verification records (`clients/<client>/QA/`)
- Launch record (`sops/delivery/LAUNCH.md`)
- `clients/<client>/ACCESS.md`
- `clients/<client>/SOLUTION.md` — deferred items from solution design

## 5. Procedure

### Acceptance

1. **Verify acceptance criteria.** Check the deliverable against
   `PROJECT_BRIEF.md` §14, item by item. Criteria not met are either resolved
   or explicitly accepted by the client as exceptions — never quietly dropped.

2. **Obtain written client acceptance**, listing what was delivered and any
   accepted exceptions. Verbal acceptance is not acceptance.

### Handover

3. **Confirm ownership and documentation.** The client knows what they own,
   where it is hosted, how to access it, and what maintenance it needs.
   Repository documentation (`CLAUDE.md`) is current.

4. **Record known limitations** — what was not done, what was deferred, and
   what will need attention. Stating these protects the relationship; omitting
   them converts them into complaints.

### Measurement

5. **Record the measurement baseline.** Capture the success indicators defined
   in discovery (`METRICS.md` §2) at their post-launch values. Without a
   baseline, no later optimization work can demonstrate value — and
   demonstrated value is what justifies the recurring stage.

6. **Record delivery metrics** for the company: duration, rework, defects,
   and profitability where measurable (`METRICS.md` §6). This is the evidence
   base for refining pricing from actual delivery margin (D-038).

### Security

7. **Revoke access no longer required** (`SECURITY.md` §5). Update
   `ACCESS.md` with revocation dates. Access retained for an agreed
   maintenance relationship is recorded with its justification.

8. **Verify no credential values** were recorded anywhere in the client
   directory (`MASTER.md` §7.3).

### Retrospective

9. **Record the retrospective** (`DELIVERY.md` §11): what should be reused,
   improved, automated, or avoided. Where it reveals a defect in a company
   document, raise a change proposal
   (`governance/CHANGE_MANAGEMENT.md` §4) — do not edit company documents
   from inside the project.

10. **Capture buyer evidence.** Complete the Buyer Evidence table in
    `clients/<client>/README.md` — who decided, who held budget, industry,
    size. This tests the D-021 buyer roles (`ICP.md` §7).

### Expansion

11. **Review expansion opportunity.** Consult the deferred items from
    `SOLUTION.md` §4 and the commercial progression (`SERVICES.md` §2):

    - Are deferred items now worth proposing as an **Expansion** engagement?
    - Does the client need ongoing optimization, support, or managed systems
      (**Recurring**)?
    - Is there a referral opportunity?

    Record the assessment even when the answer is no. An engagement closed
    without expansion review is the single most common way a boutique services
    business loses its highest-margin revenue.

12. **Set status.** `Status: Closed` in `clients/<client>/README.md`. Retain
    the directory — it is the company's record and the basis for future
    expansion.

## 6. Outputs

- Written client acceptance with any accepted exceptions
- Handover record: ownership, access, maintenance needs, known limitations
- Measurement baseline and delivery metrics
- `ACCESS.md` updated with revocations
- Retrospective
- Buyer evidence captured
- Expansion assessment
- Status set to `Closed`

## 7. Quality Checks

- [ ] Every acceptance criterion verified, met or explicitly excepted.
- [ ] Client acceptance is in writing.
- [ ] Known limitations disclosed, not omitted (`MASTER.md` §9.2).
- [ ] Measurement baseline recorded — otherwise future value cannot be shown.
- [ ] Access revoked and `ACCESS.md` updated.
- [ ] No credential values anywhere in the directory.
- [ ] Buyer evidence captured (tests D-021).
- [ ] Expansion reviewed and recorded, including a negative result.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Client will not confirm acceptance | Determine whether a criterion is genuinely unmet; escalate — do not treat silence as acceptance |
| Acceptance criteria were never specific enough to verify | Record as a retrospective finding; the defect originated at onboarding |
| Access left granted after closure | Revoke now; this is a standing security exposure (`SECURITY.md` §5) |
| No measurement baseline captured | Capture what is still available and record the gap; optimization value becomes unprovable |
| Engagement closed with no expansion review | Perform it retroactively; the relationship is warmest at closure |
| Retrospective skipped under time pressure | The next engagement repeats the same failure — this is the step that compounds |

## 9. Escalation

Escalate when: the client disputes acceptance; criteria cannot be met; the
engagement is terminating early or unhappily; a security exposure is found —
stop and remediate (absolute constraint, `MASTER.md` §7); or expansion review
identifies an opportunity requiring a commercial decision.

## 10. Automation Potential

**Can be assisted:** acceptance criteria checklists, metric collection,
flagging access that should be revoked, drafting handover documentation and
the retrospective, surfacing deferred items for expansion review.

**Must not be automated:** acceptance, access revocation decisions, and any
client communication.
