# AUTHORITY MODEL

**System:** Governance
**Purpose:** Define the single authority hierarchy for The Milbourne Group operating system, the rule for resolving conflicts between documents, and who may change what.
**Authority:** Derived from `MASTER.md` §5, which delegates the precedence model to this document. It supersedes any conflicting precedence statement elsewhere in the repository, and is itself subordinate to `MASTER.md`.
**Parent Authority:** `MASTER.md` — the ultimate authority in this system.
**Applies to:** Every document, agent, automation, and human operator in this repository.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Any change to the document set, any new authority tier, any unresolved conflict escalation.
**Related:** `MASTER.md`, `STRATEGIC_CONFIGURATION.md`, `governance/DOCUMENT_REGISTRY.md`, `governance/CHANGE_MANAGEMENT.md`

---

## 1. Why This Document Exists

Before this document, the repository contained four incompatible precedence
statements:

| Source | Claimed top authority |
|---|---|
| `MASTER.md` §1.1 | `MASTER.md` is "the root operating constitution" |
| `MASTER.md` §5.1 | Domain documents (Level 4) rank **above** `MASTER.md` (Level 5) |
| Package README | `STRATEGIC_CONFIGURATION.md`, then the `.docx`; `MASTER.md` unranked |
| `STRATEGIC_CONFIGURATION.md` | Itself and the `.docx` supersede "legacy operating-system files" |

An operator could justify almost any decision by selecting a precedence
statement. This document replaces all four. Where an older statement survives
anywhere in the repository, this document wins.

---

## 2. The Supremacy of MASTER.md

**`MASTER.md` is the ultimate authority in this system.** Nothing outranks it.
Every other document — this one included — derives its standing from it.

This has a consequence worth stating plainly, because it is what makes the
model safe: **the absolute constraints are absolute because `MASTER.md` makes
them so.** Law, executed contracts, security, safety, and client
confidentiality bind every operator — not because they sit above the
constitution, but because `MASTER.md` §7 imposes them and forbids any
lower-tier document, client request, agent instruction, or deadline from
suspending them.

`MASTER.md` therefore cannot be cited to justify violating them. An operator
claiming "MASTER is supreme, so I may override this security rule" has
misread it: the rule *is* MASTER's. The constitution constrains itself.

Likewise, `MASTER.md` §2 delegates authority over *what the business is* —
identity, positioning, market, offers, pricing — to founder-approved decision.
That delegation is why Tier 2 binds domain documents.

---

## 3. The Two Dimensions of Authority

Authority is not a single ranking. Resolve conflicts on two dimensions, in
this order.

### 3.1 Tier — how binding a document is

Tiers are absolute. A lower tier never overrides a higher tier.

### 3.2 Scope — what subject a document is entitled to govern

A document has authority **only over its declared subject**. A client
agreement is authoritative about that engagement's deliverables; it is not
authoritative about company security policy. `BRAND.md` is authoritative about
voice; it is not authoritative about pricing.

**Rule of Scope:** Within a single subject, the most specific document at the
highest applicable tier wins. Outside its subject, a document has no authority
at all.

This resolves the defect in the superseded `MASTER.md` §5.1, which ranked
client requirements near the top of a single global ladder and therefore
implied a client could override company policy. They cannot.

---

## 4. The Authority Hierarchy

### Tier 1 — MASTER.md — The Operating Constitution

**Supreme.** Universal principles, execution protocol, quality standards,
uncertainty handling, authorization boundaries, agent governance, and the
absolute constraints of §7.

`MASTER.md` outranks every other document in this repository on every subject
it addresses. Where it delegates a subject — strategy to Tier 2, domain
substance to Tier 3 — that delegation is itself an exercise of its authority
and is honoured accordingly (§5).

Changing `MASTER.md` requires founder approval.

### Tier 2 — Founder-Approved Strategic Decisions

What the business **is**: identity, positioning, market, offer architecture,
commercial model, and any decision recorded as `Confirmed`.

Documents: `STRATEGIC_CONFIGURATION.md`, `DECISIONS.md` (entries with status
`Confirmed`).

Tier 2 governs strategy because `MASTER.md` §2 places identity and positioning
under founder decision. Where a Tier 3+ document contradicts a confirmed
founder decision, the lower document is **wrong and must be corrected**, not
reinterpreted.

