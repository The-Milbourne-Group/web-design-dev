# THE MILBOURNE GROUP — BUSINESS OPERATING SYSTEM

The operating system for The Milbourne Group: a **boutique strategic digital
systems partner** helping established businesses whose commercial and
operational maturity has outgrown their website and digital infrastructure.

This repository holds how the company operates, what it has decided, what it
does not yet know — and the software that runs the commercial pipeline.

---

## Start Here

| You are | Read |
|---|---|
| **New to the company** | `EXECUTIVE_SUMMARY.md` → `STRATEGIC_CONFIGURATION.md` → `MASTER.md` |
| **An AI session** | `CLAUDE.md` — context loading, boundaries, escalation |
| **Operating the business today** | `tools/README.md`, then `./mg next` |
| **Looking for the architecture** | `SYSTEM_MAP.md` |
| **Resolving a conflict** | `governance/AUTHORITY.md` |
| **About to change a document** | `governance/CHANGE_MANAGEMENT.md` |
| **Executing a process** | `SOP_INDEX.md` |

## Two Layers

**The documents are the specification.** They define what the company is, what
it has decided, and how work must be done.

**`./mg` is the implementation.** A CLI that runs the pipeline from first
contact to active delivery, enforcing what the documents require and refusing
what they reserve. Python 3.11, standard library only — no install, no
services, no credentials.

```bash
./mg next                # every live opportunity and target: stage, next action, owner, gaps
./mg check               # governance check across every record
./mg metrics             # conversion, cycle time, channel performance
tools/e2e.sh             # end-to-end test of the whole system (78 assertions)
```

Full command reference: `tools/README.md`.

### What it covers

```
TARGET → RESEARCH → ASSESS → OUTREACH → LEAD
       → QUALIFY → DISCOVER → SOLUTION → PROPOSAL → WON → PROJECT INITIALIZED
```

Records live in `growth/<slug>/` before contact and `clients/<slug>/` from
lead onward. Every markdown artifact beside a record is **generated from it**,
so a fact captured once is never retyped — which is what makes "what was sold"
reconcilable at onboarding.

Delivery execution beyond project initialization is **not yet built**. The
lifecycle is specified in `DELIVERY.md` §2 and its procedures exist in
`sops/delivery/`, but they are run by hand.

## Authority

**`MASTER.md` is the ultimate authority.** Nothing in this repository
outranks it.

```
Tier 1  MASTER.md                    the operating constitution — supreme
Tier 2  Founder-approved strategy    STRATEGIC_CONFIGURATION.md, DECISIONS.md
Tier 3  Domain sources of truth      BUSINESS, SALES, DELIVERY, SECURITY, …
Tier 4  SOPs
Tier 5  Agent instructions
Tier 6  Templates
Tier 7  Project and client knowledge
Tier 8  Temporary working artifacts
```

`MASTER.md` §7 imposes **absolute constraints** — law, executed contracts,
security, safety, client confidentiality — that bind every tier including
itself. No client request, agent instruction, or deadline suspends them.

Authority is also **scoped**: a document governs only its declared subject.
Full model: `governance/AUTHORITY.md`.

## The One Rule Worth Repeating

**Never invent a value the founder has not decided.**

Strategic configuration is now complete, so the rule bites differently than it
used to: the values exist, and the job is to use them rather than improvise
around them. An operator that quotes a price outside `SERVICES.md` §2.4, claims
experience the founder has not documented, or extends the offer set has created
a false company fact.

This is enforced, not just stated. `./mg` reads the approved configuration at
runtime and refuses figures below the $5,000 minimum engagement, requirements
with no source, scope outside the approved capabilities, and outreach whose
personalisation rests on inference rather than observed fact.

**D-036 is worth reading before any outbound work.** The founder advantage is
operating capability, not credentials — no undocumented experience,
relationship, client, outcome or credential is ever claimed.

## Map

```
MASTER.md · CLAUDE.md · SYSTEM_MAP.md        entry points and constitution
STRATEGIC_CONFIGURATION.md                    founder-approved strategy
DECISIONS · OPEN_QUESTIONS · ASSUMPTIONS · RISKS · GLOSSARY   registers
BUSINESS · BRAND · SERVICES · ICP · MARKETING · SALES
DELIVERY · WEB_STANDARDS · TECH_STACK · AUTOMATION
SECURITY · METRICS · ROADMAP                  domain sources of truth
governance/                                   authority, change, registry, QA
sops/ (12) · agents/ (8) · templates/         procedure, roles, assets
tools/ · mg                                   the operating CLI
growth/                                       targets before contact
clients/                                      engagement knowledge, isolated
exports/                                      generated artifacts, no authority
```

## Current Status

**Strategic configuration is complete.** `OPEN_QUESTIONS.md` holds no pending
founder decision. Forty decisions are recorded (D-001 – D-040). The company is
in **controlled commercial validation** (D-037).

### The launch configuration

| | |
|---|---|
| **Market** | Established small-to-mid-sized service and professional businesses whose digital presence or infrastructure has outgrown the business (D-036) |
| **Advantage** | Operating capability — systems thinking, strategy-to-implementation continuity, founder-led delivery (D-036). No undocumented claims. |
| **Acquisition** | Targeted outbound · founder network where documented · referrals as they develop · portfolio evidence · selective partnerships (D-036) |
| **Capacity** | One major implementation in active build; at most two active engagements (D-037) |
| **Pricing** | $5,000 minimum · entry $7,500–$25,000 · assessment $1,500–$5,000 · recurring from $750/mo · 50/25/25 (D-038, `SERVICES.md` §2.4) |
| **Stack** | Next.js + TypeScript · Tailwind · PostgreSQL · Vercel or equivalent (D-039) |
| **Brand** | Inter · `#111111` `#F7F7F5` `#6B7280` `#E5E7EB` accent `#1D4ED8` · 4px spacing · 4–8px radius (D-040) |

### The objective

**Close and successfully deliver three profitable projects**, establish reliable
project economics, then refine pricing from actual delivery margin (D-037,
D-038). Revenue is prioritized over further speculative internal system
building.

### What is assumed, not known

Two operating assumptions carry the launch and are validated by the first
projects, not by argument:

- **A-007** — the price bands are viable in this market. No engagement has been
  sold at them.
- **A-008** — one major engagement at a time is sustainable. Not yet measured
  against real delivery.

Tax treatment and governing legal jurisdiction are unrecorded (**R-010**) and
must be settled before the first agreement is executed.

### Not yet built

Delivery execution beyond project initialization. The lifecycle is specified in
`DELIVERY.md` §2 and its procedures exist in `sops/delivery/`, but they are run
by hand.

### Not yet proven

No SOP has been executed against a live engagement. Every procedure is
constructed from the documents rather than transcribed from observed practice,
and the pilots are realistic simulations. Treat the first real pass through each
as a draft to correct.
