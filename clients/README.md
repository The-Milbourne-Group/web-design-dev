# CLIENTS

**System:** Project knowledge
**Purpose:** Home for all client and engagement knowledge, isolated per client.
**Authority:** Tier 7. Authoritative within an engagement only.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), §7.1 in particular
**Applies to:** Every engagement.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Isolation model change.
**Related:** `SECURITY.md` §4, `governance/KNOWLEDGE_ARCHITECTURE.md` §5, `sops/delivery/ONBOARDING.md`

---

## Client Isolation — Absolute Constraint

Client context isolation is imposed by `MASTER.md` §7.1 and is not negotiable
by any client, agent, deadline, or convenience.

1. **One directory per client.** All engagement knowledge lives there.
2. **No cross-references.** Nothing in one client's directory may name or
   describe another client's specifics.
3. **One client per session.** Load exactly one client's context at a time. If
   work requires two, stop and escalate.
4. **No credential values** — names and locations only (`MASTER.md` §7.3).
5. **Company documents are read-only from here.** Evidence from an engagement
   is raised as a change proposal
   (`governance/CHANGE_MANAGEMENT.md` §4), never applied in place.
6. **Generalize before promoting.** A lesson learned on one engagement is
   promoted as a pattern with no identifying detail — it never travels
   directly between client directories.

## Initializing an Engagement

Copy `_CLIENT_TEMPLATE/` to `clients/<client-name>/` and follow
`sops/delivery/ONBOARDING.md`.

```
clients/<client-name>/
├── PROJECT_BRIEF.md     Scope, requirements, stakeholders, acceptance criteria
├── DECISIONS.md         Engagement decisions (company decisions go to root DECISIONS.md)
├── DISCOVERY.md         Discovery notes carried from sales
├── ACCESS.md            What access exists and where credentials are stored
└── QA/                  Verification records per `sops/delivery/QA.md`
```