Where Tier 2 and `MASTER.md` genuinely conflict, `MASTER.md` wins — and the
conflict is itself a defect to escalate, because the constitution should not
be describing strategy the founder has not approved. *(This case occurred:
`MASTER.md` §2.1 asserted an AI-first identity contradicting founder-approved
positioning. It was resolved by correcting `MASTER.md`, not by demoting the
founder's decision — see `DECISIONS.md` D-002.)*

### Tier 3 — Domain Sources of Truth

Authoritative knowledge for one business area.

`BUSINESS.md`, `BRAND.md`, `SERVICES.md`, `ICP.md`, `MARKETING.md`,
`SALES.md`, `DELIVERY.md`, `WEB_STANDARDS.md`, `TECH_STACK.md`,
`AUTOMATION.md`, `SECURITY.md`, `METRICS.md`, `ROADMAP.md`, and the registers
(`OPEN_QUESTIONS.md`, `ASSUMPTIONS.md`, `RISKS.md`, `GLOSSARY.md`).

Each is the **single** source of truth for its subject.
`governance/DOCUMENT_REGISTRY.md` records which document owns which subject;
two documents must never both claim one subject.

`SECURITY.md` is a special case: its core principles restate absolute
constraints imposed by `MASTER.md` §7 and are therefore non-negotiable, while
its operational detail is ordinary Tier 3 and may be revised.

### Tier 4 — Procedural Knowledge

`sops/`, indexed by `SOP_INDEX.md`. SOPs implement domain policy. An SOP may
add operational detail; it may never introduce policy its parent domain
document does not support.

### Tier 5 — Agent Instructions

`agents/`, indexed by `agents/README.md`. Agents execute within the tiers
above. Specialization grants **capability**, not **authority**.

### Tier 6 — Reusable Assets

`templates/`. Starting points only. A template is never evidence that its
content is correct or complete for a given engagement.

### Tier 7 — Project and Client Knowledge

`clients/`, plus `CLAUDE.md` files in client codebases.

Authoritative **within its engagement** for scope, requirements, and
implementation detail. Always subordinate to the absolute constraints of
`MASTER.md` §7. Never modifies company-level documents — see §5.

### Tier 8 — Temporary Working Artifacts

Drafts, research notes, unreviewed AI output, session scratch work. Carries no
authority. Never cite one as a source of truth. Promote it under
`governance/CHANGE_MANAGEMENT.md` or discard it.

---

## 5. Constitution vs. Domain: How Delegation Works

`MASTER.md` is supreme, but it is deliberately thin. It governs *how the
company operates* and delegates *what is true in a domain* to Tier 3.

| Question | Authority |
|---|---|
| How do we work, verify, escalate, and decide? | `MASTER.md` |
| What has the founder decided the business is? | Tier 2 |
| What is true about sales / brand / delivery / security? | The Tier 3 owner |

**Resolution rule.** On operating conduct, authority, verification honesty,
absolute constraints, and escalation, `MASTER.md` governs directly. On the
substance of a domain, the Tier 3 owner governs — under delegation, not in
competition. If a domain document attempts to weaken an operating rule in
`MASTER.md`, `MASTER.md` wins and the domain document is defective.

`MASTER.md` must not itself hold domain content. Where it does, it has
absorbed something that belongs elsewhere and should be relocated (§1.3 of
`MASTER.md`).

---

## 6. Direction of Change

Knowledge flows **down** the hierarchy. Changes flow **up** only through
governance.

```
Tier 1  MASTER.md  ── delegates strategy ──►  Tier 2  Founder decisions
   │                                              │
   │  governs conduct                             │  governs identity
   ▼                                              ▼
Tier 3  Domain source of truth  ◄─────────────────┘
   │  informs
   ▼
Tier 4  SOPs ──► Tier 5 Agents ──► Tier 6 Templates
                       │
                       ▼
                 Tier 7 Project execution
                       │  evidence
                       ▼
              CHANGE_MANAGEMENT.md  ──► proposes change upward
```

A project must never silently edit a company document. Evidence discovered
during delivery is raised as a change proposal, not applied in place.

## 7. Decision Rights

### Reserved to the founder — never decided by an agent

- Strategic positioning, identity, and market selection
- Ideal client profile and target market
- Service definitions and offer architecture
- Pricing, minimum engagement, discounts, and commercial terms
- Any financial commitment or contractual obligation
- Legal obligations and risk acceptance
- Brand identity, official visual system, and public claims
- Hiring, subcontracting, and capacity commitments
- Major technology commitments and vendor selection
- Changes to `MASTER.md`, or to any Tier 2 or Tier 3 document
- Granting an automation Level 3 or Level 4 autonomy
- Anything irreversible, externally visible, or client-facing

### Delegated to agents and operators — decide and proceed

- Applying an existing documented policy to a specific case
- Drafting artifacts for founder review
- Analysis, research, and recommendations
- Tier 4–8 work that follows an existing SOP
- Editorial correction of a document to match a higher-tier document
- Flagging a conflict, gap, assumption, or risk into a register

### Requires approval before action

- Any change to a Tier 3 document's substance
- Any new SOP, agent, or template
- Any client-facing communication or commitment
- Any action listed in `MASTER.md` §7.4 (authorization boundaries)

**Default rule:** If a decision is not clearly delegated, it is reserved.
Escalate rather than assume.

---

## 8. Conflict Resolution Procedure

When two instructions conflict:

1. **Identify** the exact conflicting statements and their source documents.
2. **Check the absolute constraints.** If either statement implicates law,
   contract, security, safety, or confidentiality, `MASTER.md` §7 resolves it
   immediately and no further analysis is needed.
3. **Apply scope.** Determine whether each document is entitled to govern the
   subject. A document outside its scope is discarded, whatever its tier.
4. **Apply tier.** Among documents entitled to the subject, the highest tier
   wins.
5. **Apply specificity.** Within the same tier and subject, the more specific
   document wins.
6. **If still unresolved,** do not guess. Record the conflict in
   `OPEN_QUESTIONS.md`, proceed with the most conservative interpretation, and
   escalate to the founder.
7. **Repair the source.** A resolved conflict is not finished until the
   defective document is corrected under `governance/CHANGE_MANAGEMENT.md`.
   Resolving a conflict in conversation and leaving the contradiction on disk
   guarantees it recurs.

Never silently ignore a material contradiction.

---

## 9. Worked Examples

**A document says the company is "AI-first"; `STRATEGIC_CONFIGURATION.md`
says the company must not position as an AI agency.**
Strategy is delegated to founder decision by `MASTER.md` §2, so the
founder-approved positioning governs and the conflicting document is
defective. *(This was a real defect in `MASTER.md` §2.1 and `BUSINESS.md` §2.
Because `MASTER.md` is supreme, the fix was to correct `MASTER.md` itself —
resolved 2026-08-29, `DECISIONS.md` D-002.)*

**A client asks for a tracking script that sends personal data to an
unvetted third party.**
Tier 7 versus the absolute constraints of `MASTER.md` §7. The constraints win.
Decline, explain, propose a compliant alternative, escalate. The client's
authority over their engagement does not extend to overriding security
policy.

**`SALES.md` and an SOP describe different qualification steps.**
Tier 3 beats Tier 4. `SALES.md` governs; the SOP is corrected to match.

**An agent definition grants itself pricing authority.**
Tier 5 cannot hold a right reserved in §7. The grant is void; the agent file
is defective.

**A delivery retrospective shows the documented QA gate is unworkable.**
Valid evidence, wrong direction. The project does not edit `DELIVERY.md`. It
raises a change proposal under `governance/CHANGE_MANAGEMENT.md`.

---

## 10. Status Vocabulary

Every factual claim in this system carries one of four statuses. Agents must
preserve these labels and must never promote a claim to a higher status
without founder approval.

| Status | Meaning | May an agent rely on it? |
|---|---|---|
| **Confirmed** | Founder-approved decision | Yes, as fact |
| **Provisional** | Working direction, not finally approved | Yes, labelled as provisional |
| **Open** | Registered in `OPEN_QUESTIONS.md`, undecided | No — must not be filled with an invented answer |
| **Deprecated** | Superseded; retained for history | No |

Fabricating a value for an `Open` item is the single most damaging failure
mode in this system. When an operator needs an open value, it states the
dependency and stops — it does not invent a niche, a price, or a client
profile.
