# KNOWLEDGE ARCHITECTURE

**System:** Governance
**Purpose:** Define the classes of knowledge in this system, where each belongs, and the rules preventing them from mixing.
**Authority:** Tier 3 governance.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Anyone deciding where a new piece of information belongs.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** New knowledge class; repeated misfiling.
**Related:** `SYSTEM_MAP.md`, `governance/DOCUMENT_REGISTRY.md`, `CLAUDE.md`

---

## 1. Why Classification Matters

Documents with different lifespans and different authority must not be mixed.
When a stable rule and a temporary note live in the same file, the note
acquires authority it was never granted, and the rule becomes unstable.

The original `MASTER.md` demonstrated the failure: a constitution that also
contained delivery phases, metric lists, automation levels, and a directory
listing. Its stable content could not be changed without touching volatile
content, and its volatile content silently competed with the domain documents
that owned those subjects.

---

## 2. The Seven Classes

### 1. Constitutional Knowledge — *how the company operates*
Long-lived rules, principles, authority, and boundaries.

**Lives in:** `MASTER.md`, `governance/`
**Changes:** Rarely. Founder approval always required.
**Test:** Would this still be true if the company changed markets entirely?

### 2. Strategic Knowledge — *what the business is*
Identity, positioning, market, offers, commercial model.

**Lives in:** `STRATEGIC_CONFIGURATION.md`, `DECISIONS.md`
**Changes:** Deliberately, by founder decision only.
**Test:** Does this describe what the company has decided to be?

### 3. Domain Knowledge — *what is true about a business area*
Authoritative knowledge for sales, brand, delivery, security, and the rest.

**Lives in:** Tier 3 documents at the repository root.
**Changes:** With evidence, via founder approval.
**Test:** Is this true across all clients and projects?

### 4. Procedural Knowledge — *how work is performed*
Repeatable steps, checklists, quality gates.

**Lives in:** `sops/`, indexed by `SOP_INDEX.md`
**Changes:** As process improves. Operator may refine; policy changes escalate.
**Test:** Could someone follow this and produce the same result?

### 5. Agent Knowledge — *instructions to AI operators*
Role definitions, scope, authority, escalation.

**Lives in:** `agents/`
**Changes:** As roles evolve.
**Test:** Does this tell an agent what it may and may not do?

### 6. Reusable Assets — *structured starting points*
Templates and scaffolds.

**Lives in:** `templates/`, `clients/_CLIENT_TEMPLATE/`
**Changes:** Freely — they carry no authority.
**Test:** Is this a starting point rather than a statement of fact?

### 7. Project Knowledge — *what is true about one engagement*
Client context, requirements, decisions, and artifacts.

**Lives in:** `clients/<client>/`
**Changes:** Constantly, within the engagement.
**Test:** Would this be meaningless to a different client?

### Plus: Temporary Knowledge
Drafts, research, unreviewed AI output, session notes.

**Lives in:** A scratch location outside this repository, or clearly marked as
a draft within a project.
**Carries no authority.** Promote it under
`governance/CHANGE_MANAGEMENT.md` or discard it. Never commit an unreviewed
AI artifact into a location that implies authority.

---

## 3. Placement Decision

Use this order. Stop at the first match.

```
Is it specific to one client or engagement?        → clients/<client>/
Is it a decision the founder has approved?         → DECISIONS.md
Is it a question the founder must answer?          → OPEN_QUESTIONS.md
Is it an unconfirmed premise being relied on?      → ASSUMPTIONS.md
Is it a threat to be tracked?                      → RISKS.md
Is it a term needing a shared definition?          → GLOSSARY.md
Is it a repeatable procedure?                      → sops/<domain>/
Is it an instruction to an AI role?                → agents/
Is it a reusable starting point?                   → templates/
Is it true across all clients in one domain?       → that domain's Tier 3 doc
Is it a universal operating rule?                  → MASTER.md
Otherwise                                          → it is temporary; do not file it
```

---

## 4. Anti-Mixing Rules

1. **A document holds one class.** Constitutional documents do not carry
   procedures. Domain documents do not carry client data.
2. **Never write client-specific information into a company document.**
   Illustrate with a generic example instead.
3. **Never write company policy into a client document.** Reference it.
4. **Never write a credential value anywhere.** Name and location only
   (`MASTER.md` §7.3).
5. **Never let a template become a source of truth.** A filled-in example is
   not evidence that its values are real.
6. **Never let unreviewed AI output enter Tiers 1–4.** It is Temporary until
   a human reviews it.
7. **One subject, one owner.** If two documents describe the same subject, one
   is defective — see `governance/DOCUMENT_REGISTRY.md`.

---

## 5. Client Isolation

Client knowledge is additionally governed by the absolute constraints in
`MASTER.md` §7.1 and `SECURITY.md` §4.

- Each client has one directory under `clients/`.
- Nothing in one client's directory may reference another client's specifics.
- Load exactly one client's context per working session.
- Cross-client learning is generalized — pattern only, no identifying
  detail — and promoted into a domain document or SOP through
  `governance/CHANGE_MANAGEMENT.md`. It never travels directly between client
  directories.
