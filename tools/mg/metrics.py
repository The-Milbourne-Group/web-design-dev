"""Workflow measurement. Computed from the records, never entered by hand.

These are the metrics `METRICS.md` §4 and §6 mandate. Before the pipeline
carried structured stage timestamps, discovery-to-proposal and proposal-to-close
could not be computed at all.
"""
from __future__ import annotations

import datetime as _dt

from . import model as m


def _d(s: str):
    try:
        return _dt.date.fromisoformat(s[:10])
    except Exception:
        return None


def _first(opp: m.Opportunity, *kinds: str):
    for e in opp.events:
        if e.kind == "status" and any(k in e.detail for k in kinds):
            return _d(e.at)
    return None


def stage_dates(opp: m.Opportunity) -> dict:
    return {
        "created": _d(opp.created_on),
        "qualified": _first(opp, f"-> {m.QUALIFIED}"),
        "discovery": _first(opp, f"-> {m.DISCOVERY}"),
        "proposal": _first(opp, f"-> {m.PROPOSAL}"),
        "closed_won": _first(opp, f"-> {m.ONBOARDING}"),
        "closed_lost": _first(opp, f"-> {m.LOST}", f"-> {m.DISQUALIFIED}"),
    }


def cycle_days(opp: m.Opportunity) -> int | None:
    s = stage_dates(opp)
    end = s["closed_won"] or s["closed_lost"]
    if s["created"] and end:
        return (end - s["created"]).days
    return None


def age_days(opp: m.Opportunity) -> int | None:
    """Days since the lead was captured, for opportunities still open."""
    d = _d(opp.created_on)
    return (_dt.date.today() - d).days if d else None


def proposal_hours(opp: m.Opportunity) -> float | None:
    """Wall-clock from solution approval to proposal issue."""
    ap, iss = opp.solution.approved_on, (opp.proposal.issued_at or opp.proposal.issued_on)
    try:
        a = _dt.datetime.fromisoformat(ap)
        b = _dt.datetime.fromisoformat(iss)
        hours = (b - a).total_seconds() / 3600
        return round(hours, 1) if hours >= 0 else None
    except Exception:
        return None


def summarize(opps: list[m.Opportunity]) -> dict:
    total = len(opps)
    reached = lambda *st: sum(1 for o in opps if _reached(o, *st))
    qualified = reached(m.QUALIFIED)
    discovered = reached(m.DISCOVERY)
    proposed = reached(m.PROPOSAL)
    won = reached(m.ONBOARDING)
    lost = sum(1 for o in opps if o.status in (m.LOST, m.DISQUALIFIED))
    cycles = [c for c in (cycle_days(o) for o in opps) if c is not None]
    prod = [p for p in (proposal_hours(o) for o in opps) if p is not None]
    pct = lambda a, b: (round(100 * a / b) if b else None)
    return {
        "leads": total,
        "qualified": qualified,
        "qualified_rate": pct(qualified, total),
        "discovery": discovered,
        "discovery_conversion": pct(discovered, qualified),
        "proposals": proposed,
        "proposal_conversion": pct(proposed, discovered),
        "won": won,
        "close_rate": pct(won, proposed),
        "lost": lost,
        "open": sum(1 for o in opps if o.status not in m.TERMINAL),
        "avg_cycle_days": (round(sum(cycles) / len(cycles)) if cycles else None),
        "avg_proposal_hours": (round(sum(prod) / len(prod), 1) if prod else None),
        "by_status": _by_status(opps),
        "by_source": _by_source(opps),
    }


def _reached(opp: m.Opportunity, status: str) -> bool:
    if opp.status == status:
        return True
    return any(e.kind == "status" and f"-> {status}" in e.detail for e in opp.events)


