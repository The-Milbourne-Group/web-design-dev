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
    role: str = ""            # as stated by them; never inferred (Q-003 open)
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
    source: str = ""             # evidence for Q-008
    problem: str = ""            # in the prospect's own words
    desired_outcome: str = ""
    authority_confirmed: bool | None = None
    fit: Fit = field(default_factory=Fit)
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
    commercial_terms: str = "To be determined"   # Q-007 open until founder decides
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
    """ICP.md §7 — the evidence Q-003 needs. Recorded, never generalized here."""
    initiated_contact: str = ""
    held_budget: str = ""
    could_say_no: str = ""
    had_to_be_convinced: str = ""
    industry: str = ""
    approximate_size: str = ""


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

    def open_follow_ups(self) -> list[FollowUp]:
        return [f for f in self.follow_ups if not f.done_on]

    def next_follow_up(self) -> FollowUp | None:
        openf = sorted(self.open_follow_ups(), key=lambda f: f.due or "9999")
        return openf[0] if openf else None


# --------------------------------------------------------------------------
# (de)serialisation — plain dict/JSON, no third-party dependency
# --------------------------------------------------------------------------

def to_dict(obj: Any) -> Any:
    if is_dataclass(obj):
        return {f.name: to_dict(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, list):
        return [to_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj


def from_dict(cls, data: Any):
    if data is None:
        return cls()
    if not is_dataclass(cls):
        return data
    kwargs = {}
    for f in fields(cls):
        if f.name not in data:
            continue
        val = data[f.name]
        ftype = f.type
        if isinstance(ftype, str):
            ftype = _RESOLVE.get(ftype, ftype)
        origin = getattr(ftype, "__args__", None)
        if isinstance(ftype, type) and is_dataclass(ftype):
            kwargs[f.name] = from_dict(ftype, val)
        elif origin and isinstance(val, list):
            inner = origin[0]
            if isinstance(inner, type) and is_dataclass(inner):
                kwargs[f.name] = [from_dict(inner, v) for v in val]
            else:
                kwargs[f.name] = val
        else:
            kwargs[f.name] = val
    return cls(**kwargs)


_RESOLVE = {
    "Contact": Contact, "Company": Company, "Fit": Fit,
    "Qualification": Qualification, "Finding": Finding, "Discovery": Discovery,
    "Requirement": Requirement, "Solution": Solution,
    "ProposalRecord": ProposalRecord, "FollowUp": FollowUp,
    "Project": Project, "BuyerEvidence": BuyerEvidence, "Event": Event,
    "list[Contact]": list[Contact], "list[Finding]": list[Finding],
    "list[Requirement]": list[Requirement], "list[FollowUp]": list[FollowUp],
    "list[Event]": list[Event],
}
