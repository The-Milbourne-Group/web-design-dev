"""Entities and the stage machine for the commercial pipeline.

The record is the single source of truth for an opportunity. Every markdown
artifact the SOPs require is rendered from it, so no fact is ever typed twice.

Statuses and their assigning procedures are defined in `clients/README.md`.
"""
from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field, asdict, fields, is_dataclass
from typing import Any


SCHEMA_VERSION = 1


def today() -> str:
    return _dt.date.today().isoformat()


def now() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat()


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "unnamed"


# --------------------------------------------------------------------------
# Status vocabulary — clients/README.md is the sole owner of these values.
# --------------------------------------------------------------------------

PROSPECT = "Prospect"
QUALIFIED = "Qualified"
DISCOVERY = "Discovery"
PROPOSAL = "Proposal"
ONBOARDING = "Onboarding"
ACTIVE = "Active"
LAUNCHED = "Launched"
CLOSED = "Closed"
DISQUALIFIED = "Disqualified"
NURTURE = "Nurture"
LOST = "Lost"

STATUSES = [
    PROSPECT, QUALIFIED, DISCOVERY, PROPOSAL, ONBOARDING,
    ACTIVE, LAUNCHED, CLOSED, DISQUALIFIED, NURTURE, LOST,
]

TERMINAL = {DISQUALIFIED, NURTURE, LOST, CLOSED}

# Which procedure assigns each status (clients/README.md status table).
ASSIGNED_BY = {
    PROSPECT: "sops/sales/QUALIFICATION.md §5.1",
    QUALIFIED: "sops/sales/QUALIFICATION.md §6",
    NURTURE: "sops/sales/QUALIFICATION.md §6 / sops/sales/PROPOSAL.md §5.9",
    DISQUALIFIED: "sops/sales/QUALIFICATION.md §6",
    DISCOVERY: "sops/sales/DISCOVERY.md §6",
    PROPOSAL: "sops/sales/SOLUTION_DESIGN.md §6",
    LOST: "sops/sales/PROPOSAL.md §5.9",
    ONBOARDING: "sops/delivery/ONBOARDING.md §5.1",
    ACTIVE: "sops/delivery/ONBOARDING.md §5.11",
    LAUNCHED: "sops/delivery/LAUNCH.md §5.13",
    CLOSED: "sops/delivery/CLOSURE.md §5.12",
}

# Legal forward moves. Terminal states are reachable from most live stages.
TRANSITIONS: dict[str, set[str]] = {
    PROSPECT: {QUALIFIED, NURTURE, DISQUALIFIED, PROSPECT},
    QUALIFIED: {DISCOVERY, NURTURE, DISQUALIFIED},
    DISCOVERY: {PROPOSAL, NURTURE, DISQUALIFIED, LOST},
    PROPOSAL: {ONBOARDING, PROPOSAL, LOST, NURTURE},
    ONBOARDING: {ACTIVE, LOST},
    ACTIVE: {LAUNCHED, CLOSED},
    LAUNCHED: {CLOSED},
    CLOSED: set(),
    DISQUALIFIED: {PROSPECT},   # re-open: QUALIFICATION.md §8 permits a second look
    NURTURE: {PROSPECT},        # reactivated lead is a qualification trigger
    LOST: {PROSPECT},
}


class StageError(Exception):
    """A transition the documented lifecycle does not permit."""


class ApprovalRequired(Exception):
    """A founder decision that governance/AUTHORITY.md §7 reserves."""


class OpenValueError(Exception):
    """An attempt to supply a value registered Open in OPEN_QUESTIONS.md."""


# --------------------------------------------------------------------------
# Entities
# --------------------------------------------------------------------------

@dataclass
class Contact:
    name: str = ""
    role: str = ""            # as stated by them; never inferred (D-021 lists expected roles)
    email: str = ""
    phone: str = ""
    is_decision_maker: bool | None = None   # None = not yet established
    notes: str = ""


@dataclass
class Company:
    name: str = ""
    website: str = ""
    industry: str = ""
    approximate_size: str = ""   # free text; no bands exist (A-005)
    location: str = ""
    notes: str = ""


@dataclass
class Fit:
    """ICP assessment. Signals are quoted from ICP.md §4-§6, never invented."""
    high_fit_signals: list[str] = field(default_factory=list)
    problem_signals: list[str] = field(default_factory=list)
    disqualifying_signals: list[str] = field(default_factory=list)
    stage: str = ""              # SERVICES.md §2: Entry / Expansion / Recurring
    feasible: bool | None = None
    reasoning: str = ""


