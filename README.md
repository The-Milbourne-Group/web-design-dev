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
tools/e2e.sh             # end-to-end test of the whole system (76 assertions)
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

`OPEN_QUESTIONS.md` is the single register of what is unknown. An operator that
supplies a price or a client profile from imagination has created a false
company fact that propagates into client-facing material.

This is enforced, not just stated. `./mg` reads the register at runtime and
refuses to state a figure, tag an unapproved capability, or issue a proposal
while the values it depends on are open.

**An approved model is not an approved number.** Four Discovery Round 2 answers
approved an architecture and explicitly deferred its values. Treating the
parent question as fully answered is how an invented price reaches a client.

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

**Discovery Round 2 is complete.** Q-001 – Q-012 are resolved by D-019 – D-030:
market approach, maturity target, size bands and buyer roles, primary trigger,
founder-advantage policy, capacity model, pricing architecture, acquisition
channels, stack policy, visual direction, package structure, and escalation
authority.

Thirty decisions are recorded. Four assumptions remain active; two were retired
by Discovery Round 2.

### Open — five items

| | Question | Priority |
|---|---|---|
| **Q-013** | Founder advantage inventory — actual experience, relationships, past projects | **Blocking** |
| **Q-014** | Founder capacity and financial requirements | **Blocking** |
| **Q-015** | Price points, minimum engagement, revenue targets | **Blocking** |
| Q-016 | Named technology stack | High |
| Q-017 | Brand asset values | Medium |

### The bottleneck

**Q-013.** D-026 makes warm network and referrals the highest-priority
acquisition channel, and D-023 makes market selection the intersection of
*founder access + technical advantage + market pain + project economics*.
Three of those four terms are now known. The fourth is not — so the
highest-priority channel cannot be worked, and no market can be selected.

**Until Q-015 is answered, no proposal may state a figure.** The pricing
*model* is approved (D-025); the numbers are not. `./mg` enforces this: the
proposal gate stays shut, and clearing it for a single engagement is an
explicit founder decision recorded against that engagement.

### Not yet proven

No SOP in this system has been executed against a live engagement. Every
procedure is constructed from the domain documents rather than transcribed from
observed practice, and the pilots that exercise them use realistic simulations,
not real clients. Treat the first real pass through each as a draft to correct.
