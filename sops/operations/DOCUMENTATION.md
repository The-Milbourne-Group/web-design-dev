# SOP: DOCUMENTATION UPDATE

**System:** Operations
**Purpose:** Keep the operating system accurate after work changes something material.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), §6.7; `governance/CHANGE_MANAGEMENT.md`
**Applies to:** Any work that changes a process, architecture, decision, or limitation.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Documentation drift found; process too heavy or too light.
**Related:** `governance/CHANGE_MANAGEMENT.md`, `governance/DOCUMENT_REGISTRY.md`, `governance/SYSTEM_QA.md`

---

## 1. Purpose

Update the authoritative source rather than creating a competing copy. This
system already demonstrated the cost of the alternative: one subject
(precedence) documented in four places produced four different answers.

## 2. Trigger

Work changed a material process, architecture, decision, requirement,
automation behaviour, or known limitation — or a document was found to be
wrong.

## 3. Owner

The operator who did the work drafts. The founder approves changes to
`MASTER.md` and Tier 2–3 documents.

## 4. Inputs

- What changed, and what is now true
- `governance/DOCUMENT_REGISTRY.md` for subject ownership and dependents
- `governance/CHANGE_MANAGEMENT.md` for change class

## 5. Procedure

1. **Identify the authoritative document** for the subject using
   `governance/DOCUMENT_REGISTRY.md`. If two documents appear to own it, that
   is itself a defect — record it.

2. **Classify the change** using `governance/CHANGE_MANAGEMENT.md` §2. When
   uncertain, treat it as one class higher.

3. **Check authority.** If the change is above your authority, stop and write
   a change proposal (`governance/CHANGE_MANAGEMENT.md` §4). Do not edit the
   document and seek approval afterward.

4. **Update the authoritative document.** Edit in place. Never append a
   correction that leaves the original error present, and never create a
   parallel "updated" file.

5. **Run the downstream impact pass** for Substantive and Strategic changes
   (`governance/CHANGE_MANAGEMENT.md` §3), including a repository search for
   old terminology and stale cross-references.

6. **Update metadata** — `Last reviewed`, and `Status` if it changed.

7. **Record it** where the change reflects a decision
   (`sops/operations/DECISION_LOG.md`), an unconfirmed premise
   (`ASSUMPTIONS.md`), or a new threat (`RISKS.md`).

8. **Run the Fast Check** in `governance/SYSTEM_QA.md` §3 before declaring the
   work complete.

## 6. Outputs

- Authoritative document updated in place
- Dependent documents corrected
- Metadata refreshed
- Register entries created where applicable

## 7. Quality Checks

- [ ] The authoritative document was updated, not a copy.
- [ ] No competing version of the subject now exists.
- [ ] Dependents listed in the registry were checked.
- [ ] Cross-references still resolve.
- [ ] `Last reviewed` updated.
- [ ] Changes above my authority were proposed, not applied.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Documentation not updated after material change | Update now; the gap between reality and documentation is where errors originate |
| A competing copy was created | Consolidate into the authoritative document; delete or deprecate the copy |
| Change applied above authority | Revert; submit as a proposal |
| Downstream documents now contradict | Complete the impact pass; the change is not finished |
| Update made the document longer without making it clearer | Prefer replacing over appending |

## 9. Escalation

Escalate before editing when the change would alter `MASTER.md`,
`STRATEGIC_CONFIGURATION.md`, `governance/AUTHORITY.md`, a `Confirmed`
decision, or the substance of any Tier 3 document.

## 10. Automation Potential

**Can be assisted:** detecting broken references, finding stale terminology,
identifying dependents, flagging overdue review dates, drafting proposals.
The checks in `governance/SYSTEM_QA.md` §4.1 are scriptable and should run
routinely.

**Must not be automated:** editing `MASTER.md` or Tier 2–3 documents without
review, and judging whether a change is Editorial or Substantive.
