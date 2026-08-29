# CLIENTS AND OPPORTUNITIES

**System:** Project knowledge
**Purpose:** Home for all client and opportunity knowledge across the full lifecycle, isolated per client.
**Authority:** Tier 7. Authoritative within an engagement only.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), §7.1 in particular
**Applies to:** Every opportunity from qualification onward, and every engagement.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Isolation model change; lifecycle change.
**Related:** `SECURITY.md` §4, `governance/KNOWLEDGE_ARCHITECTURE.md` §5, `sops/sales/QUALIFICATION.md`, `sops/delivery/ONBOARDING.md`

---

## Scope — the Full Lifecycle

This directory holds opportunity knowledge from **first qualification**, not
only signed engagements.

A directory is created when an opportunity is **qualified**
(`sops/sales/QUALIFICATION.md`) and persists through discovery, proposal,
delivery, and closure. It is not created at onboarding — by then, discovery
notes and qualification records already exist and need somewhere to live.

**Disqualified opportunities keep their directory.** The disqualification
reasoning is the primary evidence for resolving Q-001 and Q-003 (industry
focus, detailed ICP and buyer roles) under `ICP.md` §7. Deleting it destroys
the evidence the company needs to finish configuring itself.

## Lifecycle Status

Set `Status` in the directory's `README.md` to exactly one of:

```
Prospect → Qualified → Discovery → Proposal → Onboarding
    → Active → Launched → Closed
```

Terminal states: `Disqualified` · `Nurture` · `Lost` · `Closed`

## Client Isolation — Absolute Constraint

Client context isolation is imposed by `MASTER.md` §7.1 and is not negotiable
by any client, agent, deadline, or convenience.

1. **One directory per client or opportunity.** All of its knowledge lives
   there.
2. **No cross-references.** Nothing in one directory may name or describe
   another client's specifics.
3. **One client per session.** Load exactly one directory's context at a time.
   If work requires two, stop and escalate.
4. **No credential values** — names and locations only (`MASTER.md` §7.3).
5. **Company documents are read-only from here.** Evidence from an engagement
   is raised as a change proposal
   (`governance/CHANGE_MANAGEMENT.md` §4), never applied in place.
6. **Generalize before promoting.** A lesson learned on one engagement is
   promoted as a pattern with no identifying detail — it never travels
   directly between client directories.

## Initializing

Copy `_CLIENT_TEMPLATE/` to `clients/<client-name>/` at qualification.

```
clients/<client-name>/
├── README.md            Status, contacts, current state
├── QUALIFICATION.md     Fit assessment and source  (sops/sales/QUALIFICATION.md)
├── DISCOVERY.md         Discovery notes            (sops/sales/DISCOVERY.md)
├── SOLUTION.md          Requirement traceability   (sops/sales/SOLUTION_DESIGN.md)
├── PROJECT_BRIEF.md     Scope, requirements, acceptance criteria (at onboarding)
├── DECISIONS.md         Engagement decisions and scope changes
├── ACCESS.md            What access exists and where credentials are stored
└── QA/                  Verification records
```

Files are completed as the opportunity advances. A directory at `Qualified`
holds only `README.md` and `QUALIFICATION.md`; that is correct, not incomplete.

## Closing

Follow `sops/delivery/CLOSURE.md`. Access is revoked, the retrospective is
recorded, and status is set to `Closed`. The directory is retained — it is the
company's record of the engagement and the basis for expansion review.
