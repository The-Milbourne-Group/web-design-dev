# SALES.md
# THE MILBOURNE GROUP
## SALES SYSTEM SOURCE OF TRUTH

**System:** Commercial
**Purpose:** Convert qualified opportunities into profitable engagements through a consistent, ethical, evidence-based process.
**Authority:** Tier 3. Authoritative for the sales process, qualification standard, and proposal requirements.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `STRATEGIC_CONFIGURATION.md` (Tier 2), `BUSINESS.md`, `SERVICES.md`, `ICP.md`, `BRAND.md`
**Applies to:** All opportunity handling from first contact to signed agreement.
**Owner:** Founder
**Status:** Active — commercial configuration confirmed (D-038).
**Last reviewed:** 2026-08-29
**Review trigger:** Pricing configuration; change to the offer set; recurring loss pattern.
**Related:** `sops/sales/QUALIFICATION.md`, `sops/sales/DISCOVERY.md`, `templates/sales/PROPOSAL_OUTLINE.md`, `agents/SALES_AGENT.md`

---


## 1. Purpose
Convert qualified opportunities into profitable client engagements through a consistent, ethical, evidence-based process.

## 2. Sales Pipeline
`Prospect → Research → Qualification → Discovery → Solution → Proposal → Agreement → Onboarding`

## 3. Qualification
Establish:
- Problem
- Desired outcome
- Buyer authority
- Constraints
- Timing
- Fit
- Delivery feasibility

Do not force-fit every prospect.

## 4. Discovery
Discovery should understand the business before prescribing a solution.

Key questions:
- What is happening now?
- What should be different?
- Why does it matter?
- Who is affected?
- What constraints exist?
- How will success be recognized?

## 5. Solution Development
Recommend the minimum viable scope that can responsibly solve the relevant problem.

Do not sell features merely because they are technically possible.

**Every requirement must trace to a discovery finding, an explicit client
statement, or a documented assumption.** A requirement with no source is
removed, not justified — this is where fabricated scope enters a commercial
engagement.

Procedure: `sops/sales/SOLUTION_DESIGN.md`.

## 6. Commercial Constraints

Binding on every sales conversation and proposal:

- **Never state a price.** Pricing, minimum engagement, and package economics
  are set in `SERVICES.md` §2.4 (D-038). Quote within the approved range; the
  figure for an engagement follows the solution design and is approved by
  the founder. An invented figure creates a commitment the company has not
  made.
- **Never promise deliverables that are not defined.** Package contents are
  defined in `SERVICES.md` §7 (D-029).
- **Sell into the confirmed progression** (D-005): Strategic Website & Digital
  Foundation first, then expansion, then recurring. Do not lead with an
  expansion engagement before the foundation is sound.
- **No guarantees of outcome.** Forecasts must be labelled as estimates.
- Proposal issuance and any commercial commitment are **founder decisions**
  (`governance/AUTHORITY.md` §6). Agents draft; the founder approves and sends.

## 7. Proposal Standard
A proposal should clearly state:
- Context
- Problem
- Recommended approach
- Scope
- Deliverables
- Exclusions
- Timeline assumptions
- Client responsibilities
- Commercial terms
- Acceptance/change process
- Next step

Procedure: `sops/sales/PROPOSAL.md`, which covers the issuance gate, the
founder approval routing, where the proposal is filed, and how its outcome is
recorded.

**Issuance is currently gated.** `SERVICES.md` §4 requires a pricing model and
defined deliverables before an offer is presented commercially; both are open
(`SERVICES.md` §2.4). The minimum engagement is $5,000; an engagement below it
requires an explicitly recorded founder exception (D-038).

## 8. Sales Ethics
Do not:
- Fabricate urgency
- Misrepresent capability
- Guarantee unsupported outcomes
- Hide material limitations
- Pressure prospects into unsuitable work

## 9. Handoff
Before delivery begins, transfer to the delivery phase:

- The approved statement of work and agreement
- All material discovery context and notes
- Stated client objectives and success criteria
- Known constraints, risks, and assumptions
- Stakeholders and the accountable decision-maker
- Anything promised verbally during the sales process

The last item is the most commonly lost and the most damaging: an
undocumented verbal commitment becomes a scope dispute during delivery.

Initialize the engagement using `clients/_CLIENT_TEMPLATE/`. Detailed
onboarding is governed by `DELIVERY.md` §3 and `sops/delivery/ONBOARDING.md`.
