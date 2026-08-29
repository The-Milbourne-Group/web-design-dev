# SYSTEM QA

**System:** Governance
**Purpose:** Verify the operating system remains structurally, strategically, operationally, and securely consistent.
**Authority:** Tier 3 governance.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), §9 in particular
**Applies to:** Anyone completing substantive work on this repository; quarterly full review.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** New failure mode; check proving ineffective.
**Related:** `governance/CHANGE_MANAGEMENT.md`, `governance/DOCUMENT_REGISTRY.md`, `MASTER.md` §9

---

## 1. When to Run

| Trigger | Scope |
|---|---|
| Before declaring substantive work complete | §3 Fast Check |
| After any Strategic change | §3 and §4, full |
| Quarterly | Everything, plus stale review dates |

`MASTER.md` §9.3 applies to this document as it does to everything else:
report what was actually checked, and state what was not.

---

## 2. The Standard That Matters

The completion standard is **not** "all files were reviewed." It is:

> The system has one authority, no competing sources of truth, no fabricated
> facts, executable procedures, and defined boundaries.

---

## 3. Fast Check

Run before completing substantive work. Minutes, not hours.

- [ ] Every document I changed still matches its higher-tier parent.
- [ ] I did not supply any value registered as `Open` in `OPEN_QUESTIONS.md`.
- [ ] Any assumption I relied on is recorded in `ASSUMPTIONS.md` and labelled
      in the output.
- [ ] Documents I changed do not now contradict their dependents
      (`governance/DOCUMENT_REGISTRY.md`).
- [ ] No credential value, client-identifying detail, or cross-client context
      entered a company document.
- [ ] Every claim of verification I made is true.

---

## 4. Full Review

### 4.1 Structural Integrity

- [ ] Every internal document reference resolves to a file that exists.
- [ ] No subject has two owners (`DOCUMENT_REGISTRY.md` §7).
- [ ] No document is orphaned — every file is reachable from `README.md`,
      `SYSTEM_MAP.md`, or an index.
- [ ] Every governance and domain document carries the metadata block.
- [ ] `Last reviewed` dates are not stale relative to review triggers.

```bash
# Broken internal references.
# governance/DOCUMENT_REGISTRY.md is excluded: its "Retired" section
# intentionally names documents that no longer exist.
grep -rhoE '`[A-Za-z0-9_/.-]+\.md`' --include=*.md \
     --exclude=DOCUMENT_REGISTRY.md . | tr -d '`' | sort -u \
  | while read -r f; do
      [ -e "$f" ] || find . -name "$(basename "$f")" -not -path './.git/*' \
        | grep -q . || echo "MISSING: $f"
    done

# Stale MASTER.md section references (must resolve, or be marked "former")
grep -rhoE '`MASTER\.md` §[0-9]+(\.[0-9]+)?' --include=*.md . \
  | grep -oE '[0-9]+(\.[0-9]+)?' | sort -u -V \
  | while read -r s; do
      grep -qE "^#{1,2} ${s}[ .]*$|^#{1,2} ${s} " MASTER.md \
        || echo "CHECK: MASTER.md §${s} (must be marked 'former')"
    done

# Governance and domain documents missing the metadata block.
# templates/ and clients/_CLIENT_TEMPLATE/ use fill-in headers by design
# and carry no authority, so they are excluded.
for f in $(find . -maxdepth 2 -name '*.md' -not -path './.git/*' \
           -not -path './templates/*' -not -path './clients/*' \
           -not -name 'README.md'); do
  grep -q '^\*\*Authority:\*\*' "$f" || echo "NO METADATA: $f"