def _by_status(opps):
    out: dict[str, int] = {}
    for o in opps:
        out[o.status] = out.get(o.status, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def _by_source(opps):
    out: dict[str, int] = {}
    for o in opps:
        s = o.qualification.source or "unrecorded"
        out[s] = out.get(s, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


# --------------------------------------------------------------------------
# Growth engine
# --------------------------------------------------------------------------

def growth_summary(targets: list, opps: list[m.Opportunity]) -> dict:
    """Which activities are producing qualified opportunities?

    Attribution is by the source string the conversion writes into the
    opportunity, so a downstream outcome traces back to the channel and
    campaign that produced it — the evidence Q-008 needs.
    """
    from . import growth as gr

    identified = len(targets)
    researched = sum(1 for t in targets if t.confirmed())
    assessed = sum(1 for t in targets if t.fit.band)
    strong = sum(1 for t in targets if t.fit.band == "Strong")
    contacted = sum(1 for t in targets if t.sent_touches())
    responded = sum(1 for t in targets if t.has_response())
    positive = sum(1 for t in targets if t.positive_response())
    converted = [t for t in targets if t.status == gr.CONVERTED]
    disqualified = sum(1 for t in targets if t.status == gr.DISQUALIFIED)
    touches = sum(len(t.sent_touches()) for t in targets)

    # downstream: what happened to the leads these targets became
    by_slug = {o.slug: o for o in opps}
    downstream = {"qualified": 0, "discovery": 0, "proposed": 0, "won": 0}
    for t in converted:
        o = by_slug.get(t.converted_to)
        if not o:
            continue
        if _reached(o, m.QUALIFIED):
            downstream["qualified"] += 1
        if _reached(o, m.DISCOVERY):
            downstream["discovery"] += 1
        if _reached(o, m.PROPOSAL):
            downstream["proposed"] += 1
        if _reached(o, m.ONBOARDING):
            downstream["won"] += 1

    pct = lambda a, b: (round(100 * a / b) if b else None)
    return {
        "identified": identified,
        "researched": researched,
        "assessed": assessed,
        "strong_fit": strong,
        "contacted": contacted,
        "messages_sent": touches,
        "responded": responded,
        "response_rate": pct(responded, contacted),
        "positive": positive,
        "positive_rate": pct(positive, contacted),
        "converted": len(converted),
        "conversion_rate": pct(len(converted), contacted),
        "disqualified": disqualified,
        "downstream": downstream,
        "by_channel": _by_channel(targets),
        "by_campaign": _by_campaign(targets),
    }


def _by_channel(targets) -> dict:
    """Outcomes per channel actually used. Q-008 is open; this is the evidence."""
    out: dict[str, dict] = {}
    for t in targets:
        for touch in t.sent_touches():
            ch = touch.channel or "unrecorded"
            row = out.setdefault(ch, {"sent": 0, "responded": 0, "positive": 0, "converted": 0})
            row["sent"] += 1
            if touch.response_on:
                row["responded"] += 1
            if touch.response_kind == "positive":
                row["positive"] += 1
        if t.status == "Converted" and t.sent_touches():
            ch = t.sent_touches()[-1].channel or "unrecorded"
            out.setdefault(ch, {"sent": 0, "responded": 0, "positive": 0, "converted": 0})
            out[ch]["converted"] += 1
    return out


def _by_campaign(targets) -> dict:
    out: dict[str, dict] = {}
    for t in targets:
        key = t.campaign or "uncategorised"
        row = out.setdefault(key, {"targets": 0, "contacted": 0, "positive": 0, "converted": 0})
        row["targets"] += 1
        if t.sent_touches():
            row["contacted"] += 1
        if t.positive_response():
            row["positive"] += 1
        if t.status == "Converted":
            row["converted"] += 1
    return out


def _by_source_origin(opps: list[m.Opportunity]) -> dict:
    """Opportunity sources, so inbound and outbound are comparable."""
    out: dict[str, int] = {}
    for o in opps:
        src = o.qualification.source or "unrecorded"
        out[src] = out.get(src, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))
