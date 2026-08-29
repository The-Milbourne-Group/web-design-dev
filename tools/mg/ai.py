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
    "target-research": {
        "goal": ("Research a target company from public information only, and type "
                 "every statement by how far it can be trusted."),
        "load": ["ICP.md", "SERVICES.md", "BRAND.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": ("A structured prospect profile. Every `confirmed` item names where "
                     "it was observed. Anything you reasoned rather than read is an "
                     "`inference`. Anything you could not establish is an `unknown` — "
                     "record it rather than filling it in. Fabricated company research "
                     "is the failure this task exists to prevent."),
        "schema": {
            "company": {"industry": "str", "approximate_size": "str",
                        "location": "str", "website": "str"},
            "contacts": [{"name": "str", "role": "as published, never inferred from a "
                                                 "name or guessed; D-021 lists expected roles, verify them",
                          "email": "only if published"}],
            "research": [{"ref": "E1", "statement": "str",
                          "kind": "confirmed|inference|unknown",
                          "source": "where observed — REQUIRED when kind is confirmed",
                          "observed_on": "YYYY-MM-DD"}],
        },
    },
    "target-assess": {
        "goal": "Assess the target against the ICP and recommend an action.",
        "load": ["ICP.md", "SERVICES.md", "BUSINESS.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": ("A fit band with the evidence behind it. Match signals only by "
                     "quoting `ICP.md` verbatim, and cite the evidence ref that supports "
                     "each. Do not invent a score; do not stretch a signal to fit."),
        "schema": {
            "signals": [{"signal": "quoted verbatim from ICP.md §4, §5 or §6",
                         "kind": "high_fit|problem|disqualifying|trigger",
                         "evidence_ref": "E1"}],
            "band": "Strong|Possible|Weak|Not a fit",
            "reasoning": "str",
            "unknowns": ["what cannot be determined from public information"],
            "recommended_action": ("Research further|Initiate outreach|Monitor|"
                                   "Wait for trigger|Disqualify"),
        },
    },
    "target-message": {
        "goal": "Draft one outreach message, grounded in confirmed research.",
        "load": ["BRAND.md", "MARKETING.md", "SALES.md", "SERVICES.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": ("A draft for founder review, and the evidence refs it rests on. "
                     "Every specific claim about this company must trace to a CONFIRMED "
                     "evidence item and you must list those refs in `grounded_in`. "
                     "If you cannot ground a claim, remove it — a message that sounds "
                     "personalised but is not is worse than a plain one."),
        "schema": {
            "purpose": "the reason for contact, in one line",
            "subject": "str",
            "body": "str",
            "grounded_in": ["E1", "E3"],
            "claims_not_grounded": ["anything you wanted to say but could not evidence"],
        },
    },
    "follow-up": {
        "goal": "Draft follow-up correspondence for founder review.",
        "load": ["SALES.md", "BRAND.md"],
        "agent": "agents/SALES_AGENT.md",
        "produces": "A draft message. No urgency, no commitment, no price.",
        "schema": {"subject": "str", "body": "str"},
    },
}


def target_facts(t) -> dict:
    return {
        "company": m.to_dict(t.company),
        "contacts": [m.to_dict(c) for c in t.contacts],
        "identified_via": t.identified_via,
        "status": t.status,
        "research": [m.to_dict(e) for e in t.research],
        "signals": [m.to_dict(s) for s in t.signals],
        "fit": m.to_dict(t.fit),
        "touches": [{"seq": x.seq, "purpose": x.purpose, "channel": x.channel,
                     "status": x.status, "sent_on": x.sent_on,
                     "response_kind": x.response_kind} for x in t.touches],
    }


def target_packet(root: Path, t, task: str) -> str:
    """A packet for a growth task — same constraints, target context."""
    import json as _json
    body = packet(root, m.Opportunity(slug=t.slug), task)
    head, _, _ = body.partition("## Opportunity record")
    head = head.replace(f"# Opportunity: {t.slug} (unnamed) · status Prospect",
                        f"# Target: {t.slug} ({t.company.name or 'unnamed'}) "
                        f"· status {t.status}")
    return head + ("## Target record (one prospect per session, MASTER.md §7.1)\n\n"
                   "```json\n"
                   + _json.dumps(target_facts(t), indent=2, ensure_ascii=False)
                   + "\n```\n")


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
    if task == "target-message":
        icp_block = (
            "\n## Message constraints (binding)\n"
            "  - `BRAND.md` §7 order: client outcome, client problem, approach,\n"
            "    capability, evidence, call to action. Lead with their problem.\n"
            "  - `MARKETING.md` §2.1: never lead with AI; never compete on price;\n"
            "    present the narrow problem, not the capability menu.\n"
            "  - `BRAND.md` §6: claim no results, clients, metrics or certifications.\n"
            "    THE COMPANY HAS NO PUBLISHED CASE STUDIES OR CLIENT RESULTS. Do not\n"
            "    imply otherwise, and do not invent social proof.\n"
            "  - `SALES.md` §8: no fabricated urgency, no pressure, no exaggerated\n"
            "    claims, no invented prior relationship or previous contact.\n"
            "  - `SALES.md` §6: never state a price or a timeline guarantee.\n"
            "  - Write like a person who read their website. No 'I hope this finds\n"
            "    you well', no 'I noticed you're crushing it', no invented flattery.\n"
            "  - The call to action is a conversation, not a booking demand.\n"
            "\n## Positioning (D-022) — this is the message spine\n"
            "  1. Their problem: the business has outgrown its digital infrastructure.\n"
            "  2. The consequence: growth, efficiency, conversion or customer\n"
            "     experience is being constrained.\n"
            "  3. Only then the solution category: strategic redesign, development,\n"
            "     systems integration, automation, infrastructure improvement.\n"
            "  Do NOT position as someone who builds websites (D-022, D-023).\n"
        )
    if task in ("target-research", "target-assess"):
        from .governance import buyer_roles, size_bands, outbound_signals
        sig = icp_signals(root)
        roles = buyer_roles(root)
        icp_block = (
            "\n## Confirmed targeting model (Discovery Round 2 — D-019 to D-022)\n"
            "\nPrimary trigger (D-022): \"Our business has outgrown our current website\n"
            "and digital systems, and they are now becoming a constraint on growth.\"\n"
            "\nMaturity target (D-020): a business that has proven it can sell and\n"
            "operate, but whose digital infrastructure has not kept pace. NOT targeted:\n"
            "pre-revenue startups, unvalidated demand, lowest-cost buyers, or anyone who\n"
            "cannot connect digital investment to a business objective.\n"
            "\nSize bands (D-021):\n"
            + "\n".join(f"  - {band}: {prio}" for band, prio in size_bands(root))
            + "\n  Headcount is not the only variable — revenue, complexity, urgency and\n"
              "  digital maturity carry equal weight.\n"
            "\nPrimary economic buyers (D-021): " + " · ".join(roles["primary"])
            + "\nSecondary buyers / champions: " + " · ".join(roles["secondary"])
            + "\n  Record a role only as PUBLISHED. Do not infer a title from a name, and\n"
              "  do not assume the listed roles exist at this company — verify.\n"
            "\nObservable maturity-gap signals (D-026):\n"
            + "\n".join(f"  - {x}" for x in outbound_signals(root))
            + "\n\n## ICP signals — quote these VERBATIM; invent none (ICP.md)\n"
            + "\nHigh-fit (§4):\n" + "\n".join(f"  - {x}" for x in sig["high_fit"])
            + "\nProblem (§5):\n" + "\n".join(f"  - {x}" for x in sig["problem"])
            + "\nDisqualifying (§6):\n" + "\n".join(f"  - {x}" for x in sig["disqualifying"])
            + "\n\nAlso confirmed: national and remote-first (D-008); boutique/premium,\n"
              "never lowest-cost (D-007); market selection is controlled testing, not a\n"
              "chosen vertical (D-019).\n"
        )
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


def ingest_target(t, task: str, data: dict, replace: bool = False) -> list[str]:
    """Merge growth-task output into a target record."""
    from . import growth as gr
    changed: list[str] = []

    if task == "target-research":
        comp = data.get("company") or {}
        for k in ("industry", "approximate_size", "location", "website"):
            if comp.get(k) and not getattr(t.company, k, ""):
                setattr(t.company, k, comp[k]); changed.append(f"company.{k}")
        for c in data.get("contacts") or []:
            name = (c.get("name") or "").strip()
            if name and not any(x.name == name for x in t.contacts):
                t.contacts.append(m.from_dict(m.Contact, c))
                changed.append(f"contact {name}")
        if data.get("research"):
            t.research = _merge_refs(t.research, data["research"], gr.Evidence,
                                     "research", changed, replace)
            counts = {k: sum(1 for e in t.research if e.kind == k)
                      for k in ("confirmed", "inference", "unknown")}
            changed.append(f"now {counts['confirmed']} confirmed, "
                           f"{counts['inference']} inferred, {counts['unknown']} unknown")

    elif task == "target-assess":
        if data.get("signals"):
            incoming = [m.from_dict(gr.Signal, x) for x in data["signals"]]
            if replace:
                t.signals = incoming
            else:
                have = {(x.signal, x.kind) for x in t.signals}
                t.signals += [x for x in incoming if (x.signal, x.kind) not in have]
            changed.append(f"signals ({len(t.signals)})")
        f = t.fit
        for key, attr in (("band", "band"), ("reasoning", "reasoning"),
                          ("recommended_action", "recommended_action")):
            if data.get(key):
                setattr(f, attr, data[key]); changed.append(f"fit.{attr}")
        if data.get("unknowns"):
            f.unknowns = _merge_list(f.unknowns, list(data["unknowns"]),
                                     "fit.unknowns", changed, replace)
        if data.get("band") or data.get("recommended_action"):
            f.assessed_on = m.today()
            t.log("ai", f"assessment: {data.get('band','?')} / "
                        f"{data.get('recommended_action','?')} — recorded, not acted on", "ai")

    elif task == "target-message":
        touch = gr.Touch(
            seq=len(t.touches) + 1,
            purpose=data.get("purpose", ""),
            draft=("Subject: " + data["subject"] + "\n\n" + data.get("body", ""))
                  if data.get("subject") else data.get("body", ""),
            grounded_in=list(data.get("grounded_in") or []),
            status="draft", drafted_on=m.today(),
        )
        t.touches.append(touch)
        changed.append(f"draft touch #{touch.seq} ({len(touch.grounded_in)} evidence refs)")
        for claim in data.get("claims_not_grounded") or []:
            changed.append(f"dropped ungrounded claim: {claim[:60]}")
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
