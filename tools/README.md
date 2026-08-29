# `mg` — the operating tool

The commercial pipeline, executable. One command per documented step, from lead
to active delivery.

```
LEAD → QUALIFICATION → DISCOVERY → ANALYSIS → SOLUTION → PROPOSAL
     → FOLLOW-UP → CLOSED DEAL → PROJECT INITIALIZATION
```

## Run it

```bash
./mg intake --from enquiry.txt --channel email   # capture a lead from anything
./mg next                      # every open opportunity: stage, last, next, owner, gaps
./mg status <slug>             # one opportunity in full
./mg check                     # governance check across every opportunity
./mg metrics                   # conversion, cycle time, proposal build time
tools/e2e.sh                   # end-to-end test of the whole slice (76 assertions)
tools/e2e.sh --keep            # same, but leaves the records for inspection
```

`mg next` is the daily view. It answers, for every live opportunity: what stage,
what happened last, what happens next, who owns it, when it is due, and what
information is still missing.

Python 3.11+, standard library only. No install, no credentials, no services.

## Where the data lives

`clients/<slug>/opportunity.json` is the record. Every markdown file beside it
is **generated from that record** — `README.md`, `QUALIFICATION.md`,
DISCOVERY.md, SOLUTION.md, PROPOSAL.md, PROPOSAL_DRAFT.md and
PROJECT_BRIEF.md. Edit the record, not the markdown: `mg render <slug>`
overwrites the generated files.

That is the whole answer to duplicate data entry. A fact captured at
qualification appears in the proposal and the project brief without being typed
again, which is also why "what was sold" is now reconcilable at onboarding.

`clients/` was already the declared home for client knowledge (Tier 7,
`clients/README.md`). Putting the pipeline in a CRM would have created a second
source of truth, which `MASTER.md` §5.3 forbids.

## The growth engine — `mg target`

Upstream of the pipeline: identify a company, research it, assess fit, reach
out, and convert it to a lead only when someone actually engages.

```bash
./mg target add --company "..." --via "Targeted outbound" --campaign q4
./mg target brief <slug> target-research     # then: target ingest <slug> target-research
./mg target brief <slug> target-assess
./mg target compose <slug> --body-file msg.txt --grounded-in E1 --grounded-in E2
./mg target approve <slug> --approved-by Founder --channel email
./mg target sent <slug> --channel email
./mg target respond <slug> --kind positive --text "..."
./mg target convert <slug>                   # becomes clients/<slug>
```

Targets live in `growth/<slug>/`, not `clients/`. `clients/README.md` creates a
directory at qualification, when a lead exists; a target has not been contacted
and may never become one. Filing every researched company under `clients/`
would flood the pipeline and corrupt the buyer evidence base.

**Evidence is typed.** Every research item is `confirmed` (with a source),
`inference`, or `unknown`. A confirmed item with no source is refused.

**Personalisation must be grounded.** Every draft names the evidence refs it
rests on, and those must be *confirmed*. A message resting on an inference is
refused at approval — that is the mechanical version of "do not pretend
outreach is personalised when it is not". The pilot caught exactly this: a
draft telling a prospect "you're currently losing enquiries" when that was
reasoning, not observation.

**The tool never sends.** It drafts, records founder approval, and logs what
you sent. Outreach is client-facing communication and founder-approved
(`governance/AUTHORITY.md` §7).

**Conversion needs a positive response.** Contacting someone does not make them
a lead. On conversion, confirmed facts cross as facts *with their sources*,
inferences cross as explicitly labelled assessment, and unknowns become open
items — the boundary survives the handover.

## Lead intake

```bash
./mg intake --from enquiry.txt --channel email    # forwarded email
cat form-post.json | ./mg intake --channel form   # web form or API POST
./mg intake --channel phone --company "Acme"      # note typed after a call
```

One entry point for every channel. It parses `Label: value` pairs, JSON bodies,
and the free text of an email; pulls out email, phone and website; and keeps the
original enquiry verbatim in the event log. **Anything it cannot find is
reported as missing, never guessed** — an unparsed field is a question to ask
the prospect.

## Pipeline stages

`status` is the authoritative field and `clients/README.md` owns its vocabulary.
`mg next` shows a derived operating stage on top of it — NEW, QUALIFYING,
QUALIFIED, DISCOVERY, SOLUTION, PROPOSAL, NEGOTIATION, WON, PROJECT INITIALIZED,
NOT A FIT, LOST, ON HOLD — because status alone cannot distinguish a lead being
worked from one just captured, or a proposal issued from one in negotiation.

