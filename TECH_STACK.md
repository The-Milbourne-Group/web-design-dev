# TECH_STACK.md
# THE MILBOURNE GROUP
## TECHNICAL GOVERNANCE SOURCE OF TRUTH

**System:** Technology
**Purpose:** Prevent uncontrolled technology sprawl while allowing justified technical decisions.
**Authority:** Tier 3. Authoritative for technology selection, repository standards, change control, and technical debt.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme)
**Applies to:** All technology selection and repository governance.
**Owner:** Founder
**Status:** Active — stack policy (D-034) and named defaults (D-039) confirmed.
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

## 3. Approved Stack

**Confirmed — policy (D-034) and named defaults (D-039).**

The purpose of an approved stack is **not** to force every client into
identical technology. It is to stop re-evaluating commodity decisions, so that
reusable assets, knowledge, deployment practices and documentation accumulate.

### 3.1 Approved Defaults

| Category | Approved default | Approved alternatives | Exception required |
|---|---|---|---|
| Marketing and business websites | **Next.js + TypeScript**, Tailwind CSS | Limited | Yes |
| Custom web applications | **Next.js + TypeScript**, managed services | Limited | Yes |
| CMS | **By requirement** — native/static, then headless CMS, then a specialized platform only where clearly justified | Use-case dependent | Sometimes |
| Hosting and deployment | **Vercel or equivalent managed modern hosting** | Selected per project against client requirements, security, compliance, cost, ownership | Yes |
| Integrations and automation | **APIs and appropriate automation tooling**; **PostgreSQL** (managed) where relational data is required | Use-case dependent | Sometimes |

Each category's default must define its full shape — for websites: framework,
styling, component architecture, form handling, analytics, SEO approach, image
optimization and deployment. For applications: front-end framework, application
architecture, back-end, database, authentication, API architecture, testing and
deployment model. For hosting: provider, deployment workflow, environments, DNS,
backup, monitoring and access management. For integrations: API patterns,
credential storage, webhooks, workflows, error logging, monitoring and
documentation.

### 3.2 Selection Rule

A technology becomes an approved default **only where the company can support
it across development, deployment, security, maintenance, documentation and
client handoff.** Favour what can be confidently built with, debugged, secured,
maintained, handed off and supported long term.

**Popularity alone is not justification.** A CMS is not introduced where static
or application-driven content is operationally more appropriate.

### 3.3 Exception Policy

A project may deviate from the approved default where:

- the client has existing infrastructure;
- a technical requirement cannot be met by the default;
- a specialized platform is commercially necessary;
- regulatory or security requirements demand a different architecture; or
- long-term client maintainability requires an alternative.

**Every exception is documented** — reason, alternative chosen, and maintenance
consequence — in the project's own record.

### 3.4 Architecture Principle

**Prefer the simplest secure architecture that satisfies the documented
requirements.** Custom infrastructure requires a documented business or
technical justification.

**Do not force a CMS** where static or application-driven content is
operationally more appropriate.

**Automation is implemented only where** the process is sufficiently stable,
inputs and outputs are understood, failure modes are acceptable, and ownership
and monitoring are defined (`MASTER.md` §11, `AUTOMATION.md`).

All production work meets the existing security, web standards, accessibility,
QA, backup and version-control requirements — the named stack does not relax
any of them.

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
