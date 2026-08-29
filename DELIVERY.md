# DELIVERY.md
# THE MILBOURNE GROUP
## CLIENT DELIVERY SOURCE OF TRUTH

**System:** Delivery
**Purpose:** Deliver high-quality work predictably, with controlled scope, clear ownership, verification, and documentation.
**Authority:** Tier 3. Authoritative for the delivery lifecycle, quality gates, and scope control. This is the single source of truth for delivery phases.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Every client engagement.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Change to the lifecycle, quality gates, or handoff standard; recurring delivery failure.
**Related:** `WEB_STANDARDS.md`, `sops/delivery/`, `templates/delivery/PROJECT_BRIEF.md`, `clients/_CLIENT_TEMPLATE/`

---


## 1. Purpose
Deliver high-quality work predictably, with controlled scope, clear ownership, verification, and documentation.

## 2. Delivery Lifecycle

This is the **single** definition of the delivery lifecycle. The parallel
nine-phase sequence formerly held in `MASTER.md` §14 has been merged here;
that duplication meant two documents defined delivery differently (one
starting at Discovery, one at Onboarding).

Not every engagement requires every phase. Do not skip critical reasoning
merely to compress a project — and record in the project brief which phases
were omitted and why.

| # | Phase | Establishes |
|---|---|---|
| 1 | Onboarding | Agreement, scope, stakeholders, access, communication, approvals |
| 2 | Discovery | Business, customers, goals, problems, existing systems, constraints |
| 3 | Strategy | Objectives, audience, positioning, user journeys, conversion strategy |
| 4 | Architecture | Sitemap, page hierarchy, content structure, functional requirements |
| 5 | Content | Messaging, headlines, body content, calls to action, trust elements |
| 6 | Design | Wireframes, visual direction, UI systems, responsive states |
| 7 | Development | Frontend, backend where required, integrations, CMS, forms, analytics |
| 8 | Quality Assurance | Requirements, functionality, responsive behaviour, accessibility, performance, integrations, failure conditions |
| 9 | Launch | Deployment, configuration, analytics, monitoring, backup, launch verification |
| 10 | Measurement & Optimization | Traffic, conversion, search visibility, user behaviour, performance, business outcomes |

Craft standards for phases 3–8 are in `WEB_STANDARDS.md`. Procedures:

| Phase | Procedure |
|---|---|
| 1 Onboarding | `sops/delivery/ONBOARDING.md` |
| 8 QA | `sops/delivery/QA.md` |
| 9 Launch | `sops/delivery/LAUNCH.md` |
| 10 Closure | `sops/delivery/CLOSURE.md` |
| Any phase — scope change | `sops/delivery/SCOPE_CHANGE.md` |

## 3. Onboarding
Confirm:
- Agreement
- Scope
- Stakeholders
- Communication channels
- Access requirements
- Timeline assumptions
- Approval process
- Risks

## 4. Discovery
Understand business context, users, objectives, existing systems, constraints, and success indicators.

## 5. Scope Control

Any material change in objectives, deliverables, integrations, or assumptions
must be evaluated **before** implementation, and a Material or Directional
change requires a written change order with client approval.

Procedure: `sops/delivery/SCOPE_CHANGE.md`, which defines the change classes,
the impact assessment, and the approval routing.

## 6. Quality Gates

Before progressing, confirm the phase outputs are acceptable — against a
standard, by a named party.

| Phase | Verified against | Confirmed by |
|---|---|---|
| Onboarding | Agreement and `PROJECT_BRIEF.md` | Founder |
| Discovery | Client playback confirmation | Client, then founder |
| Strategy / Architecture | Discovery findings and traceability | Founder |
| Content / Design | `WEB_STANDARDS.md` §2–§3, brand | Founder, then client approver |
| Development | `WEB_STANDARDS.md` §4, requirements | Founder |
| QA | Acceptance criteria, `WEB_STANDARDS.md` | QA verifies; **founder accepts** |
| Launch | `sops/delivery/LAUNCH.md` checklist | Founder authorizes |
| Closure | Acceptance criteria | Client accepts in writing |

**QA verifies; the founder accepts.** These are distinct acts and must not be
performed as one (`agents/README.md` §4). Where a phase has no named client
approver, that is an onboarding defect (`sops/delivery/ONBOARDING.md` §5.4).

## 7. Client Communication
Communicate:
- Progress
- Decisions required
- Dependencies
- Risks
- Material changes

Do not hide blockers.

## 8. QA and Launch
Verify requirements appropriate to the project, including functionality, responsive behavior, accessibility, integrations, performance, and failure conditions.

## 9. Post-Launch and Closure

Confirm launch status, monitoring, ownership, known limitations, and next
optimization opportunities.

Closing an engagement — acceptance, handover, measurement baseline, access
revocation, retrospective, and expansion review — follows
`sops/delivery/CLOSURE.md`. An engagement is not complete when the work ships;
it is complete when it has been accepted, measured, secured, and reviewed.

## 10. Escalation

Escalate to the founder immediately, without waiting for a status cycle, when:

- Scope has materially changed and work would proceed outside the agreement
- A deadline or commitment is at risk
- A quality gate cannot be passed
- A security, legal, or confidentiality concern arises (absolute constraint — stop work)
- The client requests something the company cannot responsibly deliver
- An assumption the project depends on turns out to be wrong

Escalating early is correct. Discovering a problem at launch is not.

## 11. Retrospective

For meaningful projects, record what should be reused, improved, automated, or
avoided — as part of `sops/delivery/CLOSURE.md` §5.9. Where a retrospective reveals a defect in a company document, raise a
change proposal under `governance/CHANGE_MANAGEMENT.md` — do not edit company
documents from inside a project (`governance/AUTHORITY.md` §5).
