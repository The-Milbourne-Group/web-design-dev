# SOP: OPPORTUNITY QUALIFICATION

**System:** Sales
**Purpose:** Determine whether an opportunity is a strong fit before investing discovery time.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `SALES.md`, `ICP.md`
**Applies to:** Every new prospect or inbound inquiry.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Evidence that the D-021 profile or D-022 trigger is wrong; recurring mis-qualification.
**Related:** `ICP.md`, `SALES.md`, `sops/sales/DISCOVERY.md`

---

## 1. Purpose

Decide, quickly and consistently, whether to advance an opportunity to
discovery — protecting founder capacity, the scarcest resource in the company
(`RISKS.md` R-005).

## 2. Trigger

A new prospect, inbound inquiry, referral, or reactivated lead.

## 3. Owner

Founder. An agent may prepare the assessment; the founder decides the outcome.

## 4. Inputs

- Prospect name, business, and how they arrived
- Whatever they have stated about their problem
- Their current website or digital presence
- `ICP.md` §2 (confirmed configuration), §4–§6 (signals)

## 5. Procedure

1. **Create the opportunity directory.** Copy `clients/_CLIENT_TEMPLATE/` to
   `clients/<prospect-name>/` and set `Status: Prospect`. This is where every
   artifact from here to closure lives (`clients/README.md`).

2. **Record the source** in `QUALIFICATION.md`. How the prospect arrived is
   channel evidence testing the D-036 acquisition order. Log it even when the
   opportunity is disqualified.

3. **Assess ICP fit** against `ICP.md` §4 and §5. Note which specific high-fit
   characteristics and problem signals are present. Do not score against
   numeric size bands — those are open (`ASSUMPTIONS.md` A-005).

4. **Identify the problem and desired outcome** in the prospect's own words.
   If neither can be stated in one sentence, the outcome is *Clarification
   required*, not *Qualified*.

5. **Confirm authority.** Establish who owns the decision and who controls
   budget. "I'd have to check with my partner" is an unresolved decision-maker,
   not an objection to overcome.

6. **Check disqualification signals** in `ICP.md` §6. Any single strong signal
   is sufficient to disqualify — they do not need to accumulate.

7. **Assess delivery feasibility.** Can the company deliver this responsibly
   with current capacity and capability? A capability the company does not
   have is not a stretch goal.

8. **Locate the engagement in the commercial progression** (`SERVICES.md` §2).
   An opportunity that fits no stage is off-strategy.

9. **Record the outcome and reasoning** — including for disqualified
   opportunities, which are the most useful evidence for ICP configuration.

## 6. Outputs

One of four outcomes, with written reasoning:

| Outcome | Meaning | Next step |
|---|---|---|
| **Qualified** | Strong fit; advance | `sops/sales/DISCOVERY.md` |
| **Nurture** | Real fit, wrong timing | Record the revisit trigger |
| **Clarification required** | Cannot assess yet | Named questions to resolve; `Status` stays `Prospect` |
| **Disqualified** | Poor fit or undeliverable | Decline courteously; record why |

**Location:** `clients/<prospect-name>/QUALIFICATION.md`, with `Status` set in
that directory's `README.md`.

Plus: source recorded; ICP and buyer evidence captured in the directory
`README.md` testing the D-021 buyer roles; risks noted.

**Disqualified opportunities keep their directory.** The reasoning is the
primary market-selection evidence under D-019 (`ICP.md` §7).

## 7. Quality Checks

- [ ] No invented assumption is presented as fact.
- [ ] No price, timeline, or deliverable was quoted (`SALES.md` §6 — pricing
      is not quoted at qualification).
- [ ] The decision-maker is identified or explicitly recorded as unknown.
- [ ] Reasoning would be intelligible to someone else in three months.
- [ ] Disqualification reasoning is recorded, not just the verdict.
- [ ] The opportunity directory exists and `Status` is set.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Qualified on enthusiasm rather than evidence | Re-run §5 against `ICP.md` before discovery; capacity spent on a poor fit is unrecoverable |
| A price was quoted | Correct it in writing immediately; escalate to the founder |
| Disqualified a good fit on incomplete information | Re-open; the cost of a second look is low |
| Prospect pressures for immediate commitment | Urgency is a disqualification signal, not a reason to skip steps |

## 9. Escalation

Escalate to the founder before responding when: the prospect requests pricing
or a commitment; the opportunity is large or unusual; legal, security, or
compliance obligations appear; the work sits outside stated capability; or the
prospect is a competitor, existing client's competitor, or presents a conflict.

## 10. Automation Potential

**Can be assisted:** research on the prospect's business and current site,
drafting the fit assessment, surfacing matched ICP signals, logging source
data.

**Must not be automated:** the qualify/disqualify decision, any communication
to the prospect, and any statement about price or scope. These are founder
decisions (`governance/AUTHORITY.md` §7).