@dataclass
class Qualification:
    source: str = ""             # channel evidence (D-026)
    problem: str = ""            # in the prospect's own words
    desired_outcome: str = ""
    authority_confirmed: bool | None = None
    fit: Fit = field(default_factory=Fit)
    # Kept apart deliberately: what the record actually supports, versus the
    # reading placed on it. An assessment must never harden into a fact.
    confirmed_facts: list[str] = field(default_factory=list)
    assessment: str = ""
    recommended_outcome: str = ""
    recommended_next_action: str = ""
    outcome: str = ""            # Qualified | Nurture | Clarification required | Disqualified
    outcome_reasoning: str = ""
    open_items: list[str] = field(default_factory=list)
    decided_by: str = ""
    decided_on: str = ""


@dataclass
class Finding:
    """One discovery finding. `confirmed` is the fact/assumption boundary."""
    ref: str = ""                # D1, D2 ... referenced by requirement sources
    topic: str = ""
    statement: str = ""
    confirmed: bool = True       # False => inference/assumption, must be labelled
    source: str = ""             # who said it, or what it was inferred from


@dataclass
class Discovery:
    scheduled_for: str = ""
    held_on: str = ""
    attendees: list[str] = field(default_factory=list)
    agenda: list[str] = field(default_factory=list)
    transcript_path: str = ""
    findings: list[Finding] = field(default_factory=list)
    objectives: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    success_indicators: list[dict] = field(default_factory=list)  # {indicator, data_source}
    stakeholders: list[dict] = field(default_factory=list)        # {name, role, influence}
    playback_confirmed: bool = False
    playback_on: str = ""


@dataclass
class Requirement:
    ref: str = ""                # R1, R2 ...
    statement: str = ""
    source: str = ""             # finding ref, "client statement", or assumption id
    kind: str = "Confirmed"      # Confirmed | Assumed
    capability: str = ""         # which SERVICES.md §3 capability delivers this
    in_scope: bool = True        # False => deferred
    deferred_reason: str = ""


@dataclass
class Solution:
    problem_restatement: str = ""
    requirements: list[Requirement] = field(default_factory=list)
    stage: str = ""              # SERVICES.md §2
    feasibility: str = ""
    open_dependencies: list[str] = field(default_factory=list)
    verified_against_discovery: bool = False
    approved_by: str = ""
    approved_on: str = ""


@dataclass
class ProposalRecord:
    gate_terms_decided: bool = False       # PROPOSAL.md §5.1 issuance gate
    gate_deliverables_defined: bool = False
    gate_notes: str = ""
    commercial_terms: str = "To be determined"   # until the founder approves the figure
    version: int = 0
    issued_on: str = ""
    issued_at: str = ""          # full timestamp, for proposal build time
    valid_until: str = ""
    approved_by: str = ""
    revisions: list[dict] = field(default_factory=list)  # {version, date, changed, why}
    outcome: str = ""            # Accepted | Negotiated | Declined | No decision
    outcome_on: str = ""
    outcome_reasoning: str = ""
    loss_reason: str = ""


@dataclass
class FollowUp:
    action: str = ""
    owner: str = "Founder"
    due: str = ""
    done_on: str = ""
    note: str = ""


@dataclass
class Project:
    brief_complete: bool = False
    acceptance_criteria: list[str] = field(default_factory=list)
    approvers: list[dict] = field(default_factory=list)   # {phase, approver}
    access_items: list[dict] = field(default_factory=list)  # {what, where} — never values
    client_dependencies: list[str] = field(default_factory=list)
    kickoff_on: str = ""
    initialized_on: str = ""


@dataclass
class BuyerEvidence:
    """ICP.md §7 — evidence testing the D-021 buyer roles. Never generalized here."""
    initiated_contact: str = ""
    held_budget: str = ""
    could_say_no: str = ""
    had_to_be_convinced: str = ""
    industry: str = ""
    approximate_size: str = ""


@dataclass
class Hold:
    """An opportunity paused while still live.

    `clients/README.md` owns the status vocabulary and contains no ON HOLD
    value; adding one is a Tier 7 change reserved to the founder. A hold is
    therefore recorded alongside the status, not as one — the opportunity keeps
    the stage it actually reached.
    """
    on_hold: bool = False
    reason: str = ""
    since: str = ""
    revisit_on: str = ""


