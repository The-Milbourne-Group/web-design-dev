# CHANGE MANAGEMENT

**System:** Governance
**Purpose:** Define how knowledge in this system is changed, who may change it, what review a change requires, and how downstream documents are kept consistent.
**Authority:** Tier 3 governance. Derived from `MASTER.md` §6.7 and §15.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Every change to any document in this repository.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Process proving too heavy or too weak; any drift incident.
**Related:** `governance/DOCUMENT_REGISTRY.md`, `governance/SYSTEM_QA.md`, `DECISIONS.md`, `sops/operations/DOCUMENTATION.md`

---

## 1. Principle

Documentation drift — a domain document changing while its SOPs, agents, and
templates continue describing the old policy — is how this system accumulated
four competing precedence statements. The cure is not heavy process. It is a
**downstream-impact pass** on every substantive change.

Routine edits must stay frictionless, or operators will bypass the system
entirely (`RISKS.md` R-009).

---

## 2. Change Classes

| Class | Examples | Approval | Downstream pass |
|---|---|---|---|
| **Editorial** | Typos, formatting, broken links, clarifying wording without changing meaning, correcting a document to match a higher tier | None — just do it | No |
| **Operational** | New SOP step, template field, agent quality standard, register entry | Operator decides | Check that SOP's parent domain doc |
| **Substantive** | Changing what a Tier 3 domain document asserts | Founder approves | **Required** |
| **Strategic** | Changing `MASTER.md`, `STRATEGIC_CONFIGURATION.md`, `governance/AUTHORITY.md`, or a `Confirmed` decision | Founder approves explicitly; `DECISIONS.md` entry required | **Required, full sweep** |

**When unsure of the class, treat it as one level higher.**

Adding a fact to a register (`DECISIONS.md`, `OPEN_QUESTIONS.md`,
`ASSUMPTIONS.md`, `RISKS.md`) is Operational. Changing a decision's **status**
from `Open` to `Confirmed` is Strategic — only the founder may do it.

---

## 3. The Downstream Impact Pass

Required for Substantive and Strategic changes. Four steps:

1. **Identify dependents.** Look up the changed document in
   `governance/DOCUMENT_REGISTRY.md` and read its "Depended on by" column.
2. **Read each dependent** for statements that the change makes false.
3. **Correct them in the same change.** A change that leaves a dependent
   contradicting it is not finished.
4. **Search for stragglers.** Grep the repository for the old terminology,
   the old value, and the document name. Cross-references are missed far more
   often than direct contradictions.

**Worked example.** Changing the entry offer in `SERVICES.md` requires
checking `BUSINESS.md` §9, `SALES.md` §6, `MARKETING.md`,
`templates/sales/PROPOSAL_OUTLINE.md`, `agents/SALES_AGENT.md`,
`sops/sales/QUALIFICATION.md`, and any open questions that reference it.

---

## 4. Proposing a Change You Cannot Approve

Agents and project work frequently discover that a company document is wrong.
The correct response is never to edit it in place (`governance/AUTHORITY.md`
§6).

Instead:

1. **State the defect** — document, section, and the exact statement.
2. **State the evidence** — what was observed, where, and when.
3. **State the impact** — what breaks if it stays, and who is affected.
4. **Propose the correction** — specific replacement wording, not "improve
   this."
5. **List downstream documents** the correction would touch.
6. **Route it:** a strategic gap goes to `OPEN_QUESTIONS.md`; an unconfirmed
   premise goes to `ASSUMPTIONS.md`; a threat goes to `RISKS.md`; a decision
   ready to be made goes to the founder using
   `templates/strategy/DECISION_BRIEF.md`.

Then continue the work under the current documented policy. Do not stall, and
do not act on the proposed policy before it is approved.

---

## 5. Promoting Assumptions to Facts

An assumption becomes a company fact only when the founder confirms it.

1. The assumption is recorded in `ASSUMPTIONS.md` with its basis and
   consequence-if-wrong.
2. Evidence accumulates, or the founder decides.
3. The founder confirms it.
4. A `DECISIONS.md` entry is created with status `Confirmed`.
5. The assumption moves to the Retired section of `ASSUMPTIONS.md`, noting the
   decision ID.
6. Downstream impact pass — including removing any hedging language that
   existed only because the item was uncertain.

Time does not promote an assumption. An assumption repeated often enough is
still an assumption.

---

## 6. Answering an Open Question

1. The founder decides.
2. Record it in `DECISIONS.md` with context, alternatives, reasoning, and
   consequences.
3. Move the question to the Resolved section of `OPEN_QUESTIONS.md` with the
   decision ID.
4. Downstream impact pass — every document that said "open," "to be
   determined," or "not yet configured" for that item must now state the
   decision.
5. Check whether the answer unblocks a dependent question.

Step 4 is the one most often skipped, and it is the one that keeps confirmed
decisions from reaching the operators who need them.

---

## 7. Retiring a Document

Do not delete a document that others reference. Instead:

1. Set its status to `Deprecated` with the date and the reason.
2. Name the document that supersedes it.
3. Update every reference to point to the successor.
4. Update `governance/DOCUMENT_REGISTRY.md`.
5. Remove the file only once nothing references it.

A deleted document leaves broken references; a deprecated one explains
itself.

---

## 8. Conflicting Instructions Discovered Mid-Work

1. Resolve for the immediate task using `governance/AUTHORITY.md` §8.
2. Record the conflict — do not rely on memory.
3. Correct the defective document, or propose the correction under §4 if it is
   above your authority.

A conflict resolved in conversation but left on disk will recur, with a
different operator reaching the opposite conclusion.

---

## 9. Review Cadence

| Cadence | Review |
|---|---|
| Per change | Downstream impact pass (Substantive and Strategic) |
| Monthly | New entries in all four registers |
| Quarterly | `RISKS.md`, `ASSUMPTIONS.md`, stale `Last reviewed` dates, `governance/SYSTEM_QA.md` full pass |
| Annually | Whole-system architecture review |
