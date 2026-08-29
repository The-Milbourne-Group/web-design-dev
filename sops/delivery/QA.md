# SOP: PROJECT QA

**System:** Delivery
**Purpose:** Verify a deliverable against its requirements and the company's craft standards before it reaches the client or production.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `DELIVERY.md` §8, `WEB_STANDARDS.md`
**Applies to:** Every client deliverable before client review or launch.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Defect reaching a client; accessibility or performance standard change.
**Related:** `WEB_STANDARDS.md`, `sops/delivery/LAUNCH.md`, `agents/QA_AGENT.md`

---

## 1. Purpose

Find defects before the client does, and produce an honest record of what was
verified and what was not.

`MASTER.md` §9.3 governs this SOP absolutely: never record a check as
performed when it was not.

## 2. Trigger

A deliverable is considered complete by the person who produced it, or a phase
quality gate is reached (`DELIVERY.md` §6).

## 3. Owner

Founder holds final QA accountability (D-010). An agent may execute checks and
report findings; it may not declare a deliverable acceptable.

## 4. Inputs

- The deliverable and its environment
- Project brief, requirements, and acceptance criteria
- `WEB_STANDARDS.md` — the craft standard being verified against
- Any prior defect list

## 5. Procedure

1. **Review requirements.** List what the deliverable must do, from the brief
   and acceptance criteria. Verifying against impressions rather than
   requirements is how requirements get quietly dropped.

2. **Verify functionality.** Every interactive element, form, link, and flow.
   Include failure paths: invalid input, empty states, network failure,
   submission errors.

3. **Verify responsive behaviour** at small, medium, and large viewports —
   layout, readability, and interaction (`WEB_STANDARDS.md` §3.2).

4. **Verify accessibility** against the WCAG 2.1 AA baseline
   (`WEB_STANDARDS.md` §3.1): keyboard navigation, visible focus, text
   alternatives, contrast, form labelling, heading order, reduced motion.

5. **Verify integrations** — forms, analytics, CMS, third-party services —
   end to end. Confirm data arrives at its destination, not merely that the
   request was sent.

6. **Verify performance** against `WEB_STANDARDS.md` §5 and record baseline
   measurements so future regression is detectable.

7. **Review security surface**: exposed credentials, unintended public
   endpoints, form validation, dependency risk (`SECURITY.md`).

8. **Assess regression risk.** What did this change touch that previously
   worked? Verify those areas.

9. **Record every defect** with severity, reproduction steps, and expected
   versus actual behaviour.

10. **Record what was NOT verified** and why. This section is mandatory. A QA
    report without it implies complete coverage and is dishonest.

## 6. Outputs

- Defect list with severity and reproduction steps
- Explicit verification record: checked, passed, failed, **not checked**
- Performance baseline
- Pass / fail recommendation to the founder

**Severity:** *Blocker* — cannot launch · *Major* — significant impairment ·
*Minor* — noticeable, not impairing · *Cosmetic* — polish.

## 7. Quality Checks

- [ ] Every requirement was explicitly checked or explicitly recorded as not
      checked.
- [ ] No check is recorded as performed when it was not.
- [ ] Defects include reproduction steps a third party could follow.
- [ ] Failure paths were tested, not only success paths.
- [ ] The "not verified" section is populated.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Blocker found | Deliverable does not proceed; return to development |
| Verification claimed but not performed | Re-run QA in full; treat the whole report as unreliable |
| Requirements unclear | Escalate rather than guessing intent |
| Defect cannot be reproduced | Record conditions observed; do not close as "works for me" |
| Time pressure to skip checks | Reduce **scope** of checking and record what was skipped — never record a skipped check as passed |

## 9. Escalation

Escalate when: a Blocker cannot be resolved in the timeline; a requirement is
ambiguous; the accessibility baseline cannot be met; a security issue is found
(stop work — absolute constraint under `MASTER.md` §7); or the deliverable does
not meet acceptance criteria and the client expects delivery.

## 10. Automation Potential

**Can be assisted:** link checking, automated accessibility scanning,
performance measurement, responsive screenshots, regression suites, defect
report drafting.

**Must not be fully automated:** the accept/reject judgement, usability
assessment, and whether the deliverable actually solves the client's problem.
Automated accessibility tools detect a minority of real issues —
`WEB_STANDARDS.md` §3.1 requires manual keyboard and screen-reader
verification regardless of scan results.
