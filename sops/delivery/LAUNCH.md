# SOP: LAUNCH

**System:** Delivery
**Purpose:** Take a deliverable live safely, verifiably, and reversibly.
**Authority:** Tier 4 procedure.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), `DELIVERY.md` §8
**Applies to:** Every production launch or major release.
**Owner:** Founder
**Status:** Active
**Last reviewed:** 2026-08-29
**Review trigger:** Any launch incident; hosting or stack change.
**Related:** `sops/delivery/QA.md`, `WEB_STANDARDS.md`, `SECURITY.md`, `TECH_STACK.md`

---

## 1. Purpose

Launch without breaking what already works, with the ability to reverse the
change, and with verification that the site actually functions in production.

## 2. Trigger

QA passed, client approval obtained, and a launch window agreed.

## 3. Owner

Founder. Launch authorization is a founder decision — it is an irreversible,
externally visible action (`MASTER.md` §7.4).

## 4. Inputs

- QA verification record showing no outstanding Blockers
- Written client approval to launch
- Production environment access
- Rollback plan
- Current production backup

## 5. Procedure

### Before launch

1. **Confirm QA passed** with no outstanding Blockers, and confirm written
   client approval exists.

2. **Back up current production** — files, database, and configuration.
   Verify the backup is restorable. An unverified backup is not a backup.

3. **Write the rollback plan**: exact steps to restore, who executes them, and
   the decision criteria for rolling back. Do this *before* launching, not
   while an incident is in progress.

4. **Verify configuration** for the production environment: environment
   variables, API endpoints, third-party keys present and correct, debug
   disabled, correct domain and SSL. Confirm no development or staging
   references remain.

5. **Confirm the launch window** avoids the client's peak business period, and
   confirm someone is available afterward to respond.

### Launch

6. **Deploy** following the repository's documented procedure.

7. **Verify DNS, SSL, and redirects.** Preserve existing URLs — broken
   redirects silently destroy accumulated search visibility, and the damage is
   not visible on the site itself.

### After launch

8. **Verify critical functionality in production.** Homepage and key pages,
   primary conversion path, forms end to end (confirm the submission
   *arrives*), integrations, and mobile.

9. **Verify analytics and monitoring** are recording live data.

10. **Verify search visibility basics**: robots directives permit indexing,
    sitemap present and correct, canonical tags correct, no staging
    `noindex` left in place.

11. **Monitor** for the agreed period — errors, traffic, form submissions,
    performance.

12. **Confirm launch with the client** in writing, including known
    limitations, what to watch for, and how to report an issue.

13. **Record the launch**: date, what shipped, known limitations, monitoring
    in place, and ownership of ongoing responsibility.

## 6. Outputs

- Live deliverable, verified in production
- Verified backup and a tested rollback path
- Production verification record
- Analytics and monitoring confirmed live
- Written client launch confirmation
- Launch record with known limitations

## 7. Quality Checks

- [ ] Backup taken **and** verified restorable before deploying.
- [ ] Rollback plan written before launch.
- [ ] Written client approval on file.
- [ ] Critical paths verified **in production**, not only staging.
- [ ] A form submission was confirmed to arrive at its destination.
- [ ] Redirects preserve existing URLs.
- [ ] No staging `noindex` or debug mode remains.
- [ ] Analytics recording live data.

## 8. Failure Conditions & Recovery

| Failure | Recovery |
|---|---|
| Critical functionality broken in production | Execute rollback; diagnose outside production; do not debug live under pressure |
| Forms not delivering | Treat as a Blocker — lost enquiries are unrecoverable revenue; roll back or fix immediately |
| Redirects missed | Fix immediately; search visibility degrades daily |
| Staging `noindex` shipped | Fix immediately; the site is invisible to search until corrected |
| Backup missing or unverified | Do not launch |
| Client reports an issue post-launch | Reproduce, assess severity, communicate a timeline, fix, verify |

## 9. Escalation

Escalate before proceeding when: QA has outstanding Blockers; client approval
is absent; no verified backup exists; rollback is not possible; a security
concern appears; or launch would occur without post-launch availability.

## 10. Automation Potential

**Can be assisted:** deployment pipelines, backup automation, configuration
checks, automated smoke tests, uptime and error monitoring, redirect
verification.

**Must not be automated:** launch authorization, the go/no-go decision, and
client communication. Automated deployment still requires a human decision to
release (`AUTOMATION.md` §6).
