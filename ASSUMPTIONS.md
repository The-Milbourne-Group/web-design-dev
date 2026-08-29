# ASSUMPTION REGISTER

**System:** Operations / Governance
**Purpose:** Record working assumptions that are not founder-confirmed facts, so they can be validated or retired rather than hardening into false company knowledge.
**Authority:** Tier 3. Authoritative about *what is assumed*, never about what is true.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `governance/AUTHORITY.md`
**Applies to:** Any operator relying on an unconfirmed premise.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Any assumption invalidated; evidence from the validation projects; quarterly review.
**Related:** `OPEN_QUESTIONS.md`, `DECISIONS.md`, `RISKS.md`

---

## Why This Register Exists

`MASTER.md` requires assumptions to be stated rather than presented as facts,
but the system had nowhere to put them. An assumption that lives only in a
conversation is indistinguishable from a fact the next time the document is
read.

**Rule.** When an assumption materially affects an outcome: record it here,
label it in the output, and proceed. When it is invalidated, follow the
downstream-impact list and correct what it touched.

Promotion to fact requires founder approval and a `DECISIONS.md` entry — see
`governance/CHANGE_MANAGEMENT.md` §5.

---

## Active Assumptions

### A-002 — No active client engagements at time of audit
**Assumed:** `clients/` was absent and no client documents existed, so the
system is being configured before or between engagements.

**Basis:** Repository contents at 2026-08-29.

**Consequence if wrong:** Live engagements are running without the isolation
structure required by `SECURITY.md` §4 and `MASTER.md` §7.1, and existing
client material must be migrated into `clients/` immediately.

**Validates via:** Founder confirmation.

---

### A-007 — The initial price bands are viable in the target market
**Assumed:** The D-038 bands — $5,000 minimum, $7,500–$25,000 entry, $1,500–$5,000
assessment, $750/month recurring floor — are commercially acceptable to
established small-to-mid-sized service and professional businesses.

**Basis:** D-038, set before any engagement has been sold. No market evidence
exists yet.

**Consequence if wrong:** Either opportunities are lost at the price, or margin
proves inadequate at it. Both are visible from the first three projects.

**Validates via:** The three validation projects (D-037). `sops/delivery/CLOSURE.md`
§5.6 captures delivery metrics; pricing is refined from actual margin (D-038).

---

### A-008 — Founder capacity supports one major engagement at a time
**Assumed:** One major implementation in active build, plus at most one
discovery, strategy, optimization or support engagement, is sustainable without
degrading delivery quality or starving acquisition.

**Basis:** D-037, set as a controlled launch configuration rather than measured
from delivery.

**Consequence if wrong:** Either the company under-commits and loses revenue, or
over-commits and misses delivery. D-037 forbids selling capacity on theoretical
hiring, so the error surfaces as workload, not as a broken promise.

**Validates via:** Observed delivery performance across the validation projects.

---

## Retired Assumptions

### A-004 — Founder is the escalation authority
**Assumed:** References to "the responsible authority" in `SECURITY.md` §7 and
to approval throughout the system mean the founder.

**Basis:** A-001; `STRATEGIC_CONFIGURATION.md` founder-led operating model.

**Consequence if wrong:** Incident response and approval routing are
misdirected.

**Validated by:** D-030.

**Retired 2026-08-29** — confirmed by D-030: the founder is the named escalation authority, with response targets.

---

### A-005 — "Established SMB" is not yet quantified
**Assumed:** The confirmed client category (D-006) carries no numeric size
band, so qualification uses the qualitative signals in `ICP.md` §3–§4 rather
than thresholds.

**Basis:** D-006 confirmed the category before D-021 set the bands.

**Consequence if wrong:** If the founder has an implicit size band in mind,
qualification will admit opportunities the founder would reject.

**Validated by:** D-021.

**Retired 2026-08-29** — superseded by D-021, which sets explicit size bands. Qualification no longer relies on qualitative signals alone.

---

### A-001 — Solo founder-operated company
**Assumed:** The company is currently operated by the founder alone, supported
by AI systems and flexible specialist capacity. There are no employees.

**Basis:** `STRATEGIC_CONFIGURATION.md` operating direction; D-010; D-011.

**Consequence if wrong:** Ownership fields naming "Founder" throughout the SOP
library would need reassignment; approval routing and segregation-of-duties
controls would need to be introduced.

**Validated by:** D-024, superseded by D-037.

**Retired 2026-08-29** — confirmed by D-037: the founder is the primary strategic and delivery authority, with specialist capacity used where commercially justified. Capacity limits are now policy, not assumption.

---

### A-003 — Currency and jurisdiction unspecified
**Assumed:** No currency, tax jurisdiction, or governing legal jurisdiction has
been recorded, so no document states one.

**Basis:** Absent from every source document.

**Consequence if wrong:** Proposal and agreement templates need jurisdiction-
specific commercial and legal terms before client use.

**Validates via:** Founder confirmation before the first proposal is issued.

**Retired 2026-08-29** — resolved by D-038: all figures are USD. Tax and governing legal jurisdiction remain unstated and are tracked as R-010 rather than as an assumption.

---

### A-006 — Audit-era interpretation of the entry offer
**Assumed:** "Strategic Website & Digital Foundation" (D-005) means an
engagement combining discovery, strategy, architecture, content planning,
design, development, QA, and launch — mapping to the former `SERVICES.md` §2.4
"Strategic Website Projects".

**Basis:** Closest existing service definition; consistent with the
progression in D-005.

**Consequence if wrong:** `SERVICES.md` entry-offer scope is misdescribed and
proposals would misrepresent the engagement.

**Validated by:** D-029 and D-038.

**Retired 2026-08-29** — superseded by D-029 and D-038, which define the entry offer's stage structure and its $7,500–$25,000 range directly. `SERVICES.md` §2.1 and §2.4 are now the source, not an interpretation.

---
