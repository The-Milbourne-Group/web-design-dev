"""The growth engine: target -> research -> fit -> outreach -> lead.

A target is a company the business identified. It is not yet a lead: nobody has
made contact and nothing has been qualified. It becomes a lead only when a
person actually engages, at which point the research already gathered is carried
into `clients/` rather than retyped.

Two disciplines carry over from the sales pipeline because they are the ones
that keep the system honest:

  - Evidence is typed. A confirmed public fact needs a source; an inference is
    labelled as one; an unknown is recorded rather than filled in.
  - Personalisation must be grounded. Every specific claim in an outreach draft
    names the evidence it rests on, and that evidence must be confirmed — the
    same control as a requirement naming its discovery finding.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import model as m


# --------------------------------------------------------------------------
# Growth pipeline states — deliberately separate from the client lifecycle in
# `clients/README.md`, which owns its own vocabulary and must not be extended.
# --------------------------------------------------------------------------

IDENTIFIED = "Identified"
RESEARCHED = "Researched"
PRIORITIZED = "Prioritized"
CONTACTED = "Contacted"
ENGAGED = "Engaged"
CONVERTED = "Converted"
MONITORING = "Monitoring"
NO_RESPONSE = "No response"
DISQUALIFIED = "Disqualified"

TARGET_STATUSES = [
    IDENTIFIED, RESEARCHED, PRIORITIZED, CONTACTED, ENGAGED, CONVERTED,
    MONITORING, NO_RESPONSE, DISQUALIFIED,
]
TARGET_TERMINAL = {CONVERTED, DISQUALIFIED, NO_RESPONSE}

TARGET_TRANSITIONS: dict[str, set[str]] = {
    IDENTIFIED: {RESEARCHED, DISQUALIFIED, MONITORING},
    RESEARCHED: {PRIORITIZED, DISQUALIFIED, MONITORING},
    PRIORITIZED: {CONTACTED, MONITORING, DISQUALIFIED},
    CONTACTED: {ENGAGED, NO_RESPONSE, MONITORING, DISQUALIFIED, CONTACTED},
    ENGAGED: {CONVERTED, MONITORING, DISQUALIFIED, NO_RESPONSE},
    MONITORING: {RESEARCHED, PRIORITIZED, CONTACTED, DISQUALIFIED},
    NO_RESPONSE: {MONITORING, CONTACTED, DISQUALIFIED},
    CONVERTED: set(),
    DISQUALIFIED: {MONITORING},
}

# Fit bands. Deliberately not a numeric score: `ICP.md` carries no weights and
# inventing them would be fake precision over an ICP that is still open
# (D-019 – D-022 set the profile; D-036 the founder advantage).
FIT_BANDS = ["Strong", "Possible", "Weak", "Not a fit"]

ACTIONS = ["Research further", "Initiate outreach", "Monitor",
           "Wait for trigger", "Disqualify"]

EVIDENCE_KINDS = ["confirmed", "inference", "unknown"]


class TargetError(Exception):
    """An operation the growth pipeline does not permit."""


# --------------------------------------------------------------------------
# Entities
# --------------------------------------------------------------------------

@dataclass
class Evidence:
    """One piece of prospect research, typed by how far it can be trusted."""
    ref: str = ""                 # E1, E2 ...
    statement: str = ""
    kind: str = "confirmed"       # confirmed | inference | unknown
    source: str = ""              # where it was observed; required if confirmed
    observed_on: str = ""


@dataclass
class Signal:
    """An ICP signal matched to the evidence that supports it."""
    signal: str = ""              # quoted from ICP.md §4/§5/§6
    kind: str = "problem"         # high_fit | problem | disqualifying | trigger
    evidence_ref: str = ""


@dataclass
class Touch:
    """One outreach attempt, from draft to outcome."""
    seq: int = 0
    channel: str = ""             # the channel actually used (D-026 priority order)
    purpose: str = ""             # the reason for contact, in one line
    draft: str = ""
    grounded_in: list[str] = field(default_factory=list)   # evidence refs
    status: str = "draft"         # draft | approved | sent | responded | no response
    drafted_on: str = ""
    approved_by: str = ""
    approved_on: str = ""
    sent_on: str = ""
    response_on: str = ""
    response_kind: str = ""       # positive | neutral | negative | none
    response_text: str = ""
    note: str = ""


@dataclass
class Fit:
    band: str = ""                # FIT_BANDS
    reasoning: str = ""
    unknowns: list[str] = field(default_factory=list)
    recommended_action: str = ""
    assessed_on: str = ""


@dataclass
class Target:
    slug: str = ""
    company: m.Company = field(default_factory=m.Company)
    contacts: list[m.Contact] = field(default_factory=list)
    identified_via: str = ""      # how this target was found — channel evidence (D-026)
    identified_on: str = ""
    campaign: str = ""            # free-text grouping, so outcomes trace to an activity
    status: str = IDENTIFIED
    research: list[Evidence] = field(default_factory=list)
    signals: list[Signal] = field(default_factory=list)
    fit: Fit = field(default_factory=Fit)
    touches: list[Touch] = field(default_factory=list)
    converted_to: str = ""        # the clients/<slug> it became
    converted_on: str = ""
    events: list[m.Event] = field(default_factory=list)
    schema_version: int = 1

    # -- lifecycle ---------------------------------------------------------

    def log(self, kind: str, detail: str = "", actor: str = "system") -> None:
        self.events.append(m.Event(at=m.now(), kind=kind, detail=detail, actor=actor))

    def set_status(self, new: str, actor: str = "system", detail: str = "") -> None:
        if new not in TARGET_STATUSES:
            raise TargetError(
                f"{new!r} is not a target status. Permitted: {', '.join(TARGET_STATUSES)}"
            )
        allowed = TARGET_TRANSITIONS.get(self.status, set())
        if new != self.status and new not in allowed:
            raise TargetError(
                f"{self.status} -> {new} is not a permitted transition. "
                f"From {self.status}: {', '.join(sorted(allowed)) or 'nothing (terminal)'}."
            )
        old, self.status = self.status, new
        self.log("status", f"{old} -> {new}. {detail}".strip(), actor)

    # -- views -------------------------------------------------------------

    def confirmed(self) -> list[Evidence]:
        return [e for e in self.research if e.kind == "confirmed"]

    def inferences(self) -> list[Evidence]:
        return [e for e in self.research if e.kind == "inference"]

    def unknowns(self) -> list[Evidence]:
        return [e for e in self.research if e.kind == "unknown"]

    def evidence(self, ref: str) -> Evidence | None:
        return next((e for e in self.research if e.ref == ref), None)

    def disqualifying(self) -> list[Signal]:
        return [s for s in self.signals if s.kind == "disqualifying"]

    def last_touch(self) -> Touch | None:
        return self.touches[-1] if self.touches else None

    def sent_touches(self) -> list[Touch]:
        return [t for t in self.touches if t.sent_on]

    def has_response(self) -> bool:
        return any(t.response_on for t in self.touches)

    def positive_response(self) -> Touch | None:
        return next((t for t in self.touches if t.response_kind == "positive"), None)

    def primary_contact(self) -> m.Contact | None:
        return self.contacts[0] if self.contacts else None


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate(t: Target) -> list[str]:
    problems: list[str] = []
    if not t.slug:
        problems.append("target has no slug")
    if t.status not in TARGET_STATUSES:
        problems.append(f"status {t.status!r} is not a permitted target status")
    if t.fit.band and t.fit.band not in FIT_BANDS:
        problems.append(f"fit band {t.fit.band!r} must be one of {', '.join(FIT_BANDS)}")
    if t.fit.recommended_action and t.fit.recommended_action not in ACTIONS:
        problems.append(f"recommended action {t.fit.recommended_action!r} "
                        f"must be one of {', '.join(ACTIONS)}")
    seen: set[str] = set()
    for e in t.research:
        if e.kind not in EVIDENCE_KINDS:
            problems.append(f"evidence {e.ref or '?'}: kind {e.kind!r} must be "
                            f"one of {', '.join(EVIDENCE_KINDS)}")
        if e.kind == "confirmed" and not e.source:
            problems.append(
                f"evidence {e.ref or '?'} is marked confirmed with no source. "
                f"A confirmed public fact names where it was observed, or it is "
                f"an inference."
            )
        if e.ref and e.ref in seen:
            problems.append(f"duplicate evidence ref {e.ref!r}")
        seen.add(e.ref)
    for s in t.signals:
        if s.evidence_ref and not t.evidence(s.evidence_ref):
            problems.append(f"signal cites evidence {s.evidence_ref!r}, which does not exist")
    for touch in t.touches:
        if touch.sent_on and not touch.approved_by:
            problems.append(f"touch {touch.seq} was sent with no recorded approval")
    return problems


# --------------------------------------------------------------------------
# Grounding — the control that prevents fabricated personalisation
# --------------------------------------------------------------------------

def grounding_problems(t: Target, touch: Touch) -> list[str]:
    """Every claim in a draft must rest on confirmed evidence."""
    problems: list[str] = []
    if not touch.grounded_in:
        problems.append(
            "The draft names no evidence. Outreach that references the prospect's "
            "situation must say which research it rests on, or the personalisation "
            "is invented (`BRAND.md` §6)."
        )
    for ref in touch.grounded_in:
        ev = t.evidence(ref)
        if ev is None:
            problems.append(f"draft cites evidence {ref!r}, which does not exist")
        elif ev.kind == "inference":
            problems.append(
                f"draft rests on {ref} — an inference, not a confirmed fact: "
                f"\"{ev.statement[:70]}\". Say it as a question, or ground the "
                f"claim in something observed."
            )
        elif ev.kind == "unknown":
            problems.append(f"draft rests on {ref}, which is recorded as unknown")
    return problems


def readiness(t: Target) -> list[str]:
    """What the target still needs before outreach can be drafted."""
    missing: list[str] = []
    if not t.confirmed():
        missing.append("at least one confirmed, sourced piece of research")
    if not t.signals:
        missing.append("at least one matched ICP signal")
    if not t.fit.band:
        missing.append("a fit assessment")
    if not t.contacts:
        missing.append("a contact to approach")
    return missing


def conversion_blockers(t: Target) -> list[str]:
    """Conversion criteria: a lead is a person who engaged, not one contacted."""
    blockers: list[str] = []
    if not t.has_response():
        blockers.append(
            "No response recorded. Contacting someone does not make them a lead — "
            "a lead is a prospect who engaged. Record the response first: "
            "`mg target respond`."
        )
    elif not t.positive_response():
        kinds = {tc.response_kind for tc in t.touches if tc.response_on}
        blockers.append(
            f"Response recorded as {', '.join(sorted(k for k in kinds if k))} — not positive. "
            f"Only a prospect who expressed interest enters the pipeline."
        )
    if t.disqualifying():
        blockers.append(
            "Disqualifying signal(s) present: "
            + "; ".join(s.signal for s in t.disqualifying())
        )
    if t.status == CONVERTED:
        blockers.append(f"Already converted to clients/{t.converted_to}.")
    return blockers