@dataclass
class Event:
    at: str = ""
    kind: str = ""
    detail: str = ""
    actor: str = ""


@dataclass
class Opportunity:
    slug: str = ""
    company: Company = field(default_factory=Company)
    contacts: list[Contact] = field(default_factory=list)
    status: str = PROSPECT
    created_on: str = ""
    qualification: Qualification = field(default_factory=Qualification)
    discovery: Discovery = field(default_factory=Discovery)
    solution: Solution = field(default_factory=Solution)
    proposal: ProposalRecord = field(default_factory=ProposalRecord)
    follow_ups: list[FollowUp] = field(default_factory=list)
    project: Project = field(default_factory=Project)
    buyer_evidence: BuyerEvidence = field(default_factory=BuyerEvidence)
    hold: Hold = field(default_factory=Hold)
    events: list[Event] = field(default_factory=list)
    schema_version: int = SCHEMA_VERSION

    # -- lifecycle ---------------------------------------------------------

    def log(self, kind: str, detail: str = "", actor: str = "system") -> None:
        self.events.append(Event(at=now(), kind=kind, detail=detail, actor=actor))

    def set_status(self, new: str, actor: str = "system", detail: str = "") -> None:
        if new not in STATUSES:
            raise StageError(
                f"{new!r} is not a permitted status. "
                f"clients/README.md defines exactly: {', '.join(STATUSES)}"
            )
        allowed = TRANSITIONS.get(self.status, set())
        if new != self.status and new not in allowed:
            raise StageError(
                f"{self.status} -> {new} is not a documented transition. "
                f"From {self.status} the lifecycle permits: "
                f"{', '.join(sorted(allowed)) or 'nothing (terminal)'}."
            )
        old, self.status = self.status, new
        self.log("status", f"{old} -> {new}. {detail}".strip(), actor)

    @property
    def decision_maker(self) -> Contact | None:
        for c in self.contacts:
            if c.is_decision_maker:
                return c
        return None

    def primary_contact(self) -> Contact | None:
        return self.contacts[0] if self.contacts else None

    def finding(self, ref: str) -> Finding | None:
        return next((f for f in self.discovery.findings if f.ref == ref), None)

    def in_scope(self) -> list[Requirement]:
        return [r for r in self.solution.requirements if r.in_scope]

    def deferred(self) -> list[Requirement]:
        return [r for r in self.solution.requirements if not r.in_scope]

    def pipeline_stage(self) -> str:
        """The operating stage, in pipeline terms, derived from the record.

        `status` is the authoritative field (`clients/README.md`); this is a
        read-only view that distinguishes states the status alone cannot show —
        qualifying vs qualified, negotiation, and hold.
        """
        if self.hold.on_hold:
            return "ON HOLD"
        s = self.status
        if s == PROSPECT:
            return "QUALIFYING" if self.qualification.outcome or self.qualification.fit.high_fit_signals else "NEW"
        if s == QUALIFIED:
            return "QUALIFIED"
        if s == DISCOVERY:
            return "SOLUTION" if self.solution.requirements else "DISCOVERY"
        if s == PROPOSAL:
            if self.proposal.outcome == "Negotiated":
                return "NEGOTIATION"
            return "PROPOSAL" if self.proposal.issued_on else "SOLUTION"
        if s == ONBOARDING:
            return "WON"
        if s in (ACTIVE, LAUNCHED, CLOSED):
            return "PROJECT INITIALIZED"
        if s == DISQUALIFIED:
            return "NOT A FIT"
        if s == LOST:
            return "LOST"
        if s == NURTURE:
            return "ON HOLD"
        return s.upper()

    def open_follow_ups(self) -> list[FollowUp]:
        return [f for f in self.follow_ups if not f.done_on]

    def next_follow_up(self) -> FollowUp | None:
        openf = sorted(self.open_follow_ups(), key=lambda f: f.due or "9999")
        return openf[0] if openf else None


# --------------------------------------------------------------------------
# (de)serialisation — plain dict/JSON, no third-party dependency
# --------------------------------------------------------------------------

