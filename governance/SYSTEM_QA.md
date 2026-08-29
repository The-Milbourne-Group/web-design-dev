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
