# SECURITY.md
# THE MILBOURNE GROUP
## SECURITY GOVERNANCE SOURCE OF TRUTH

**System:** Security
**Purpose:** Protect client information, company systems, credentials, and operational integrity.
**Authority:** Tier 3. Its core principles (§2, §3, §4) restate the **absolute constraints** imposed by `MASTER.md` §7 and are therefore non-negotiable — not overridable by any client, agent, deadline, or other document. Operational detail is ordinary Tier 3 and may be revised.
**Parent Authority:** `MASTER.md` (Tier 1 — supreme), §7 in particular
**Applies to:** Everyone and everything operating on behalf of the company.
**Owner:** Founder
**Status:** Active — escalation authority and response targets confirmed (D-030).
**Last reviewed:** 2026-08-29
**Review trigger:** Any incident; new tool or vendor handling client data; access change.
**Related:** `MASTER.md` §7, `AUTOMATION.md`, `clients/_CLIENT_TEMPLATE/`

---


## 1. Purpose
Protect client information, company systems, credentials, and operational integrity.

## 2. Core Principles
- Least privilege
- Minimum necessary data
- Client context isolation
- Secure defaults
- Explicit authorization
- Appropriate logging
- Prompt revocation of unnecessary access

## 3. Secrets

Never place secrets in public repositories, public documents, client-facing
content, unjustified logs, or unsecured configuration.

**Document secrets by name and location only, never by value.** A document may
state that an API key exists and where it is stored; it must never contain the
key. This applies to every file in this repository, including project
documents, briefs, and AI working notes.

Use approved secret-management mechanisms when available. If none is
available, escalate rather than improvising storage.

## 4. Client Isolation
Do not mix private information, credentials, analytics, or proprietary strategy between unrelated clients.

## 5. Access
Grant access according to task need. Review and revoke access when no longer required.

## 6. AI and External Tools
Do not send sensitive client data to an external system unless its use is authorized and appropriate for the data.

## 7. Incident Response

If a suspected security issue occurs:

1. **Limit further exposure** — revoke, rotate, or isolate first.
2. Preserve relevant evidence where appropriate.
3. **Escalate to the founder immediately.** The founder is the responsible
   authority for all security escalation (`ASSUMPTIONS.md` A-004, pending
   confirmed by D-030).
4. Never conceal, minimise, or delay reporting an issue.
5. Document facts, impact, affected parties, and remediation in `RISKS.md`.
6. Notify affected clients where obligation or integrity requires it — a
   founder decision, never an agent decision.

Suspected exposure is treated as exposure until proven otherwise.

## 8. Verification
Do not claim a system is secure merely because no problem is known.

Security requirements may need project-specific controls.
