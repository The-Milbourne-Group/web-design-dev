# SOP INDEX

**System:** Operations
**Purpose:** Catalogue every standard operating procedure, define the SOP structure standard, and route work to the correct procedure.
**Authority:** Tier 3. Authoritative for the SOP catalogue and the SOP structure standard.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme)
**Applies to:** Anyone executing or writing a procedure.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** SOP created, retired, or restructured.
**Related:** `sops/`, `governance/CHANGE_MANAGEMENT.md`, `agents/README.md`

---

## 1. Routing

| If you are… | Use |
|---|---|
| Assessing a new prospect or inbound inquiry | `sops/sales/QUALIFICATION.md` |
| Preparing for or running a discovery conversation | `sops/sales/DISCOVERY.md` |
| Turning discovery findings into a scope | `sops/sales/SOLUTION_DESIGN.md` |
| Producing, issuing, or recording the outcome of a proposal | `sops/sales/PROPOSAL.md` |
| Starting a signed engagement | `sops/delivery/ONBOARDING.md` |
| Handling a mid-project change request | `sops/delivery/SCOPE_CHANGE.md` |
| Verifying work before launch | `sops/delivery/QA.md` |
| Taking a project live | `sops/delivery/LAUNCH.md` |
| Closing out an engagement | `sops/delivery/CLOSURE.md` |
| Recording a significant decision | `sops/operations/DECISION_LOG.md` |
| Updating documentation after work | `sops/operations/DOCUMENTATION.md` |
| Reviewing an existing automation | `sops/automation/WORKFLOW_REVIEW.md` |

## 2. Catalogue

| SOP | Domain | Governed by | Owner | Last reviewed |
|---|---|---|---|---|
| `sops/sales/QUALIFICATION.md` | Sales | `SALES.md`, `ICP.md` | Founder | 2026-08-29 |
| `sops/sales/DISCOVERY.md` | Sales | `SALES.md` | Founder | 2026-08-29 |
| `sops/sales/SOLUTION_DESIGN.md` | Sales | `SALES.md` §5, `SERVICES.md` | Founder | 2026-08-29 |
| `sops/sales/PROPOSAL.md` | Sales | `SALES.md` §6–§7, `SERVICES.md` §4 | Founder | 2026-08-29 |
| `sops/delivery/ONBOARDING.md` | Delivery | `DELIVERY.md` | Founder | 2026-08-29 |
| `sops/delivery/SCOPE_CHANGE.md` | Delivery | `DELIVERY.md`, `SERVICES.md` | Founder | 2026-08-29 |
| `sops/delivery/QA.md` | Delivery | `DELIVERY.md`, `WEB_STANDARDS.md` | Founder | 2026-08-29 |
| `sops/delivery/LAUNCH.md` | Delivery | `DELIVERY.md` | Founder | 2026-08-29 |
| `sops/delivery/CLOSURE.md` | Delivery | `DELIVERY.md` §9, §11 | Founder | 2026-08-29 |
| `sops/operations/DECISION_LOG.md` | Operations | `MASTER.md` | Founder | 2026-08-29 |
| `sops/operations/DOCUMENTATION.md` | Operations | `governance/CHANGE_MANAGEMENT.md` | Founder | 2026-08-29 |
| `sops/automation/WORKFLOW_REVIEW.md` | Automation | `AUTOMATION.md` | Founder | 2026-08-29 |

## 3. SOP Structure Standard

Every SOP must contain all ten sections below. This is the **single**
definition of the standard; it previously existed in two places
(the former `MASTER.md` §15.2 and `sops/README.md`) with different element lists.

| # | Section | Must answer |
|---|---|---|
| 1 | Purpose | What outcome does this produce? |
| 2 | Trigger | What starts it? |
| 3 | Owner | Who is accountable? |
| 4 | Inputs | What is required before starting? |
| 5 | Procedure | Numbered, executable steps |
| 6 | Outputs | What artifacts exist afterward? |
| 7 | Quality Checks | How is correctness verified? |
| 8 | Failure Conditions & Recovery | What goes wrong, and what then? |
| 9 | Escalation | When does this stop and go to the founder? |
| 10 | Automation Potential | What could be automated, and what must not be? |

An SOP missing any section is defective and must not be relied upon.

## 4. Writing Rules

- **Steps must be executable.** "Understand the client" is not a step;
  "ask the six questions in §5.2 and record the answers" is.
- **Name the artifact.** Every step producing something says where it goes.
- **State the decision rule.** A decision point defines the criteria, not just
  the existence of a choice.
- **Never restate policy.** Reference the governing domain document. An SOP
  that duplicates policy will drift from it.
- **Never introduce policy.** If a procedure requires a rule that no domain
  document supports, that is a change proposal
  (`governance/CHANGE_MANAGEMENT.md` §4), not an SOP edit.