Hold is recorded alongside the status rather than replacing it, so a paused
opportunity keeps the stage it actually reached:

```bash
./mg hold <slug> --reason "Contact on leave" --revisit 2026-12-01
./mg hold <slug> --release
```

A hold needs a reason, and a revisit date schedules the follow-up that brings it
back. `clients/README.md` has no ON HOLD status and adding one is a founder
decision, so the tool does not invent one.

## When something goes wrong

Every save is atomic (temp file, then rename) and archives the previous version
under `clients/<slug>/.history/`. An interrupted or killed process leaves the
record whole — verified against repeated SIGKILLs mid-write.

```bash
./mg check                          # includes any record that cannot be read
./mg restore <slug> --list          # archived versions
./mg restore <slug> --version 1     # recover one
./mg drop <slug> --requirement R9   # remove a mis-ingested item
```

A record that fails validation is never written and never silently skipped:
`mg check`, `mg list` and `mg next` all name it and point at `mg restore`.
`mg check` exits non-zero when it finds anything, so it works as a cron or
pre-commit health check.

Persistence and backup are git: the records are committed with the repository,
so history and off-machine recovery already exist. Nothing else is required at
this scale.

## The guards

The tool refuses what the operating system reserves. Each refusal names the
document it comes from.

| Guard | Enforces |
|---|---|
| Qualification needs authority, an ICP signal, feasibility and a stage | `sops/sales/QUALIFICATION.md` §5 |
| Qualify / disqualify needs `--approved-by` | `governance/AUTHORITY.md` §7 |
| No solution design before client playback | `sops/sales/DISCOVERY.md` §5.9 |
| A requirement with no source blocks approval | `sops/sales/SOLUTION_DESIGN.md` §5.2 |
| Figures below the $5,000 minimum engagement are flagged | `SERVICES.md` §2.4, D-038 |
| A commercial figure is rejected until the founder decides terms | `SALES.md` §6 |
| Declining a proposal requires loss reasoning | `sops/sales/PROPOSAL.md` §5.10 |
| Kickoff needs acceptance criteria and named approvers | `sops/delivery/ONBOARDING.md` §5.4, §5.9 |
| Only documented status transitions are permitted | `clients/README.md` |
| Every in-scope requirement names an approved capability | `SERVICES.md` §3 |
| A finding's `confirmed` flag must be a real boolean | evidence/inference boundary |
| Duplicate company or contact email is refused | data continuity |

`SERVICES.md` §2.4 is parsed at runtime for the approved bands and the minimum
engagement value, so a pricing change is a document edit. No code change, one
source of truth.

## The AI layer

The AI operator here is a Claude Code session, so the leverage is context
assembly and structured hand-back, not another API client.

```bash
./mg brief <slug> qualify           # emits a task packet — paste into a session
./mg ingest <slug> qualify --from result.json
```

`brief` applies the `CLAUDE.md` §3 loading table for that task, injects the live
open-questions list and the `ICP.md` signal set, states the constraints, and
asks for JSON. `ingest` merges the result, so no AI output is retyped.

Tasks: `research`, `qualify`, `discovery-prep`, `discovery-analysis`,
`solution`, `proposal`, `follow-up`.

Three behaviours matter.

`qualify` returns four separated things — **confirmed facts** (what the record
supports), **assessment** (the reading placed on it), **missing information**,
and a **recommended next action**. The recommendation is recorded, never
applied: the founder decides. On a strategically ambiguous opportunity the
correct answer is `Clarification required`, not a guess.

`discovery-analysis` requires every finding to be typed confirmed or inferred.
Inferences are printed back on ingest and stay labelled all the way to the
project brief.

Ingest **merges** by default and never discards what is already recorded — a
re-run analysis adds and updates rather than replacing. `--replace` is the
explicit way to discard. Contradictions (two confirmed findings on one topic
from different sources) are surfaced before solution design.

Project initialization carries the approved scope, exclusions, risks,
constraints and labelled assumptions forward — and deliberately withholds
internal reasoning, agent recommendations and unconfirmed inferences, so none of
it hardens into a project requirement.

## Autonomy

This is an operator tool, not an autonomous automation: the human performs each
step and the tool assists and refuses (`AUTOMATION.md` Level 1–2). Nothing here
sends, publishes, or decides. Every founder decision is an explicit
`--approved-by` on the command line, recorded in the event log.

## Not built, deliberately

Scheduling, email and e-signature integrations. Each needs a credential and a
vendor decision the founder has not made, and none of them is the bottleneck.
Discovery dates are recorded, not booked.
