# CLAUDE.md — <REPOSITORY>

> Template — Tier 6. Required for every significant repository
> (`MASTER.md` §13.1, `TECH_STACK.md` §4).
>
> **Repository instructions govern implementation detail for this repository
> only.** They never override security requirements, client confidentiality,
> legal or contractual obligations, or any absolute constraint in
> `MASTER.md` §7.

**Repository:**
**Client / Project:**
**Owner:** Founder
**Status:** Active / Maintenance / Archived
**Last updated:**

---

## 1. Purpose
What this repository is and the business outcome it serves.

## 2. Architecture
Structure, key modules, and how they relate. Enough that a new operator can
orient without reading everything.

## 3. Stack
Languages, frameworks, and major libraries, with versions.

## 4. Commands

```bash
# Install
# Develop
# Test
# Lint / typecheck
# Build
# Deploy (staging)
```

## 5. Dependencies
External services, APIs, and integrations. **Name credentials and where they
are stored — never their values** (`MASTER.md` §7.3).

## 6. Coding Standards
Repository-specific conventions. Company craft standards are in
`WEB_STANDARDS.md` §4 — this section adds detail, it does not lower the bar.

## 7. Testing
What is tested, how to run it, and what must pass before a change is
considered complete.

## 8. Deployment
Environments, procedure, who may deploy, and the rollback procedure.
Production deployment requires founder authorization (`MASTER.md` §7.4).

## 9. Constraints
Anything that must not be changed, and why.

## 10. Known Risks and Technical Debt

| Item | Reason accepted | Consequence | Review trigger |
|---|---|---|---|
| | | | |

*Recorded per `TECH_STACK.md` §7.*
