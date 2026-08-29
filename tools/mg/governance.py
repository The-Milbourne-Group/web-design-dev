"""Guardrails derived from the operating system, read live from the registers.

Nothing here hard-codes a policy value. `OPEN_QUESTIONS.md` is parsed at
runtime, so when the founder resolves a question the gate opens by itself and
no code change is needed. That keeps one source of truth (`MASTER.md` §5.3).
"""
from __future__ import annotations

import re
from pathlib import Path

from . import model as m


def repo_root(start: Path | None = None) -> Path:
    p = (start or Path(__file__).resolve()).parent
    for cand in [p, *p.parents]:
        if (cand / "MASTER.md").exists() and (cand / "governance").is_dir():
            return cand
    raise RuntimeError("Not inside the operating-system repository (no MASTER.md found).")


# --------------------------------------------------------------------------
# OPEN_QUESTIONS.md — the register of what must never be invented
# --------------------------------------------------------------------------

_Q_HEAD = re.compile(r"^###\s+(Q-\d+)\s+—\s+(.+?)\s+·\s+(\w+)\s*$", re.M)
_Q_ROW = re.compile(
    r"^\|\s*(Q-\d+)\s*[—·-]\s*([^|]+?)\s*\|(?P<rest>(?:[^|\n]*\|){1,4})", re.M)
_D_REF = re.compile(r"\bD-\d+\b")


def open_questions(root: Path) -> dict[str, dict]:
    """Return {id: {title, priority, resolved}} from the live register."""
    text = (root / "OPEN_QUESTIONS.md").read_text(encoding="utf-8")
    body, _, resolved_section = text.partition("\n## Resolved")
    out: dict[str, dict] = {}
    for qid, title, prio in _Q_HEAD.findall(body):
        out[qid] = {"id": qid, "title": title.strip(), "priority": prio, "resolved": False}
    for qid, title, prio in _Q_HEAD.findall(resolved_section):
        out[qid] = {"id": qid, "title": title.strip(), "priority": prio, "resolved": True}
    # Resolved questions are recorded as table rows, not headings. The decision
    # column has moved between rounds, so find the D-### anywhere in the row.
    for mm in _Q_ROW.finditer(resolved_section):
        qid, title = mm.group(1), mm.group(2)
        found = _D_REF.search(mm.group("rest"))
        out.setdefault(qid, {"id": qid, "title": title.strip(), "priority": "Resolved",
                             "resolved": True,
                             "decision": found.group(0) if found else ""})
    return out


def is_open(root: Path, qid: str) -> bool:
    q = open_questions(root).get(qid)
    return bool(q) and not q["resolved"]


# Pricing is decided (D-038). The guard no longer refuses figures — it checks
# them against the approved bands in `SERVICES.md` §2.4 and against the minimum
# engagement value, which is the control that actually protects margin now.
#
# History, for why this is shaped as it is: Q-007 -> D-025 (model) -> Q-015 -> D-033 (structure)
# -> Q-020 -> D-038 (values). While any link held no number the guard keyed on
# the live residual, because an approved model is not an approved number.

PRICING_QUESTION = None          # retained: callers test it for a live residual