done
```

### 4.2 Strategic Integrity

- [ ] No document contradicts `STRATEGIC_CONFIGURATION.md`.
- [ ] No document describes the company as AI-first or leads with AI as the
      value proposition (D-002).
- [ ] Services trace to the confirmed progression (D-005).
- [ ] ICP aligns with the confirmed client category (D-006).
- [ ] Sales and marketing align with ICP and positioning.
- [ ] Delivery can actually deliver what sales is permitted to promise.
- [ ] No confirmed decision appears anywhere as an open configuration item
      (D-014).

```bash
grep -rniE 'AI-first|AI-native|AI-powered agency' --include=*.md . | grep -v DECISIONS.md | grep -v RISKS.md
```

### 4.3 Operational Integrity

- [ ] Every SOP has all ten required elements (`SOP_INDEX.md` §3).
- [ ] Every SOP has a named owner and a last-reviewed date.
- [ ] Templates support the SOPs that reference them.
- [ ] Every SOP referenced by an agent or index exists.
- [ ] Approval boundaries are stated wherever a consequential action occurs.

### 4.4 AI Integrity

- [ ] Every agent definition has all ten elements from `MASTER.md` §10.2.
- [ ] No two agents claim authority over the same decision
      (`agents/README.md` §4).
- [ ] Every agent names the documents it must load.
- [ ] Every agent states forbidden actions and escalation triggers.
- [ ] No agent can grant itself a right reserved in
      `governance/AUTHORITY.md` §7.

### 4.5 Security Integrity

- [ ] No secret values anywhere — names and locations only.
- [ ] No client-identifying information in company documents.
- [ ] Client directories contain no cross-references to other clients.
- [ ] External AI and tool usage respects `SECURITY.md` §6.

```bash
# Candidate secret values (expect zero hits)
grep -rniE '(api[_-]?key|secret|password|token|bearer)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9/_+-]{12,}' \
  --include=*.md . || echo "clean"
