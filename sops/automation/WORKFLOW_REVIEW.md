# SOP: AUTOMATION REVIEW

**System:** Automation
**Purpose:** Evaluate whether an existing automation still creates more leverage than burden, and whether its controls remain adequate.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `AUTOMATION.md` §8
**Applies to:** Every material automation, on a defined cadence and after any failure.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Automation failure; autonomy level change; quarterly review.
**Related:** `AUTOMATION.md`, `templates/automation/AUTOMATION_SPEC.md`, `SECURITY.md`

---

## 1. Purpose

Automation decays. Upstream systems change, assumptions expire, and an
automation that once saved time starts producing silent errors. This review
catches that, and removes automation that no longer earns its complexity.

## 2. Trigger

Quarterly for every material automation; immediately after any failure; before
any increase in autonomy level; or when the underlying process changes.

## 3. Owner

Founder. Autonomy level changes are founder decisions
(`MASTER.md` §11).

## 4. Inputs

- The automation's specification (`templates/automation/AUTOMATION_SPEC.md`)
- Execution logs and failure history since last review
- The current state of the process it automates
- `AUTOMATION.md` §3 autonomy levels

## 5. Procedure

1. **Confirm the specification is current.** Verify the documented trigger,
   inputs, process, outputs, success criteria, failure conditions, recovery,
   monitoring, permissions, and owner still describe reality. A specification
   that has drifted from behaviour is worse than none.

2. **Verify the underlying process is still defined and stable.** If it has
   changed, the automation may be reliably executing an obsolete process —
   the most dangerous failure mode, because it produces no errors.

3. **Review failure history**: how often it failed, whether failures were
   detected automatically or noticed by a human, how long recovery took, and
   whether any failure was silent.

4. **Test failure handling deliberately.** Confirm failures are visible and
   recoverable (`AUTOMATION.md` §7). An automation whose failure mode has never
   been tested has an unknown failure mode.

5. **Verify permissions** remain minimum-necessary (`SECURITY.md` §5). Access
   granted for a superseded purpose is revoked.

6. **Confirm the autonomy level is still appropriate.** Increasing it requires
   founder authorization and monitoring proportional to consequence. Decreasing
   it is always permitted and requires no approval.

7. **Measure value**: time saved, failure rate, recovery time, cost,
   complexity, and business value (`AUTOMATION.md` §8). Estimates are
   acceptable; label them as estimates (`METRICS.md` §8).

8. **Decide** — keep as is, improve, reduce autonomy, or **remove**. Removal
   is a legitimate and frequently correct outcome.

9. **Record the review and any decision** in the specification, and in
   `DECISIONS.md` where autonomy or removal changed.

## 6. Outputs

- Updated automation specification
- Failure and value summary
- Decision: keep / improve / reduce autonomy / remove
- Permissions verified or revoked
- Register entries where applicable

## 7. Quality Checks

- [ ] Specification matches actual behaviour.
- [ ] The underlying process is still stable and defined.
- [ ] Failure handling was tested, not assumed.
- [ ] No silent failures in the review period.
- [ ] Permissions are minimum-necessary.
- [ ] Value measurement distinguishes measured from estimated.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Automation failing silently | Reduce autonomy immediately; add monitoring before restoring |
| Automating a process that has changed | Suspend; re-define the process; re-specify before resuming |
| Creating more burden than leverage | Remove it — `AUTOMATION.md` §8 |
| Permissions broader than required | Revoke now; record under `SECURITY.md` |
| Specification drifted from behaviour | Rewrite from observed behaviour, then reconcile with intent |
| No monitoring exists | Reduce to Level 2 (human-approved) until monitoring is added |

## 9. Escalation

Escalate when: an automation has taken a consequential action outside its
boundaries; a failure affected a client; permissions exceed authorization; a
security concern is found (stop the automation — absolute constraint under
`MASTER.md` §7); or an autonomy increase is proposed.

## 10. Automation Potential

**Can be assisted:** log collection, failure-rate calculation, permission
audits, flagging automations overdue for review.

**Must not be automated:** the keep/remove decision, autonomy level changes,
and judging whether the underlying process is still valid.