def validate(opp: "Opportunity") -> list[str]:
    """Structural problems that make a record unsafe to operate on."""
    problems: list[str] = []
    if not opp.slug:
        problems.append("record has no slug")
    if opp.status not in STATUSES:
        problems.append(
            f"status {opp.status!r} is not a permitted value. "
            f"clients/README.md defines exactly: {', '.join(STATUSES)}"
        )
    if opp.created_on and not _is_date(opp.created_on):
        problems.append(f"created_on {opp.created_on!r} is not an ISO date")
    seen: set[str] = set()
    for f in opp.discovery.findings:
        if not isinstance(f.confirmed, bool):
            problems.append(
                f"finding {f.ref or '?'}: `confirmed` is {f.confirmed!r}, not a boolean — "
                f"the evidence/inference boundary cannot be evaluated"
            )
        if f.ref and f.ref in seen:
            problems.append(f"duplicate finding ref {f.ref!r}")
        seen.add(f.ref)
    seen = set()
    for r in opp.solution.requirements:
        if r.kind not in ("Confirmed", "Assumed"):
            problems.append(f"requirement {r.ref or '?'}: kind {r.kind!r} "
                            f"must be Confirmed or Assumed")
        if r.ref and r.ref in seen:
            problems.append(f"duplicate requirement ref {r.ref!r}")
        seen.add(r.ref)
    for fu in opp.follow_ups:
        if fu.due and not _is_date(fu.due):
            problems.append(f"follow-up due {fu.due!r} is not an ISO date")
    return problems


def _is_date(value: str) -> bool:
    try:
        _dt.date.fromisoformat(str(value)[:10])
        return True
    except ValueError:
        return False


def to_dict(obj: Any) -> Any:
    if is_dataclass(obj):
        return {f.name: to_dict(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, list):
        return [to_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj


_TRUE = {"true", "yes", "y", "1", "confirmed", "t"}
_FALSE = {"false", "no", "n", "0", "inferred", "assumed", "f", ""}


def as_bool(value: Any, field_name: str = "") -> bool | None:
    """Coerce to a real bool, or raise. Never guess.

    An AI returning `"confirmed": "yes please"` previously stored the string,
    and every truthiness test then read it as confirmed — silently converting an
    inference into a fact. That is the one boundary this system cannot lose, so
    an unrecognised value is an error, not a default.
    """
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in _TRUE:
            return True
        if v in _FALSE:
            return False
    raise ValueError(
        f"{field_name or 'value'}: expected true/false, got {value!r}. "
        f"Leaving it ambiguous would let an inference be read as a confirmed fact."
    )


def _hints(cls) -> dict:
    """Resolved type hints for a dataclass, cached.

    Resolving in the class's own module is what makes this safe: an earlier
    version matched types by bare name through one shared table, so
    `growth.Fit` silently resolved to `model.Fit` and the record round-tripped
    into the wrong object.
    """
    cached = _HINT_CACHE.get(cls)
    if cached is None:
        import sys as _sys
        import typing
        mod = _sys.modules.get(cls.__module__)
        ns = dict(vars(mod)) if mod else {}
        try:
            cached = typing.get_type_hints(cls, globalns=ns)
        except Exception:
            cached = {f.name: f.type for f in fields(cls)}
        _HINT_CACHE[cls] = cached
    return cached


def from_dict(cls, data: Any):
    if data is None:
        return cls()
    if not is_dataclass(cls):
        return data
    hints = _hints(cls)
    kwargs = {}
    for f in fields(cls):
        if f.name not in data:
            continue
        val = data[f.name]
        ftype = hints.get(f.name, f.type)
        args = getattr(ftype, "__args__", None)
        if isinstance(ftype, type) and is_dataclass(ftype):
            kwargs[f.name] = from_dict(ftype, val)
        elif args and isinstance(val, list):
            inner = args[0]
            if isinstance(inner, type) and is_dataclass(inner):
                kwargs[f.name] = [from_dict(inner, v) for v in val]
            else:
                kwargs[f.name] = val
        elif _is_bool_hint(ftype):
            kwargs[f.name] = as_bool(val, f"{cls.__name__}.{f.name}")
        else:
            kwargs[f.name] = val
    return cls(**kwargs)


def _is_bool_hint(ftype) -> bool:
    if ftype is bool:
        return True
    args = getattr(ftype, "__args__", None)
    return bool(args) and set(args) <= {bool, type(None)}


_HINT_CACHE: dict = {}
