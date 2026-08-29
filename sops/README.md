# SOP LIBRARY

**System:** Operations
**Purpose:** Directory of standard operating procedures.
**Authority:** Tier 4 index.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `SOP_INDEX.md`
**Applies to:** Anyone executing a documented procedure.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** SOP added or retired.
**Related:** `SOP_INDEX.md`

---

The catalogue, routing table, structure standard, and writing rules live in
**`SOP_INDEX.md`**, which is their single source of truth. Start there.

```
sops/
├── sales/       QUALIFICATION, DISCOVERY
├── delivery/    ONBOARDING, SCOPE_CHANGE, QA, LAUNCH
├── operations/  DECISION_LOG, DOCUMENTATION
└── automation/  WORKFLOW_REVIEW
```

SOPs are Tier 4: they implement the policy set by Tier 3 domain documents.
An SOP may add operational detail; it may never introduce policy its parent
document does not support.