```

---

## 5. Recording Results

Record a full review as a dated entry in this section: what was checked, what
failed, and what was corrected. A review that found nothing is still worth
recording — it establishes when the system was last known good.

### 2026-08-29 — Post-audit baseline

**Checked:** all four full-review categories across 60 documents.

**Corrected during the audit:**
four competing precedence statements reduced to one; `MASTER.md` self-
contradiction between §1.1 and §5.1 resolved; AI-first identity removed from
`MASTER.md` §2.1 and `BUSINESS.md` §2; delivery lifecycle deduplicated;
metric, automation-level, and implementation-standard duplication removed;
confirmed geography removed from open-configuration lists; all eight SOPs
rebuilt to the ten-element standard; all eight agents rebuilt to `MASTER.md`
§10.2; `DECISIONS.md`, `OPEN_QUESTIONS.md`, `ASSUMPTIONS.md`, `RISKS.md`,
`GLOSSARY.md`, `SOP_INDEX.md` created; `clients/_CLIENT_TEMPLATE/` created.

**Not verified:** the accuracy of founder-approved strategy itself — this
system records the founder's decisions, it does not validate them. Nine items
remain open by design (`OPEN_QUESTIONS.md`).

### 2026-08-29 — Second integration test (commercial chain)

**Checked:** cold-start orientation against the ten orientation questions; the
ten end-to-end scenarios re-run against the post-remediation system; all eight
agents; adversarial cases; and two new mechanical checks — every `DOC.md §N`
cross-reference resolved to a real section or numbered step, and every declared
client `Status` traced to the procedure that assigns it.

**Baseline confirmed clean:** file references resolve, metadata complete, no
secret values, no AI-first positioning, 11/11 SOPs and 8/8 agents at standard.

**Failures found and fixed:**

| ID | Severity | Defect | Fix |
|---|---|---|---|
| P0-7 | System breaking | The proposal — the only binding client-facing commercial document — had no procedure and no artifact location. `SYSTEM_MAP.md` §3 named a *template* in its Procedure column; the sole control against a fabricated price was a blockquote in a Tier 6 template, which carries no authority. Onboarding and scope change both reconcile against "what was sold", which was never filed. `METRICS.md` §4 mandated two proposal metrics that nothing recorded. | D-018 |
| P1-8 | High | `Active`, `Launched`, and `Lost` were declared statuses that no procedure assigned; `Clarification required` was a qualification outcome absent from the vocabulary | Status-assignment table in `clients/README.md`; steps added to `ONBOARDING.md`, `LAUNCH.md`, `PROPOSAL.md` |
| P1-9 | High | Two differing client lifecycles — `SYSTEM_MAP.md` §6 included `Solution` and `Agreement`; `clients/README.md` included `Active`, `Launched`, `Closed`. Neither was registered as owner | `clients/README.md` registered as sole owner of the vocabulary; `SYSTEM_MAP.md` aligned and scoped to flow |
| P2-10 | Friction | `CLOSURE.md` §5.11 cited `SOLUTION.md` §5 (Feasibility) for deferred items, which are §4 — expansion review pointed at the wrong section | Corrected |

**Surfaced, not fixed — requires founder decision:** `SERVICES.md` §4 forbids
presenting an offer without a pricing model and defined deliverables. Q-007 and
Q-011 left both open at the time. *(Superseded 2026-08-29: D-038 sets the price
points and `SERVICES.md` §2.4 satisfies §4. Retained as the record of the
finding.)* **At the time of this review no proposal could be issued that satisfied
`SERVICES.md` §4.** The commercial chain is executable up to solution design and
then blocked by an undecided value, not by a documentation gap.
`sops/sales/PROPOSAL.md` §9 makes this a standing escalation rather than
something discovered mid-engagement.

**Regression:** re-ran all checks after remediation. One defect introduced
during remediation (a dangling `templates/README.md` §3 reference, that file
having no numbered sections) was caught and corrected. Final state: every live
cross-reference resolves to an existing section or step; the only three
unresolved are explicitly marked "former" and are intentional history; 12/12
SOPs at the ten-element standard; 11/11 statuses assigned by a named procedure.

**Not verified:** the SOPs remain untested against a live engagement — this
round tested the system against itself, not against reality. `PROPOSAL.md` in
particular has never been executed, and its issuance gate has never been run
against a real commercial decision. Treat the first real pass through it as a
draft to correct.

### 2026-08-29 — Integration and execution test

**Checked:** orientation from a cold start; ten end-to-end business scenarios
(lead, discovery, solution design, proposal, onboarding, delivery, scope
change, conflicting knowledge, missing information, closure); all eight agents
for context, authority, output, escalation, and overlap; eleven adversarial
cases.

**Failures found and fixed:**

| ID | Severity | Defect | Fix |
|---|---|---|---|
| P0-1 | System breaking | Qualification and discovery artifacts had no storage location; placement rule routed them to "do not file"; `ICP.md` §7 buyer evidence had nowhere to accumulate | D-015 |
| P1-2 | High | Discovery→proposal step undocumented; no SOP, no owner — the entry point for fabricated scope | D-016 |
| P1-3 | High | No closure procedure; access left granted, no measurement baseline, confirmed expansion strategy had no operational trigger | D-017 |
| P1-4 | High | `SERVICES.md` §5 pointed to `DELIVERY.md` §5 for change orders, which did not define them; `DELIVERY.md` had no route to `SCOPE_CHANGE.md` | Both corrected to point at the SOP |
| P2-5 | Friction | `DELIVERY.md` §6 quality gates named no verifier and no standard | Phase gate table added |
| P2-6 | Friction | `CLAUDE.md` §3 had no fallback when no loading row matched; `SECURITY.md` framed as conditional | Fallback and always-applies note added |

**Regression:** all fixes re-tested. One defect introduced during remediation
(`SOLUTION.md` referenced before the template existed) was caught by the
broken-reference check and corrected. Full suite clean: references resolve,
metadata complete, no secret values, 8/8 agents and 11/11 SOPs at standard.

**Not verified:** SOPs remain untested against a live engagement. They are
constructed from the domain documents, not transcribed from observed practice
— treat the first real pass through each as a draft to correct.
