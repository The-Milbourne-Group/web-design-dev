# AUTOMATION SPECIFICATION — <NAME>

> Template — Tier 6. Governed by `AUTOMATION.md` §4.
> **An undefined process must not be automated** (`MASTER.md` §11). Complete
> every section before implementation.

**Name:**
**Owner:** Founder
**Status:** Proposed / Active / Suspended / Retired
**Autonomy level:** 0–4 (`AUTOMATION.md` §3)
**Created:**
**Last reviewed:**
**Next review:**

---

## 1. Purpose
The outcome this produces and the work it removes.

## 2. Underlying Process
The manual process being automated. **It must be stable and documented first.**
Link the SOP if one exists.

## 3. Trigger
Exactly what starts it — schedule, event, or manual invocation.

## 4. Inputs
Required data and its source. What happens if an input is missing or malformed.

## 5. Process
Numbered steps, including decision points and their criteria.

## 6. External Systems

| System | Purpose | Permissions granted | Justification |
|---|---|---|---|
| | | | |

*Minimum necessary only (`SECURITY.md` §5). Never record credential values.*

## 7. Outputs
What is produced and where it goes.

## 8. Success Criteria
How to tell it worked — not merely that it ran.

## 9. Failure Conditions
Specific ways it can fail, including **silent** failure modes.

## 10. Failure Handling
What happens on failure. Prefer visible, recoverable failure over silent
incorrect success (`AUTOMATION.md` §7).

## 11. Recovery
Steps to recover, who executes them, and how to detect that recovery is needed.

## 12. Monitoring
What is logged, what is alerted on, who receives alerts, and how a silent
failure would be detected.

## 13. Permission Boundaries
What this automation may and may not do. Consequential actions require human
approval unless authority was deliberately delegated (`AUTOMATION.md` §6).

## 14. Value Measurement

| Measure | Estimate / Measured |
|---|---|
| Time saved per run | |
| Run frequency | |
| Failure rate | |
| Recovery time | |
| Cost | |
| Complexity | |

## 15. Review History

| Date | Reviewer | Outcome | Changes |
|---|---|---|---|
| | | | |

*Reviewed per `sops/automation/WORKFLOW_REVIEW.md`.*
