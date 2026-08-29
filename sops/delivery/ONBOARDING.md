# SOP: CLIENT ONBOARDING

**System:** Delivery
**Purpose:** Establish everything required to deliver before substantial work begins.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `DELIVERY.md` §3
**Applies to:** Every engagement after agreement, before delivery work.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Recurring onboarding gap; access or approval failure.
**Related:** `DELIVERY.md`, `SALES.md` §9, `clients/_CLIENT_TEMPLATE/`, `SECURITY.md`

---

## 1. Purpose

Convert a signed agreement into a project that can actually be executed:
scope, stakeholders, access, communication, and approvals all established
before work starts.

## 2. Trigger

An executed agreement, or explicit founder authorization to begin.

## 3. Owner

Founder.

## 4. Inputs

- Executed agreement and approved statement of work
- Complete sales handoff (`SALES.md` §9)
- Discovery notes and confirmed success criteria
- `clients/_CLIENT_TEMPLATE/`

## 5. Procedure

1. **Initialize the client workspace.** Copy `clients/_CLIENT_TEMPLATE/` to
   `clients/<client-name>/`. This directory is the engagement's sole home
   (`governance/KNOWLEDGE_ARCHITECTURE.md` §5).

2. **Complete the project brief** (`templates/delivery/PROJECT_BRIEF.md`)
   from the agreement and discovery notes. Carry assumptions and open
   questions across rather than dropping them — they are the most common
   source of later scope disputes.

3. **Confirm scope against the agreement.** Reconcile the brief with what was
   sold, including anything promised verbally during sales. Any discrepancy is
   resolved now, in writing, not during delivery.

4. **Confirm stakeholders and approvals.** Record who approves each phase, who
   supplies content and access, and what happens when an approver is
   unavailable. Name a single accountable client contact.

5. **Establish communication.** Agree the channel, update cadence, response
   expectations, and escalation path in both directions.

6. **Obtain access** under `SECURITY.md` §5, requesting the minimum necessary
   for the work. Record in the client workspace **what** access exists and
   **where** credentials are stored — never the credential values themselves
   (`MASTER.md` §7.3).

7. **Confirm timeline assumptions**, explicitly including client-side
   dependencies. Most timeline failures originate in client content and
   approval delays, so state those dependencies now.

8. **Record risks and dependencies** in the project brief.

9. **Confirm the definition of done** — the acceptance criteria that will end
   the engagement — before starting.

10. **Hold a kickoff** confirming objective, scope, exclusions, timeline,
    responsibilities, and communication. Send a written summary.

## 6. Outputs

- `clients/<client>/` workspace initialized
- Completed project brief with acceptance criteria
- Stakeholder and approval map
- Access recorded (names and locations only)
- Confirmed timeline with client-side dependencies
- Written kickoff summary

## 7. Quality Checks

- [ ] Scope in the brief matches the agreement exactly.
- [ ] Verbal sales promises are captured in writing.
- [ ] Exclusions are stated, not merely implied.
- [ ] Every phase has a named approver.
- [ ] No credential values appear anywhere in the workspace.
- [ ] Acceptance criteria are specific enough to be verified.
- [ ] Client-side dependencies are explicit.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Work started before onboarding completed | Stop; complete §5; unbriefed work is usually rework |
| Scope in brief differs from agreement | Resolve in writing before proceeding — do not average the two |
| Access not granted | Timeline pauses; notify the client that the dependency is theirs |
| No accountable approver | Escalate; a project without an approver cannot reach acceptance |
| Client wants to skip kickoff | Send the written summary regardless; shared understanding is the deliverable, not the meeting |

## 9. Escalation

Escalate when: the agreement and expectations diverge materially; required
access cannot be granted; no accountable decision-maker exists; the client
requests work outside the agreement at kickoff; or security or compliance
obligations appear that were not identified during sales.

## 10. Automation Potential

**Can be assisted:** workspace scaffolding, populating the brief from
discovery notes, generating the access checklist, drafting the kickoff summary.

**Must not be automated:** access requests, scope confirmation, and client
communication — all founder-approved (`governance/AUTHORITY.md` §7).
