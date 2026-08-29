"""The AI layer: context packets for a Claude session, and result ingestion.

The AI operator in this company is a Claude Code session, so the leverage is
not another API client — it is assembling exactly the right context and exactly
the right constraints, which `CLAUDE.md` §3 specifies as a table a human has to
apply by hand. This does it mechanically, per task.

`mg brief <slug> <task>` prints a packet. Paste it into a session, or pipe it.
`mg ingest <slug> --from result.json` merges structured output back into the
record, so no AI output is retyped.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import model as m
from .governance import open_questions, icp_signals

# CLAUDE.md §3 layered context loading, per task.
ALWAYS = ["MASTER.md", "governance/AUTHORITY.md", "OPEN_QUESTIONS.md"]

TASKS: dict[str, dict] = {
    "research": {
        "goal": "Research the prospect's business and current digital presence.",
        "load": ["ICP.md", "sops/sales/QUALIFICATION.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": "Findings on their business, market, and current site. Public information only.",
        "schema": {"notes": "str", "problem_signals": ["str"], "high_fit_signals": ["str"]},
    },
    "qualify": {
        "goal": "Assess ICP fit and recommend a qualification outcome.",
        "load": ["ICP.md", "SALES.md", "SERVICES.md", "sops/sales/QUALIFICATION.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": ("A recommendation. You do NOT decide — the founder decides. "
                     "Keep confirmed_facts and assessment strictly separate: a fact is "
                     "something the record supports, an assessment is your reading of it. "
                     "If a strategically ambiguous opportunity cannot be called on the "
                     "evidence, recommend 'Clarification required' rather than guessing."),
        "schema": {
            "confirmed_facts": ["only what the record or public information directly "
                                "supports — quote or cite it"],
            "assessment": "your reasoned interpretation, clearly separate from the facts above",
            "high_fit_signals": ["quoted verbatim from ICP.md §4"],
            "problem_signals": ["quoted verbatim from ICP.md §5"],
            "disqualifying_signals": ["quoted verbatim from ICP.md §6"],
            "stage": "Entry|Expansion|Recurring",
            "feasible": "bool",
            "missing_information": ["what must be established before a confident decision"],
            "recommended_outcome": "Qualified|Nurture|Clarification required|Disqualified",
            "recommended_next_action": "the single most appropriate next step",
        },
    },
    "discovery-prep": {
        "goal": "Prepare the discovery conversation: agenda and informed questions.",
        "load": ["ICP.md", "sops/sales/DISCOVERY.md", "templates/sales/DISCOVERY_NOTES.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": "An agenda and a question set specific to this prospect — not a blank form.",
        "schema": {"agenda": ["str"], "questions": ["str"]},
    },
    "discovery-analysis": {
        "goal": ("Convert raw discovery notes or a transcript into structured findings. "
                 "The single most important requirement: separate what the client "
                 "actually SAID (confirmed=true) from what you INFERRED (confirmed=false)."),
        "load": ["sops/sales/DISCOVERY.md", "METRICS.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": "Structured findings, objectives, problems, constraints, risks, unknowns.",
        "schema": {
            "findings": [{"ref": "D1", "topic": "str", "statement": "str",
                          "confirmed": "bool", "source": "who said it / basis for the inference"}],
            "objectives": ["str"], "problems": ["str"], "constraints": ["str"],
            "risks": ["str"], "opportunities": ["str"], "unknowns": ["str"],
            "assumptions": ["str"],
            "success_indicators": [{"indicator": "str", "data_source": "str or empty"}],
            "stakeholders": [{"name": "str", "role": "str", "influence": "str"}],
        },
    },
    "solution": {
        "goal": ("Draft the requirement traceability matrix. Every requirement MUST cite a "
                 "finding ref, an explicit client statement, or an assumption. A requirement "
                 "with no source is REMOVED, not justified."),
        "load": ["SERVICES.md", "SALES.md", "sops/sales/SOLUTION_DESIGN.md"],
        "agent": "agents/SALES_AGENT.md prepares; founder decides (D-010)",
        "produces": ("A traceability matrix and a minimum viable scope recommendation. "
                     "Every requirement must name the approved capability that delivers "
                     "it. If a client need maps to no approved capability, say so "
                     "plainly — do not scope work the company has not said it does."),
        "schema": {
            "problem_restatement": "str",
            "requirements": [{"ref": "R1", "statement": "str",
                              "source": "D1 / client statement / assumption",
                              "kind": "Confirmed|Assumed",
                              "capability": "which SERVICES.md §3 capability delivers this "
                                            "— see the list below; if none does, the "
                                            "company does not offer it",
                              "in_scope": "bool",
                              "deferred_reason": "str if in_scope false"}],
            "stage": "Entry|Expansion|Recurring", "feasibility": "str",
            "open_dependencies": ["str"],
        },
    },
    "proposal": {
        "goal": "Draft proposal prose from the approved solution. Add no scope.",
        "load": ["SALES.md", "SERVICES.md", "BRAND.md", "sops/sales/PROPOSAL.md",
                 "templates/sales/PROPOSAL_OUTLINE.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": "Prose for context, problem framing and approach. NEVER a price.",
        "schema": {"context": "str", "approach": "str", "next_step": "str"},
    },
    "follow-up": {
        "goal": "Draft follow-up correspondence for founder review.",
        "load": ["SALES.md", "BRAND.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": "A draft message. No urgency, no commitment, no price.",
        "schema": {"subject": "str", "body": "str"},
    },
}


def _facts(opp: m.Opportunity) -> dict:
    """Only what the task could need — MASTER.md §5.4, smallest sufficient set."""
    return {
        "company": m.to_dict(opp.company),
        "contacts": [m.to_dict(c) for c in opp.contacts],
        "status": opp.status,
        "qualification": m.to_dict(opp.qualification),
        "discovery": m.to_dict(opp.discovery),
        "solution": m.to_dict(opp.solution),
    }


def packet(root: Path, opp: m.Opportunity, task: str) -> str:
    if task not in TASKS:
        raise KeyError(f"Unknown task {task!r}. Available: {', '.join(TASKS)}")
    t = TASKS[task]
    qs = open_questions(root)
    open_now = [f"{q['id']} ({q['priority']}) — {q['title']}"
                for q in qs.values() if not q["resolved"]]
    sig = icp_signals(root)

    load_list = "\n".join(f"  - {p}" for p in ALWAYS + t["load"])
    open_list = "\n".join(f"  - {o}" for o in open_now)
    icp_block = ""
    if task == "solution":
        from .governance import capability_keys
        caps = capability_keys(root)
        icp_block = ("\n## Approved capabilities (SERVICES.md §3) — tag every requirement\n"
                     + "\n".join(f"  {k}  — {v}" for k, v in caps.items())
                     + "\n\nA client need that maps to none of these is not something the "
                       "company offers. Name it as out of scope; never invent a capability.\n")
    if task in ("qualify", "research"):
        icp_block = (
            "\n## ICP signals you may match against (ICP.md — quote these, invent none)\n"
            + "\nHigh-fit:\n" + "\n".join(f"  - {s}" for s in sig["high_fit"])
            + "\nProblem:\n" + "\n".join(f"  - {s}" for s in sig["problem"])
            + "\nDisqualifying:\n" + "\n".join(f"  - {s}" for s in sig["disqualifying"])
            + "\n"
        )

    return f"""# AI TASK PACKET — {task}
