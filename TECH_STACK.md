# TECH_STACK.md
# THE MILBOURNE GROUP
## TECHNICAL GOVERNANCE SOURCE OF TRUTH

**System:** Technology
**Purpose:** Prevent uncontrolled technology sprawl while allowing justified technical decisions.
**Authority:** Tier 3. Authoritative for technology selection, repository standards, change control, and technical debt.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme)
**Applies to:** All technology selection and repository governance.
**Owner:** Founder
**Status:** Active — approved stack open (Q-009).
**Last reviewed:** 2026-08-29
**Review trigger:** Stack configuration; material technology change; vendor risk event.
**Related:** `WEB_STANDARDS.md` (craft standards), `SECURITY.md`, `templates/development/REPOSITORY_CLAUDE_TEMPLATE.md`

---


## 1. Purpose
Prevent uncontrolled technology sprawl while allowing justified technical decisions.

## 2. Selection Principles
Choose technology based on:
- Client requirements
- Reliability
- Security
- Maintainability
- Team/AI capability
- Ecosystem maturity
- Cost
- Performance
- Vendor risk
- Deployment requirements

Do not choose technology primarily for novelty.

## 3. Approved Stack Status
The company-wide approved stack is not yet fully configured.

Until formalized:
- Do not claim a technology is standard without authorization.
- Prefer stable, well-supported tools.
- Document material decisions.

## 4. Repository Standards
Each significant repository should include `CLAUDE.md` covering:
- Purpose
- Architecture
- Commands
- Dependencies
- Testing
- Deployment
- Constraints

## 5. Development Standards

Web product craft standards — implementation, accessibility, responsive
behaviour, and performance — are defined in `WEB_STANDARDS.md`, which is their
single source of truth.

This document governs **technology selection and governance**; `WEB_STANDARDS.md`
governs **how well the product is built**. The near-identical implementation
list previously held in both places, and in the former `MASTER.md` §11.3, has been
consolidated there.

## 6. Change Control
Material technical changes should consider migration, rollback, compatibility, security, and maintenance.

## 7. Technical Debt
Record significant debt when intentionally accepted. Include reason, consequence, and review trigger.
