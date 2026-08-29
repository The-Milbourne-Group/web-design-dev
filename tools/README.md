# `mg` — the operating tool

The commercial pipeline, executable. One command per documented step, from lead
to active delivery.

```
LEAD → QUALIFICATION → DISCOVERY → ANALYSIS → SOLUTION → PROPOSAL
     → FOLLOW-UP → CLOSED DEAL → PROJECT INITIALIZATION
```

## Run it

```bash
./mg list                      # the pipeline
./mg status <slug>             # one opportunity: last, next, owner, when
./mg check                     # governance check across every opportunity
./mg metrics                   # conversion, cycle time, proposal build time
tools/e2e.sh                   # end-to-end test of the whole slice (37 assertions)
tools/e2e.sh --keep            # same, but leaves the records for inspection
```

Python 3.11+, standard library only. No install, no credentials, no services.

## Where the data lives

`clients/<slug>/opportunity.json` is the record. Every markdown file beside it
is **generated from that record** — `README.md`, `QUALIFICATION.md`,
`DISCOVERY.md`, `SOLUTION.md`, `PROPOSAL.md`, `PROPOSAL_DRAFT.md`,
`PROJECT_BRIEF.md`. Edit the record, not the markdown: `mg render <slug>`
overwrites the generated files.

That is the whole answer to duplicate data entry. A fact captured at
qualification appears in the proposal and the project brief without being typed
again, which is also why "what was sold" is now reconcilable at onboarding.

`clients/` was already the declared home for client knowledge (Tier 7,
`clients/README.md`). Putting the pipeline in a CRM would have created a second
source of truth, which `MASTER.md` §5.3 forbids.

## The guards

The tool refuses what the operating system reserves. Each refusal names the
document it comes from.

| Guard | Enforces |
|---|---|
| Qualification needs authority, an ICP signal, feasibility and a stage | `sops/sales/QUALIFICATION.md` §5 |
| Qualify / disqualify needs `--approved-by` | `governance/AUTHORITY.md` §7 |
| No solution design before client playback | `sops/sales/DISCOVERY.md` §5.9 |
| A requirement with no source blocks approval | `sops/sales/SOLUTION_DESIGN.md` §5.2 |
| Proposal issuance blocked while Q-007 / Q-011 are open | `SERVICES.md` §4, `sops/sales/PROPOSAL.md` §5.1 |
| A commercial figure is rejected until the founder decides terms | `SALES.md` §6 |
| Declining a proposal requires loss reasoning | `sops/sales/PROPOSAL.md` §5.10 |
| Kickoff needs acceptance criteria and named approvers | `sops/delivery/ONBOARDING.md` §5.4, §5.9 |
| Only documented status transitions are permitted | `clients/README.md` |

`OPEN_QUESTIONS.md` is parsed at runtime, so when the founder resolves Q-007
the gate opens on its own. No code change, one source of truth.

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

Two behaviours matter. A qualification recommendation is **logged, never
applied** — the founder decides. And `discovery-analysis` requires every finding
to be typed confirmed or inferred; inferences are printed back on ingest and
stay labelled through to the project brief.

## Autonomy

This is an operator tool, not an autonomous automation: the human performs each
step and the tool assists and refuses (`AUTOMATION.md` Level 1–2). Nothing here
sends, publishes, or decides. Every founder decision is an explicit
`--approved-by` on the command line, recorded in the event log.

## Not built, deliberately

Scheduling, email and e-signature integrations. Each needs a credential and a
vendor decision the founder has not made, and none of them is the bottleneck.
Discovery dates are recorded, not booked.