def pricing(root: Path) -> dict:
    """The approved commercial configuration, read from `SERVICES.md` §2.4."""
    text = (root / "SERVICES.md").read_text(encoding="utf-8")
    mm = re.search(r"^## 2\.4 Commercial Configuration(.*?)(?=^### Minimum engagement)",
                   text, re.M | re.S)
    out: dict[str, dict] = {}
    if not mm:
        return out
    for line in mm.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or "| Price |" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        label = re.sub(r"\*\*", "", cells[0]).strip()
        figures = [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", cells[1])]
        if not figures:
            continue
        out[label] = {
            "low": min(figures),
            "high": max(figures) if len(figures) > 1 else None,
            "recurring": "month" in cells[1].lower(),
            "raw": re.sub(r"\*\*", "", cells[1]).strip(),
        }
    return out


def minimum_engagement(root: Path) -> int | None:
    for label, band in pricing(root).items():
        if "minimum engagement" in label.lower():
            return band["low"]
    return None


_MONEY_WORD = re.compile(
    r"\b(fee|fees|cost|costs|price|priced|pricing|invest|investment|budget"
    r"|retainer|rate|quote|quoted|charge|payable|deposit|invoice)\b", re.I)

_CUR_SYMBOL = re.compile(r"[$£€]\s?\d[\d,]*(?:\.\d+)?\s?k?", re.I)
_CUR_CODE = re.compile(
    r"\b\d[\d,]*(?:\.\d+)?\s?(?:k\b|USD|GBP|EUR|dollars?|pounds?|euros?)", re.I)
_THOUSANDS = re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b")
_BARE = re.compile(r"\b\d{4,}(?:\.\d+)?\b")


def _is_year(tok: str) -> bool:
    digits = tok.replace(",", "").split(".")[0]
    return len(digits) == 4 and digits.isdigit() and 1900 <= int(digits) <= 2100


def find_money(text: str) -> list[str]:
    """Tokens in `text` that genuinely read as a commercial figure.

    Matches are deduplicated by span: `$3,000` is found by both the currency
    pattern and the thousands pattern, and reporting one figure twice makes the
    operator distrust the check.
    """
    spans: list[tuple[int, int, str]] = []
    for rx in (_CUR_SYMBOL, _CUR_CODE, _THOUSANDS):
        for mm in rx.finditer(text):
            tok = mm.group(0).strip()
            if rx is _THOUSANDS and _is_year(tok):
                continue
            spans.append((mm.start(), mm.end(), tok))
    # A bare four-digit-plus number counts only on a line that is talking money,
    # and never when it is a year.
    offset = 0
    for line in text.splitlines(keepends=True):
        if _MONEY_WORD.search(line):
            for mm in _BARE.finditer(line):
                if not _is_year(mm.group(0)):
                    spans.append((offset + mm.start(), offset + mm.end(), mm.group(0)))
        offset += len(line)

    spans.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    out: list[str] = []
    covered_to = -1
    for start, end, tok in spans:
        if start < covered_to:          # inside a longer match already reported
            continue
        out.append(tok)
        covered_to = end
    return out


def scan_for_open_values(root: Path, text: str) -> list[str]:
    """Check commercial figures against the approved configuration.

    Before D-038 this refused every figure, because no price existed and
    inventing one was the system's worst failure mode. Prices now exist, so the
    useful check is different: a figure below the minimum engagement value is
    the thing that quietly destroys margin.
    """
    problems: list[str] = []
    if PRICING_QUESTION and is_open(root, PRICING_QUESTION):
        hits = find_money(text)
        if hits:
            problems.append(
                f"{PRICING_QUESTION} is open — price points are not decided. Found "
                f"figure(s) that read as commercial values: {', '.join(hits)}. "
                f"Write 'to be determined' (SALES.md §6)."
            )
        return problems

    minimum = minimum_engagement(root)
    if minimum is None:
        return problems
    for hit in find_money(text):
        digits = re.sub(r"[^\d.]", "", hit.split(".")[0])
        if not digits:
            continue
        value = int(float(digits))
        if "k" in hit.lower():
            value *= 1000
        # A recurring figure is measured against the retainer floor, not the
        # project minimum, so only flag amounts stated as project value.
        if value < minimum and not re.search(
                rf"{re.escape(hit)}\s*(?:/|per\s+)\s*(?:mo|month)", text, re.I):
            problems.append(
                f"{hit} is below the ${minimum:,} minimum engagement value "
                f"(SERVICES.md §2.4, D-038). An engagement below it is accepted only "
                f"where the work is explicitly strategic or creates exceptional "
                f"portfolio or relationship value, and the founder records the "
                f"exception."
            )
    return problems


# --------------------------------------------------------------------------
# ICP signals — quoted from ICP.md so qualification cannot invent criteria
# --------------------------------------------------------------------------

def _bullets(text: str, heading: str) -> list[str]:
    mm = re.search(rf"^##\s+{re.escape(heading)}.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if not mm:
        return []
    out = []
    for line in mm.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            out.append(re.sub(r"\*\*(.+?)\*\*", r"\1", line[2:]).strip())
    return out


def icp_signals(root: Path) -> dict[str, list[str]]:
    text = (root / "ICP.md").read_text(encoding="utf-8")
    return {
        "high_fit": _bullets(text, "4. High-Fit Characteristics"),
        "problem": _bullets(text, "5. Problem Signals"),
        "disqualifying": _bullets(text, "6. Disqualification Signals"),
    }


def capabilities(root: Path) -> list[str]:
    """The approved capability set from `SERVICES.md` §3, read live.

    Offers are assembled from these; anything outside them is work the company
    has not said it does (`SERVICES.md` §3, §6).
    """
    text = (root / "SERVICES.md").read_text(encoding="utf-8")
    mm = re.search(r"^##\s+3\. Underlying Capabilities(.*?)(?=^##\s)", text, re.M | re.S)
    if not mm:
        return []
    out = []
    for line in mm.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or "Applied in" in line:
            continue
        cell = line.strip("|").split("|")[0].strip()
        if cell:
            out.append(cell.split("—")[0].strip())
    return out


def capability_keys(root: Path) -> dict[str, str]:
    """Short keys operators tag requirements with, mapped to the full entry."""
    keys = {}
    for cap in capabilities(root):
        key = re.sub(r"[^a-z0-9]+", "-", cap.lower()).strip("-")
        keys[key] = cap
    return keys


def unmapped_requirements(root: Path, opp: m.Opportunity) -> list[tuple[str, str]]:
    """In-scope requirements not tagged with an approved capability."""
    valid = set(capability_keys(root))
    out = []
    for r in opp.in_scope():
        if not r.capability:
            out.append((r.ref, "no capability tag"))
        elif r.capability not in valid:
            out.append((r.ref, f"capability {r.capability!r} is not in SERVICES.md §3"))
    return out


def buyer_roles(root: Path) -> dict[str, list[str]]:
    """Confirmed buyer roles from `ICP.md` §7 (D-021).

    Read live rather than hard-coded: these were open until Discovery Round 2
    and the shape may change again as real buyer evidence accumulates.
    """
    text = (root / "ICP.md").read_text(encoding="utf-8")
    out: dict[str, list[str]] = {"primary": [], "secondary": []}
    for key, label in (("primary", r"\*\*Primary economic buyers\.\*\*(.+?)\n\n"),
                       ("secondary", r"\*\*Secondary buyers and champions\.\*\*(.+?)\n\n")):
        mm = re.search(label, text, re.S)
        if mm:
            out[key] = [r.strip() for r in mm.group(1).replace("\n", " ").split("·") if r.strip()]
    return out


def size_bands(root: Path) -> list[tuple[str, str]]:
    """Confirmed size bands from `ICP.md` §2.1 (D-021)."""
    text = (root / "ICP.md").read_text(encoding="utf-8")
    mm = re.search(r"^## 2\.1 Size Bands(.*?)(?=^## )", text, re.M | re.S)
    if not mm:
        return []
    out = []
    for line in mm.group(1).splitlines():
        line = line.strip()
        if line.startswith("|") and "employees" in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2:
                out.append((cells[0], re.sub(r"\*\*", "", cells[1])))
    return out


def channels(root: Path) -> list[tuple[str, str]]:
    """Confirmed acquisition channels in priority order from `MARKETING.md` §3."""
    text = (root / "MARKETING.md").read_text(encoding="utf-8")
    mm = re.search(r"^## 3\. Core Channels(.*?)(?=^### 3\.1)", text, re.M | re.S)
    if not mm:
        return []
    out = []
    for line in mm.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or "Why this order" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[0].isdigit():
            name = re.sub(r"\*\*", "", cells[1]).split("—")[0].strip()
            out.append((cells[0], name))
    return out


def outbound_signals(root: Path) -> list[str]:
    """Observable digital-maturity-gap indicators from `MARKETING.md` §3.1."""
    text = (root / "MARKETING.md").read_text(encoding="utf-8")
    mm = re.search(r"^### 3\.1 Outbound Target Signals(.*?)(?=^### )", text, re.M | re.S)
    if not mm:
        return []
    body = mm.group(1)
    inner = re.search(r"\(D-026\):(.+?)\.\s*$", body, re.S)
    raw = inner.group(1) if inner else body
    return [x.strip() for x in raw.replace("\n", " ").split(";") if x.strip()]


def service_stages() -> list[str]:
    return ["Entry", "Expansion", "Recurring"]


# --------------------------------------------------------------------------
# Approval gates — governance/AUTHORITY.md §7 reserves these to the founder
# --------------------------------------------------------------------------

GATES = {
    "qualification": (
        "The qualify/disqualify decision",
        "sops/sales/QUALIFICATION.md §3, §10",
    ),
    "solution": (
        "What solution to propose",
        "sops/sales/SOLUTION_DESIGN.md §3 (D-010)",
    ),
    "proposal_issue": (
        "Issuing a proposal — a client-facing commercial commitment",
        "sops/sales/PROPOSAL.md §3, governance/AUTHORITY.md §7",
    ),
    "kickoff": (
        "Beginning delivery against an executed agreement",
        "sops/delivery/ONBOARDING.md §2",
    ),
}


def require_founder(gate: str, approver: str | None) -> str:
    """Return the approver, or raise. `--approved-by` is the founder acting."""
    what, where = GATES[gate]
    if not approver:
        raise m.ApprovalRequired(
            f"{what} is reserved to the founder ({where}).\n"
            f"  Re-run with --approved-by 'Founder' once you have decided."
        )
    return approver


# --------------------------------------------------------------------------
# Proposal issuance gate — SERVICES.md §4 vs the open register
# --------------------------------------------------------------------------

def proposal_gate(root: Path, opp: m.Opportunity) -> list[str]:
    """Blockers preventing a compliant proposal. Empty list == clear to issue.

    Pricing no longer appears here: D-038 sets the price points, so
    `SERVICES.md` §4 is satisfied by the approved configuration rather than by a
    per-engagement declaration. What remains are the controls that were never
    about pricing — an approved solution, sourced requirements, and scope the
    company has actually said it delivers.
    """
    blockers: list[str] = []
    if not opp.solution.approved_by:
        blockers.append(
            "Solution not approved. The scope must be founder-approved before it is "
            "proposed (sops/sales/SOLUTION_DESIGN.md §3, D-010)."
        )
    unsourced = [r.ref for r in opp.in_scope() if not r.source]
    if unsourced:
        blockers.append(
            f"Requirement(s) with no source: {', '.join(unsourced)}. "
            f"A requirement with no source is removed, not justified "
            f"(sops/sales/SOLUTION_DESIGN.md §5.2)."
        )
    unmapped = unmapped_requirements(root, opp)
    if unmapped:
        blockers.append(
            "Requirement(s) not delivered by an approved capability: "
            + ", ".join(ref for ref, _ in unmapped)
            + " (SERVICES.md §3)."
        )
    terms = (opp.proposal.commercial_terms or "").strip()
    if not terms or terms.lower() in ("to be determined", "tbd"):
        blockers.append(
            "Commercial terms not set. Prices are approved (SERVICES.md §2.4) but the "
            "figure for THIS engagement is a founder decision — the entry range is "
            "$7,500–$25,000 and the price follows the solution design. Record it with "
            "`mg gate <slug> --terms '...' --terms-decided --approved-by Founder`."
        )
    money = scan_for_open_values(root, terms)
    blockers.extend(money)
    return blockers


# --------------------------------------------------------------------------
# Readiness checks per stage — what is missing before this stage can advance
# --------------------------------------------------------------------------

def missing_for(stage: str, opp: m.Opportunity) -> list[str]:
    q, d, s = opp.qualification, opp.discovery, opp.solution
    if stage == "qualification":
        miss = []
        if not q.source:
            miss.append("lead source (channel evidence, D-026)")
        if not q.problem:
            miss.append("the problem in the prospect's own words")
        if not q.desired_outcome:
            miss.append("desired outcome")
        if q.authority_confirmed is None:
            miss.append("who owns the decision and who controls budget")
        if not q.fit.high_fit_signals and not q.fit.problem_signals:
            miss.append("at least one matched ICP signal (ICP.md §4-§5)")
        if q.fit.feasible is None:
            miss.append("delivery feasibility assessment")
        if not q.fit.stage:
            miss.append("engagement stage in the progression (SERVICES.md §2)")
        return miss
    if stage == "discovery":
        miss = []
        if not d.held_on:
            miss.append("discovery date")
        if not d.findings:
            miss.append("findings")
        if not d.objectives:
            miss.append("business objectives")
        if not d.problems:
            miss.append("problems")
        if not d.success_indicators:
            miss.append("success indicators with a data source (METRICS.md §2)")
        if not any(st.get("role") for st in d.stakeholders):
            miss.append("stakeholder map")
        if not d.playback_confirmed:
            miss.append("client playback confirmation (DISCOVERY.md §5.9 — mandatory)")
        return miss
    if stage == "solution":
        miss = []
        if not s.problem_restatement:
            miss.append("problem restatement in the client's words")
        if not opp.in_scope():
            miss.append("at least one in-scope requirement")
        if not s.stage:
            miss.append("engagement stage (SERVICES.md §2)")
        if not s.feasibility:
            miss.append("feasibility assessment")
        if not s.verified_against_discovery:
            miss.append("verification against discovery (SOLUTION_DESIGN.md §5.8)")
        return miss
    if stage == "project":
        p = opp.project
        miss = []
        if not p.acceptance_criteria:
            miss.append("acceptance criteria (ONBOARDING.md §5.9)")
        if not p.approvers:
            miss.append("named approver per phase (ONBOARDING.md §5.4)")
        if not p.client_dependencies:
            miss.append("client-side dependencies (ONBOARDING.md §5.7)")
        return miss
    return []


_STOP = {
    "that", "this", "with", "from", "they", "their", "them", "have", "has",
    "been", "were", "which", "when", "what", "into", "than", "then", "there",
    "would", "could", "should", "about", "because", "while", "where", "does",
    "not", "and", "the", "for", "are", "but",
}


def _terms(text: str) -> set[str]:
    """Content words, crudely stemmed, for overlap comparison."""
    out = set()
    for w in re.findall(r"[a-z]{4,}", text.lower()):
        if w in _STOP:
            continue
        out.add(w[:-1] if w.endswith("s") and not w.endswith("ss") else w)
    return out


def contradictions(opp: m.Opportunity) -> list[tuple[str, list[str]]]:
    """Confirmed findings on one topic attributed to different people.

    Not semantic contradiction detection — that needs judgement. This is the
    mechanical signal that reliably precedes one: two people told us something
    about the same thing, and only one version can be carried into a proposal.
    """
    by_topic: dict[str, list[m.Finding]] = {}
    for f in opp.discovery.findings:
        if f.confirmed and f.topic:
            by_topic.setdefault(f.topic.strip().lower(), []).append(f)
    out = []
    for topic, group in by_topic.items():
        sources = {(f.source or "").strip().lower() for f in group}
        if len(group) > 1 and len(sources) > 1:
            out.append((group[0].topic, [f"{f.ref}: {f.statement} — {f.source}" for f in group]))
    return out


def unaddressed_problems(opp: m.Opportunity, threshold: int = 2) -> list[str]:
    """Discovery problems that no requirement — in scope or deferred — appears to touch.

    Advisory, not blocking. Matching is lexical, so it is deliberately
    conservative: it flags a problem only when the overlap with every
    requirement is very low, because a detector that cries wolf trains the
    operator to ignore it.
    """
    corpus = _terms(" ".join(
        f"{r.statement} {r.source} {r.deferred_reason}" for r in opp.solution.requirements
    ))
    if not corpus:
        return list(opp.discovery.problems)
    out = []
    for prob in opp.discovery.problems:
        if len(_terms(prob) & corpus) < threshold:
            out.append(prob)
    return out
