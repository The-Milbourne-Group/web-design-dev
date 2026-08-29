# AGENT REGISTRY

**System:** Agents
**Purpose:** Route work to the correct agent, and record what each may decide, what it must escalate, and which documents it must load.
**Authority:** Tier 5 index. Authoritative for agent routing and responsibility boundaries.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), §10 in particular
**Applies to:** Any AI session or operator selecting an agent role.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Agent added, retired, or given new authority; overlapping authority discovered.
**Related:** `MASTER.md` §10, `governance/AUTHORITY.md` §7, `CLAUDE.md`

---

## 1. The Governing Principle

**Specialization grants capability, not authority.**

An agent's expertise in a domain never expands what it may decide. Every agent
operates inside `governance/AUTHORITY.md` §7, and no agent may grant itself a
right reserved to the founder.

Agent output is work product — analysis, evidence, recommendation, or draft.
It is never automatically correct (`MASTER.md` §10.1).

## 2. Routing

| Task | Agent |
|---|---|
| Prioritization, routing, cross-domain conflicts, bottleneck analysis | `CEO_AGENT.md` |
| Market analysis, positioning reasoning, opportunity evaluation, decision briefs | `STRATEGY_AGENT.md` |
| Prospect research, qualification support, discovery prep, proposal drafting | `SALES_AGENT.md` |
| Proposal issuance and commercial terms | **Founder**, via `sops/sales/PROPOSAL.md` |
| Solution design support and requirement traceability | `SALES_AGENT.md` prepares; **founder decides** |
| Search intent, content opportunity, technical SEO, growth measurement | `SEO_AGENT.md` |
| Interface design, UX, hierarchy, design systems, responsive states | `DESIGN_AGENT.md` |
| Implementation, architecture, integration, technical delivery | `DEV_AGENT.md` |
| Verification, defect finding, acceptance checking | `QA_AGENT.md` |
| Process mapping, automation design, monitoring, failure handling | `AUTOMATION_AGENT.md` |

**No agent fits?** Do the work under `MASTER.md` directly. Do not invent an
agent (`MASTER.md` §10.2 — specialization must justify its coordination cost).

## 3. Required Definition

Every agent file contains all ten elements from `MASTER.md` §10.2: mission,
responsibilities, non-responsibilities, inputs, outputs, tools, decision
authority, escalation rules, quality standards, and success criteria.

*Before 2026-08-29 no agent definition contained more than six of these; none
stated tools, decision authority, escalation rules, or success criteria. An
agent without stated boundaries defaults to assuming it has none.*

## 4. Overlap Resolution

Where two agents could plausibly claim a decision, authority is assigned to
exactly one. These were ambiguous before this registry existed.

| Contested decision | Authority | Other agent's role |
|---|---|---|
| What work is prioritized next | CEO | Strategy recommends; CEO sequences |
| Whether an opportunity is worth pursuing | Strategy (analysis) → Founder (decision) | Sales supplies qualification evidence |
| Whether to disqualify a prospect | Founder, via `sops/sales/QUALIFICATION.md` | Sales prepares and recommends |
| What solution to propose | **Founder**, via `sops/sales/SOLUTION_DESIGN.md` (D-010) | Sales builds the traceability matrix; Strategy may supply analysis |
| Whether a proposal may be issued | **Founder**, via `sops/sales/PROPOSAL.md` §5.1 | Sales drafts and files; issuance is never delegated |
| Website content and messaging | SEO for search intent; Design for hierarchy | Both bound by `BRAND.md` |
| Whether a deliverable is acceptable | QA verifies; **Founder accepts** | Dev and Design remediate |
| Technology selection | Dev proposes; Founder approves (`TECH_STACK.md` §3) | — |
| Whether to automate a process | Automation proposes; Founder approves | CEO identifies the candidate |
| Design versus implementation trade-off | Dev on feasibility; Design on user impact; escalate if unresolved | — |

**Rule:** if two agents disagree and this table does not resolve it, escalate.
Do not negotiate a compromise between agents — that produces a decision no
document authorized.

## 5. Universal Constraints

Binding on every agent, additional to its own definition
(`MASTER.md` §10.4):

- Never decide anything reserved in `governance/AUTHORITY.md` §7
- Never supply a value registered as `Open` in `OPEN_QUESTIONS.md`
- Never contradict `STRATEGIC_CONFIGURATION.md`
- Never state a price, timeline guarantee, or undefined deliverable
- Never claim verification that did not occur (`MASTER.md` §9.3)
- Never move client context between engagements (`MASTER.md` §7.1)
- Never edit `MASTER.md` or a Tier 2–3 document without
  `governance/CHANGE_MANAGEMENT.md`
- Never record a credential value anywhere
- Never present an assumption as a fact

## 6. Context Loading

Every agent loads `MASTER.md` and `governance/AUTHORITY.md`, plus the specific
documents named in its definition. Load the smallest sufficient set
(`MASTER.md` §5.4). The loading protocol is in `CLAUDE.md`.