# Opportunity: {opp.slug} ({opp.company.name or 'unnamed'}) · status {opp.status}
# Generated by tools/mg. Context selected per CLAUDE.md §3.

## Role
{t['agent']}
Specialization grants capability, not authority (agents/README.md §1).

## Goal
{t['goal']}

## Load these documents before answering
{load_list}

## Absolute constraints
  - NEVER supply a value registered Open below. If the task needs one, say which
    question blocks it and stop. This is the highest-frequency and most damaging
    failure mode in this system (CLAUDE.md §4.1, RISKS.md R-006).
  - NEVER state a price, discount, timeline guarantee, or undefined deliverable.
  - NEVER present an assumption as a fact. Label every inference.
  - NEVER describe the company as AI-first or lead with AI as the value
    proposition (D-002).
  - You RECOMMEND. The founder DECIDES.

## Open questions — these values are NOT known
{open_list}
{icp_block}
## What you produce
{t['produces']}

## Required output format
Return ONLY a JSON object matching this shape, in a ```json fenced block:

```json
{json.dumps(t['schema'], indent=2)}
```

## Opportunity record (the only client context — one client per session, MASTER.md §7.1)

```json
{json.dumps(_facts(opp), indent=2, ensure_ascii=False)}
```
"""


# --------------------------------------------------------------------------
# Ingestion — merge structured AI output into the record
# --------------------------------------------------------------------------

def _merge_refs(existing: list, incoming: list, cls, label: str,
                changed: list[str], replace: bool) -> list:
    """Merge by `ref`, never silently dropping what is already recorded.

    Replacing the list outright destroyed prior findings on a second ingest —
    a client's discovery disappearing because an analysis was re-run. Entries
    with a known ref are updated; new refs are appended; anything already
    recorded and not mentioned again survives.
    """
    parsed = [m.from_dict(cls, x) for x in incoming]
    if replace:
        changed.append(f"{label} replaced ({len(parsed)})")
        return parsed
    by_ref = {getattr(x, "ref", "") or f"_{i}": x for i, x in enumerate(existing)}
    added = updated = 0
    for item in parsed:
        key = getattr(item, "ref", "") or f"_new{added}"
        if key in by_ref:
            by_ref[key] = item
            updated += 1
        else:
            by_ref[key] = item
            added += 1
    if added or updated:
        note = f"{label} ({added} added"
        note += f", {updated} updated" if updated else ""
        note += f", {len(existing) - updated} kept)" if existing else ")"
        changed.append(note)
    return list(by_ref.values())


def _merge_list(existing: list[str], incoming: list[str], label: str,
                changed: list[str], replace: bool) -> list[str]:
    if replace:
        changed.append(f"{label} replaced")
        return list(incoming)
    merged = list(existing)
    added = 0
    for item in incoming:
        if item not in merged:
            merged.append(item)
            added += 1
    if added:
        changed.append(f"{label} (+{added})")
    return merged


def ingest(opp: m.Opportunity, task: str, data: dict, replace: bool = False) -> list[str]:
    """Merge a result packet. Returns a list of what changed.

    Merges by default. `replace=True` is the explicit, opt-in way to discard
    what is already recorded.
    """
    changed: list[str] = []

    if task in ("research", "qualify"):
        f = opp.qualification.fit
        if replace:
            f.high_fit_signals = f.problem_signals = f.disqualifying_signals = []
        for key, attr in (("high_fit_signals", "high_fit_signals"),
                          ("problem_signals", "problem_signals"),
                          ("disqualifying_signals", "disqualifying_signals")):
            if data.get(key):
                setattr(f, attr, sorted(set(getattr(f, attr) + list(data[key]))))
                changed.append(f"fit.{attr} ({len(getattr(f, attr))})")
        if data.get("stage"):
            f.stage = data["stage"]; changed.append("fit.stage")
        if data.get("feasible") is not None:
            f.feasible = bool(data["feasible"]); changed.append("fit.feasible")
        q = opp.qualification
        if data.get("confirmed_facts"):
            q.confirmed_facts = list(data["confirmed_facts"]); changed.append("confirmed_facts")
        if data.get("assessment"):
            q.assessment = data["assessment"]; changed.append("assessment")
        if data.get("reasoning"):
            f.reasoning = data["reasoning"]; changed.append("fit.reasoning")
        for key in ("missing_information", "open_items"):
            if data.get(key):
                q.open_items = sorted(set(q.open_items + list(data[key])))
                changed.append("missing_information")
                break
        if data.get("recommended_next_action"):
            q.recommended_next_action = data["recommended_next_action"]
            changed.append("recommended_next_action")
        if data.get("recommended_outcome"):
            q.recommended_outcome = data["recommended_outcome"]
            opp.log("ai", f"qualification recommendation: {data['recommended_outcome']}", "ai")
            changed.append(f"recommendation recorded ({data['recommended_outcome']}) "
                           f"— NOT applied; founder decides")

    elif task == "discovery-prep":
        if data.get("agenda"):
            opp.discovery.agenda = list(data["agenda"]); changed.append("agenda")
        if data.get("questions"):
            opp.discovery.agenda = opp.discovery.agenda + list(data["questions"])
            changed.append("questions appended to agenda")

    elif task == "discovery-analysis":
        d = opp.discovery
        if data.get("findings"):
            d.findings = _merge_refs(d.findings, data["findings"], m.Finding,
                                     "findings", changed, replace)
            nc = sum(1 for x in d.findings if not x.confirmed)
            changed.append(f"now {len(d.findings)} findings: "
                           f"{len(d.findings)-nc} confirmed, {nc} inferred")
        for k in ("objectives", "problems", "constraints", "risks",
                  "opportunities", "unknowns", "assumptions"):
            if data.get(k):
                setattr(d, k, _merge_list(getattr(d, k), list(data[k]), k, changed, replace))
        for k, key in (("success_indicators", "indicator"), ("stakeholders", "name")):
            if data.get(k):
                cur = getattr(d, k)
                if replace:
                    setattr(d, k, list(data[k])); changed.append(f"{k} replaced")
                else:
                    seen = {x.get(key) for x in cur}
                    added = [x for x in data[k] if x.get(key) not in seen]
                    setattr(d, k, cur + added)
                    if added:
                        changed.append(f"{k} (+{len(added)})")

    elif task == "solution":
        s = opp.solution
        if data.get("problem_restatement"):
            s.problem_restatement = data["problem_restatement"]; changed.append("problem_restatement")
        if data.get("requirements"):
            s.requirements = _merge_refs(s.requirements, data["requirements"],
                                         m.Requirement, "requirements", changed, replace)
        if data.get("stage"):
            s.stage = data["stage"]; changed.append("stage")
        if data.get("feasibility"):
            s.feasibility = data["feasibility"]; changed.append("feasibility")
        if data.get("open_dependencies"):
            s.open_dependencies = list(data["open_dependencies"]); changed.append("open_dependencies")

    elif task in ("proposal", "follow-up"):
        opp.log("ai", f"{task} draft ingested: {json.dumps(data)[:200]}", "ai")
        changed.append("draft logged to events (prose is not a record field)")

    return changed


def extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model response, fenced or bare."""
    t = text.strip()
    if "```" in t:
        parts = t.split("```")
        for p in parts:
            p = p.strip()
            if p.startswith("json"):
                p = p[4:].strip()
            if p.startswith("{"):
                try:
                    return json.loads(p)
                except json.JSONDecodeError:
                    continue
    start = t.find("{")
    if start >= 0:
        return json.loads(t[start:t.rfind("}") + 1])
    raise ValueError("No JSON object found in the input.")
