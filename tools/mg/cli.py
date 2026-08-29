"""mg — the operating CLI for The Milbourne Group commercial pipeline.

One command per documented step. Each writes the structured record, re-renders
the artifacts the SOP requires, and refuses anything the operating system
reserves to the founder.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import model as m, store, render, governance as gov, ai, metrics

# ---------------------------------------------------------------- output ----

class C:
    B = "\033[1m"; D = "\033[2m"; R = "\033[0m"
    OK = "\033[32m"; WARN = "\033[33m"; ERR = "\033[31m"; ACC = "\033[36m"

def _tty() -> bool:
    return sys.stdout.isatty()

def c(s, code):
    return f"{code}{s}{C.R}" if _tty() else s

def ok(s):   print(f"{c('✓', C.OK)} {s}")
def warn(s): print(f"{c('!', C.WARN)} {s}")
def err(s):  print(f"{c('✗', C.ERR)} {s}", file=sys.stderr)
def head(s): print(f"\n{c(s, C.B)}")
def dim(s):  print(c(s, C.D))


def _save_and_render(root: Path, opp: m.Opportunity) -> list[str]:
    store.save(root, opp)
    written = []
    for name, content in render.render_all(opp, root).items():
        store.write_artifact(root, opp.slug, name, content)
        written.append(name)
    return written


def _report_render(written):
    dim(f"  rendered: {', '.join(sorted(written))}")


def _next_action(root: Path, opp: m.Opportunity) -> str:
    s = opp.status
    if s == m.PROSPECT:
        miss = gov.missing_for("qualification", opp)
        if miss:
            return f"Collect: {miss[0]}  →  mg set {opp.slug} --help"
        return f"mg qualify {opp.slug} --outcome Qualified --approved-by Founder"
    if s == m.QUALIFIED:
        return f"mg brief {opp.slug} discovery-prep   then   mg discovery {opp.slug} --held-on <date>"
    if s == m.DISCOVERY:
        miss = gov.missing_for("discovery", opp)
        if miss:
            return f"Discovery incomplete: {miss[0]}"
        return f"mg brief {opp.slug} solution   then   mg solution {opp.slug} --approved-by Founder"
    if s == m.PROPOSAL:
        p = opp.proposal
        if not p.issued_on:
            blockers = gov.proposal_gate(root, opp)
            return ("Clear the issuance gate: mg gate " + opp.slug) if blockers else \
                   f"mg propose {opp.slug} --approved-by Founder"
        if not p.outcome:
            nf = opp.next_follow_up()
            return (f"Follow up: {nf.action} (due {nf.due})" if nf
                    else f"mg followup {opp.slug} --action '...' --due <date>")
        return f"mg outcome {opp.slug} --outcome Accepted"
    if s == m.ONBOARDING:
        miss = gov.missing_for("project", opp)
        if miss:
            return f"Onboarding needs: {miss[0]}"
        return f"mg kickoff {opp.slug} --approved-by Founder"
    if s == m.ACTIVE:
        return "Delivery in progress — sops/delivery/"
    if s in m.TERMINAL:
        return "—"
    return "—"


# ---------------------------------------------------------------- commands ---

def cmd_new(root, a):
    slug = a.slug or m.slugify(a.company)
    if store.exists(root, slug) and not a.force:
        err(f"{slug} already exists. Use --force to overwrite, or pick --slug.")
        return 1
    opp = m.Opportunity(slug=slug, created_on=m.today())
    opp.company.name = a.company
    opp.company.website = a.website or ""
    opp.company.industry = a.industry or ""
    opp.company.approximate_size = a.size or ""
    opp.qualification.source = a.source or ""
    if a.contact:
        opp.contacts.append(m.Contact(name=a.contact, role=a.role or "",
                                      email=a.email or "", phone=a.phone or ""))
    opp.qualification.problem = a.problem or ""
    opp.qualification.desired_outcome = a.outcome_wanted or ""
    opp.log("created", f"lead captured from {a.source or 'unrecorded source'}", a.actor)
    opp.set_status(m.PROSPECT, a.actor, "lead captured")
    written = _save_and_render(root, opp)
    ok(f"Created {c(slug, C.ACC)} — {opp.company.name}")
    _report_render(written)
    miss = gov.missing_for("qualification", opp)
    if miss:
        head("Missing before qualification can conclude")
        for x in miss:
            print(f"  - {x}")
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_set(root, a):
    opp = store.load(root, a.slug)
    changed = []
    fieldmap = {
        "website": (opp.company, "website"), "industry": (opp.company, "industry"),
        "size": (opp.company, "approximate_size"), "location": (opp.company, "location"),
        "source": (opp.qualification, "source"), "problem": (opp.qualification, "problem"),
        "desired_outcome": (opp.qualification, "desired_outcome"),
    }
    for key, (obj, attr) in fieldmap.items():
        val = getattr(a, key, None)
        if val:
            setattr(obj, attr, val); changed.append(attr)
    if a.authority is not None:
        opp.qualification.authority_confirmed = a.authority; changed.append("authority_confirmed")
    if a.stage:
        opp.qualification.fit.stage = a.stage; changed.append("fit.stage")
    if a.feasible is not None:
        opp.qualification.fit.feasible = a.feasible; changed.append("fit.feasible")
    if a.signal:
        opp.qualification.fit.problem_signals = sorted(
            set(opp.qualification.fit.problem_signals + a.signal))
        changed.append("problem_signals")
    if a.fit_signal:
        opp.qualification.fit.high_fit_signals = sorted(
            set(opp.qualification.fit.high_fit_signals + a.fit_signal))
        changed.append("high_fit_signals")
    if a.disqualifier:
        opp.qualification.fit.disqualifying_signals = sorted(
            set(opp.qualification.fit.disqualifying_signals + a.disqualifier))
        changed.append("disqualifying_signals")
    if a.contact:
        opp.contacts.append(m.Contact(name=a.contact, role=a.role or "",
                                      email=a.email or "",
                                      is_decision_maker=a.decision_maker))
        changed.append("contacts")
    if not changed:
        warn("Nothing to set."); return 1
    opp.log("update", ", ".join(changed), a.actor)
    written = _save_and_render(root, opp)
    ok(f"Updated {a.slug}: {', '.join(changed)}")
    _report_render(written)
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_qualify(root, a):
    opp = store.load(root, a.slug)
    miss = gov.missing_for("qualification", opp)
    if miss and a.outcome == "Qualified" and not a.force:
        err("Cannot qualify — required information is missing:")
        for x in miss:
            print(f"    - {x}", file=sys.stderr)
        dim("  (--force overrides, but the SOP's quality check will fail)")
        return 1
    try:
        approver = gov.require_founder("qualification", a.approved_by)
    except m.ApprovalRequired as e:
        err(str(e)); return 1

    q = opp.qualification
    q.outcome = a.outcome
    q.outcome_reasoning = a.reasoning or ""
    q.decided_by = approver
    q.decided_on = m.today()

    target = {"Qualified": m.QUALIFIED, "Nurture": m.NURTURE,
              "Disqualified": m.DISQUALIFIED, "Clarification required": m.PROSPECT}[a.outcome]
    try:
        opp.set_status(target, approver, a.outcome)
    except m.StageError as e:
        err(str(e)); return 1
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — {c(a.outcome, C.ACC)} (decided by {approver})")
    _report_render(written)
    if a.outcome == "Disqualified":
        dim("  Directory retained. The reasoning is evidence for Q-001 and Q-003 (ICP.md §7).")
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_discovery(root, a):
    opp = store.load(root, a.slug)
    d = opp.discovery
    if a.scheduled_for: d.scheduled_for = a.scheduled_for
    if a.held_on:       d.held_on = a.held_on
    if a.attendee:      d.attendees = sorted(set(d.attendees + a.attendee))
    if a.transcript:    d.transcript_path = a.transcript
    if a.playback:
        d.playback_confirmed = True
        d.playback_on = a.playback if isinstance(a.playback, str) else m.today()
    if opp.status == m.QUALIFIED and d.held_on:
        try:
            opp.set_status(m.DISCOVERY, a.actor, "discovery held")
        except m.StageError as e:
            err(str(e)); return 1
    opp.log("discovery", "updated", a.actor)
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — discovery updated")
    _report_render(written)
    miss = gov.missing_for("discovery", opp)
    if miss:
        head("Outstanding before solution design")
        for x in miss:
            print(f"  - {x}")
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_solution(root, a):
    opp = store.load(root, a.slug)
    if not opp.discovery.playback_confirmed and not a.force:
        err("Discovery playback not confirmed. `sops/sales/DISCOVERY.md` §5.9 makes it "
            "mandatory before any solution design.")
        dim("  mg discovery <slug> --playback  (once the client has corrected your understanding)")
        return 1
    s = opp.solution
    if a.restate:   s.problem_restatement = a.restate
    if a.stage:     s.stage = a.stage
    if a.feasibility: s.feasibility = a.feasibility
    if a.verified:  s.verified_against_discovery = True

    unsourced = [r.ref for r in opp.in_scope() if not r.source]
    if unsourced:
        err(f"Requirement(s) with no source: {', '.join(unsourced)}")
        dim("  A requirement with no source is removed, not justified "
            "(sops/sales/SOLUTION_DESIGN.md §5.2).")
        return 1

    if a.approved_by:
        miss = gov.missing_for("solution", opp)
        if miss and not a.force:
            err("Cannot approve the solution — missing:")
            for x in miss:
                print(f"    - {x}", file=sys.stderr)
            return 1
        s.approved_by = gov.require_founder("solution", a.approved_by)
        s.approved_on = m.now()
        try:
            opp.set_status(m.PROPOSAL, s.approved_by, "solution approved")
        except m.StageError:
            pass
    opp.log("solution", "updated", a.actor)
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — solution updated"
       + (f" · approved by {s.approved_by}" if s.approved_by else ""))
    _report_render(written)
    un = gov.unaddressed_problems(opp)
    if un:
        head("Discovery problems with no matching requirement")
        for p in un:
            print(f"  - {p}")
        dim("  Address it or record it as an explicit exclusion — silence becomes a dispute.")
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_gate(root, a):
    opp = store.load(root, a.slug)
    p = opp.proposal
    mutating = a.terms_decided or a.deliverables_defined or a.terms or a.note
    if mutating:
        try:
            approver = gov.require_founder("proposal_issue", a.approved_by)
        except m.ApprovalRequired as e:
            err(str(e)); return 1
        # Commercial terms carry a figure only once the founder has decided them.
        # Passing --terms without --terms-decided is the exact path by which an
        # invented price would reach a client-facing document.
        if a.terms:
            if not (a.terms_decided or p.gate_terms_decided):
                for x in gov.scan_for_open_values(root, a.terms):
                    err(x)
                err("Terms not recorded. Pricing is open (Q-007): either decide it for this "
                    "engagement with --terms-decided, or leave terms as 'to be determined'.")
                return 1
            problems = gov.scan_for_open_values(root, a.terms) if not a.terms_decided else []
            if problems:
                for x in problems:
                    err(x)
                return 1
            p.commercial_terms = a.terms
            opp.log("gate", "commercial terms recorded", approver)
        if a.terms_decided:
            p.gate_terms_decided = True
            opp.log("gate", "commercial terms decided for this engagement", approver)
        if a.deliverables_defined:
            p.gate_deliverables_defined = True
            opp.log("gate", "deliverables defined for this engagement", approver)
        if a.note:
            p.gate_notes = a.note
        _save_and_render(root, opp)
        ok("Gate updated.")
    blockers = gov.proposal_gate(root, opp)
    head(f"Issuance gate — {a.slug}")
    if not blockers:
        ok("Clear to issue.")
    else:
        for b in blockers:
            warn(b)
    return 0


def cmd_propose(root, a):
    opp = store.load(root, a.slug)
    blockers = gov.proposal_gate(root, opp)
    if blockers and not a.force:
        err("Proposal cannot be issued:")
        for b in blockers:
            print(f"    - {b}", file=sys.stderr)
        return 1
    try:
        approver = gov.require_founder("proposal_issue", a.approved_by)
    except m.ApprovalRequired as e:
        err(str(e)); return 1

    p = opp.proposal
    if a.terms:
        problems = gov.scan_for_open_values(root, a.terms) if not p.gate_terms_decided else []
        if problems:
            for x in problems:
                err(x)
            return 1
        p.commercial_terms = a.terms
    p.version += 1
    p.issued_on = m.today()
    p.issued_at = m.now()
    p.approved_by = approver
    p.valid_until = a.valid_until or ""
    p.revisions.append({
        "version": p.version, "date": m.today(),
        "changed": a.changed or ("initial issue" if p.version == 1 else "revision"),
        "why": a.why or "",
    })
    opp.log("proposal", f"issued v{p.version}", approver)
    if not opp.follow_ups:
        opp.follow_ups.append(m.FollowUp(
            action="Confirm receipt and answer questions on the proposal",
            owner="Founder", due=a.follow_up_due or "", note="auto-created at issue"))
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — proposal v{p.version} issued by {approver}")
    _report_render(written)
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_followup(root, a):
    opp = store.load(root, a.slug)
    if a.done:
        openf = opp.open_follow_ups()
        if not openf:
            warn("No open follow-up."); return 1
        target = next((f for f in openf if a.done in f.action), openf[0])
        target.done_on = m.today()
        target.note = a.note or target.note
        opp.log("followup", f"completed: {target.action}", a.actor)
        ok(f"Completed: {target.action}")
    if a.action:
        opp.follow_ups.append(m.FollowUp(action=a.action, owner=a.owner or "Founder",
                                         due=a.due or "", note=a.note or ""))
        opp.log("followup", f"scheduled: {a.action}", a.actor)
        ok(f"Scheduled: {a.action} — {a.owner or 'Founder'}, due {a.due or 'unset'}")
    _save_and_render(root, opp)
    head(f"Follow-up state — {a.slug}")
    print(f"  Last:  {opp.events[-1].detail if opp.events else '—'}")
    nf = opp.next_follow_up()
    print(f"  Next:  {nf.action if nf else '—'}")
    print(f"  Owner: {nf.owner if nf else '—'}")
    print(f"  When:  {nf.due if nf else '—'}")
    return 0


def cmd_outcome(root, a):
    opp = store.load(root, a.slug)
    p = opp.proposal
    if not p.issued_on:
        err("No proposal has been issued."); return 1
    p.outcome = a.outcome
    p.outcome_on = m.today()
    p.outcome_reasoning = a.reasoning or ""
    if a.outcome in ("Declined", "No decision"):
        if not a.loss_reason and not a.force:
            err("Loss reasoning is required. It is the strongest evidence available for "
                "Q-001 and Q-003 (ICP.md §7); a loss recorded only as 'lost' teaches "
                "the company nothing (sops/sales/PROPOSAL.md §5.10).")
            dim("  --loss-reason 'scope|price|timing|trust|competitor|no decision — detail'")
            return 1
        p.loss_reason = a.loss_reason or ""
    target = {"Accepted": m.ONBOARDING, "Negotiated": m.PROPOSAL,
              "Declined": m.LOST, "No decision": m.NURTURE}[a.outcome]
    try:
        opp.set_status(target, a.actor, f"proposal {a.outcome.lower()}")
    except m.StageError as e:
        err(str(e)); return 1
    for f in opp.open_follow_ups():
        f.done_on = m.today()
    opp.log("proposal", f"outcome {a.outcome}", a.actor)
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — proposal {c(a.outcome, C.ACC)} · status {opp.status}")
    _report_render(written)
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_init_project(root, a):
    opp = store.load(root, a.slug)
    if opp.status != m.ONBOARDING and not a.force:
        err(f"Status is {opp.status}. Project initialization follows an accepted "
            f"proposal (sops/delivery/ONBOARDING.md §2).")
        return 1
    pr = opp.project
    if a.acceptance:  pr.acceptance_criteria = list(a.acceptance)
    if a.approver:
        for spec in a.approver:
            phase, _, who = spec.partition("=")
            pr.approvers.append({"phase": phase.strip(), "approver": who.strip() or "Founder"})
    if a.access:
        for spec in a.access:
            what, _, where = spec.partition("=")
            if gov.scan_for_open_values(root, where):
                pass
            pr.access_items.append({"what": what.strip(), "where": where.strip()})
    if a.dependency: pr.client_dependencies = list(a.dependency)
    pr.initialized_on = m.today()
    pr.brief_complete = bool(pr.acceptance_criteria and pr.approvers)
    opp.log("project", "initialized from sales record", a.actor)
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — project initialized")
    _report_render(written)
    dim(f"  Carried forward without re-entry: "
        f"{len(opp.in_scope())} requirements, {len(opp.discovery.objectives)} objectives, "
        f"{len(opp.discovery.risks)} risks, {len(opp.discovery.stakeholders)} stakeholders, "
        f"{len(opp.discovery.success_indicators)} success indicators")
    miss = gov.missing_for("project", opp)
    if miss:
        head("Outstanding before kickoff")
        for x in miss:
            print(f"  - {x}")
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_kickoff(root, a):
    opp = store.load(root, a.slug)
    miss = gov.missing_for("project", opp)
    if miss and not a.force:
        err("Cannot hold kickoff — missing:")
        for x in miss:
            print(f"    - {x}", file=sys.stderr)
        return 1
    try:
        approver = gov.require_founder("kickoff", a.approved_by)
    except m.ApprovalRequired as e:
        err(str(e)); return 1
    opp.project.kickoff_on = m.today()
    try:
        opp.set_status(m.ACTIVE, approver, "onboarding complete, delivery begins")
    except m.StageError as e:
        err(str(e)); return 1
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — kickoff held, status {c(m.ACTIVE, C.ACC)}")
    _report_render(written)
    return 0


def cmd_status(root, a):
    opp = store.load(root, a.slug)
    head(f"{opp.company.name or opp.slug}  ({opp.slug})")
    print(f"  Status      {c(opp.status, C.ACC)}   {c('set by ' + m.ASSIGNED_BY.get(opp.status,'—'), C.D)}")
    print(f"  Stage       {opp.solution.stage or opp.qualification.fit.stage or '—'}")
    print(f"  Source      {opp.qualification.source or '—'}")
    dm = opp.decision_maker
    print(f"  Decider     {dm.name if dm else c('not established', C.WARN)}")
    cyc = metrics.cycle_days(opp)
    if cyc is not None:
        print(f"  Cycle       {cyc} days (closed)")
    else:
        age = metrics.age_days(opp)
        print(f"  Age         {age} days open" if age is not None else "  Age         —")

    head("Pipeline")
    stages = [("Lead", True), ("Qualified", metrics._reached(opp, m.QUALIFIED)),
              ("Discovery", metrics._reached(opp, m.DISCOVERY)),
              ("Solution", bool(opp.solution.approved_by)),
              ("Proposal", bool(opp.proposal.issued_on)),
              ("Won", metrics._reached(opp, m.ONBOARDING)),
              ("Project", bool(opp.project.initialized_on))]
    print("  " + "  ".join(
        (c("●", C.OK) if done else c("○", C.D)) + f" {name}" for name, done in stages))

    head("Follow-up")
    last = next((e for e in reversed(opp.events) if e.kind != "update"), None)
    print(f"  What happened last  {last.detail if last else '—'} {c('(' + last.at[:10] + ')', C.D) if last else ''}")
    nf = opp.next_follow_up()
    print(f"  What happens next   {nf.action if nf else '—'}")
    print(f"  Who owns it         {nf.owner if nf else '—'}")
    print(f"  When                {nf.due or 'unset' if nf else '—'}")

    if opp.status == m.PROPOSAL:
        blockers = gov.proposal_gate(root, opp)
        if blockers:
            head("Issuance gate")
            for b in blockers:
                warn(b)
    head("Next")
    print(f"  {_next_action(root, opp)}")
    return 0


def cmd_list(root, a):
    opps = store.load_all(root)
    if not opps:
        warn("No opportunities. `mg new --company '...'` to capture a lead.")
        return 0
    if a.status:
        opps = [o for o in opps if o.status == a.status]
    if not a.all:
        opps = [o for o in opps if o.status not in m.TERMINAL] or opps
    head(f"{len(opps)} opportunit{'y' if len(opps)==1 else 'ies'}")
    w = max((len(o.slug) for o in opps), default=8)
    for o in sorted(opps, key=lambda x: (m.STATUSES.index(x.status), x.slug)):
        nf = o.next_follow_up()
        print(f"  {o.slug:<{w}}  {c(o.status, C.ACC):<22} "
              f"{(o.company.name or '')[:24]:<26} "
              f"{c((nf.action[:38] + '…') if nf and len(nf.action) > 38 else (nf.action if nf else '—'), C.D)}")
    return 0


def cmd_brief(root, a):
    opp = store.load(root, a.slug)
    try:
        print(ai.packet(root, opp, a.task))
    except KeyError as e:
        err(str(e)); return 1
    return 0


def cmd_ingest(root, a):
    opp = store.load(root, a.slug)
    raw = Path(a.from_file).read_text(encoding="utf-8") if a.from_file else sys.stdin.read()
    try:
        data = ai.extract_json(raw)
    except Exception as e:
        err(f"Could not parse result: {e}"); return 1
    changed = ai.ingest(opp, a.task, data)
    if not changed:
        warn("Nothing merged."); return 1
    opp.log("ingest", f"{a.task}: {', '.join(changed)}", "ai")
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — merged {a.task}")
    for x in changed:
        print(f"    + {x}")
    _report_render(written)

    if a.task == "discovery-analysis":
        d = opp.discovery
        inferred = [f for f in d.findings if not f.confirmed]
        if inferred:
            head("Inferences — not client statements, must stay labelled")
            for f in inferred:
                print(f"  {c(f.ref, C.WARN)} {f.statement}")
    if a.task == "solution":
        uns = [r.ref for r in opp.in_scope() if not r.source]
        if uns:
            head("Unsourced requirements — remove or convert to a labelled assumption")
            for r in uns:
                print(f"  {c(r, C.ERR)}")
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_check(root, a):
    """Governance check across the pipeline."""
    opps = store.load_all(root)
    problems = 0
    head("Governance check")
    qs = gov.open_questions(root)
    openq = [q for q in qs.values() if not q["resolved"]]
    print(f"  Open questions: {len(openq)} of {len(qs)}"
          f"  ({', '.join(q['id'] for q in openq if q['priority']=='Blocking')} blocking)")
    for o in opps:
        issues = []
        d = store.opp_dir(root, o.slug)
        for f in d.rglob("*.md"):
            hits = gov.scan_for_open_values(root, f.read_text(encoding="utf-8"))
            if hits:
                issues.append(f"{f.name}: {hits[0]}")
        if o.status not in m.STATUSES:
            issues.append(f"invalid status {o.status!r}")
        for r in o.in_scope():
            if not r.source:
                issues.append(f"requirement {r.ref} has no source")
        for fnd in o.discovery.findings:
            if not fnd.confirmed and not fnd.source:
                issues.append(f"inference {fnd.ref} has no stated basis")
        if o.status == m.ACTIVE and not o.project.acceptance_criteria:
            issues.append("delivery active with no acceptance criteria")
        if issues:
            problems += len(issues)
            print(f"\n  {c(o.slug, C.WARN)}")
            for i in issues:
                print(f"    - {i}")
    print()
    if problems:
        err(f"{problems} issue(s) found.")
        return 1
    ok("No governance issues found.")
    return 0


def cmd_metrics(root, a):
    opps = store.load_all(root)
    s = metrics.summarize(opps)
    if a.json:
        print(json.dumps(s, indent=2)); return 0
    head("Pipeline")
    rows = [
        ("Leads", s["leads"], ""),
        ("Qualified", s["qualified"], f"{s['qualified_rate']}% of leads" if s["qualified_rate"] is not None else ""),
        ("Discovery", s["discovery"], f"{s['discovery_conversion']}% of qualified" if s["discovery_conversion"] is not None else ""),
        ("Proposals", s["proposals"], f"{s['proposal_conversion']}% of discovery" if s["proposal_conversion"] is not None else ""),
        ("Won", s["won"], f"{s['close_rate']}% close rate" if s["close_rate"] is not None else ""),
        ("Lost / disqualified", s["lost"], ""),
        ("Open", s["open"], ""),
    ]
    for label, val, note in rows:
        print(f"  {label:<22}{c(str(val), C.B):<14}{c(note, C.D)}")
    head("Cycle")
    print(f"  {'Avg sales cycle':<22}{s['avg_cycle_days'] if s['avg_cycle_days'] is not None else '—'} days")
    print(f"  {'Avg proposal build':<22}"
          f"{s['avg_proposal_hours'] if s['avg_proposal_hours'] is not None else '—'} hours"
          f"   {c('(solution approved → issued)', C.D)}")
    if s["by_status"]:
        head("By status")
        for k, v in s["by_status"].items():
            print(f"  {k:<22}{v}")
    if s["by_source"]:
        head("By source   " + c("(evidence for Q-008)", C.D))
        for k, v in s["by_source"].items():
            label = k if len(k) <= 44 else k[:43] + "…"
            print(f"  {label:<46}{v}")
    return 0


def cmd_render(root, a):
    opp = store.load(root, a.slug)
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — re-rendered from record")
    _report_render(written)
    return 0


# ---------------------------------------------------------------- parser ----

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mg",
        description="The Milbourne Group commercial pipeline. "
                    "One command per documented step; the record is the source of truth.")
    p.add_argument("--actor", default="Founder", help="who is performing this action")
    sub = p.add_subparsers(dest="cmd", required=True)

    n = sub.add_parser("new", help="capture a lead")
    n.add_argument("--company", required=True)
    n.add_argument("--slug"); n.add_argument("--source")
    n.add_argument("--contact"); n.add_argument("--role"); n.add_argument("--email")
    n.add_argument("--phone"); n.add_argument("--website"); n.add_argument("--industry")
    n.add_argument("--size"); n.add_argument("--problem")
    n.add_argument("--outcome-wanted", dest="outcome_wanted")
    n.add_argument("--force", action="store_true")
    n.set_defaults(fn=cmd_new)

    s = sub.add_parser("set", help="update opportunity fields")
    s.add_argument("slug")
    for f in ("website", "industry", "size", "location", "source", "problem"):
        s.add_argument(f"--{f}")
    s.add_argument("--desired-outcome", dest="desired_outcome")
    s.add_argument("--authority", action=argparse.BooleanOptionalAction, default=None)
    s.add_argument("--stage", choices=gov.service_stages())
    s.add_argument("--feasible", action=argparse.BooleanOptionalAction, default=None)
    s.add_argument("--signal", action="append", help="problem signal from ICP.md §5")
    s.add_argument("--fit-signal", action="append", help="high-fit characteristic, ICP.md §4")
    s.add_argument("--disqualifier", action="append", help="disqualification signal, ICP.md §6")
    s.add_argument("--contact"); s.add_argument("--role"); s.add_argument("--email")
    s.add_argument("--decision-maker", dest="decision_maker",
                   action=argparse.BooleanOptionalAction, default=None)
    s.set_defaults(fn=cmd_set)

    q = sub.add_parser("qualify", help="record the qualification decision (founder)")
    q.add_argument("slug")
    q.add_argument("--outcome", required=True,
                   choices=["Qualified", "Nurture", "Clarification required", "Disqualified"])
    q.add_argument("--reasoning"); q.add_argument("--approved-by", dest="approved_by")
    q.add_argument("--force", action="store_true")
    q.set_defaults(fn=cmd_qualify)

    d = sub.add_parser("discovery", help="schedule, record and confirm discovery")
    d.add_argument("slug")
    d.add_argument("--scheduled-for", dest="scheduled_for")
    d.add_argument("--held-on", dest="held_on")
    d.add_argument("--attendee", action="append")
    d.add_argument("--transcript")
    d.add_argument("--playback", nargs="?", const=True, default=None,
                   help="record client playback confirmation (DISCOVERY.md §5.9)")
    d.set_defaults(fn=cmd_discovery)

    so = sub.add_parser("solution", help="solution design and founder approval")
    so.add_argument("slug")
    so.add_argument("--restate"); so.add_argument("--stage", choices=gov.service_stages())
    so.add_argument("--feasibility")
    so.add_argument("--verified", action="store_true",
                    help="verified against discovery (SOLUTION_DESIGN.md §5.8)")
    so.add_argument("--approved-by", dest="approved_by")
    so.add_argument("--force", action="store_true")
    so.set_defaults(fn=cmd_solution)

    g = sub.add_parser("gate", help="the proposal issuance gate (SERVICES.md §4)")
    g.add_argument("slug")
    g.add_argument("--terms-decided", dest="terms_decided", action="store_true")
    g.add_argument("--deliverables-defined", dest="deliverables_defined", action="store_true")
    g.add_argument("--terms", help="commercial terms as the founder has decided them")
    g.add_argument("--note"); g.add_argument("--approved-by", dest="approved_by")
    g.set_defaults(fn=cmd_gate)

    pr = sub.add_parser("propose", help="issue a proposal (founder)")
    pr.add_argument("slug")
    pr.add_argument("--approved-by", dest="approved_by")
    pr.add_argument("--terms"); pr.add_argument("--valid-until", dest="valid_until")
    pr.add_argument("--changed"); pr.add_argument("--why")
    pr.add_argument("--follow-up-due", dest="follow_up_due")
    pr.add_argument("--force", action="store_true")
    pr.set_defaults(fn=cmd_propose)

    fu = sub.add_parser("followup", help="track what happens next and who owns it")
    fu.add_argument("slug")
    fu.add_argument("--action"); fu.add_argument("--owner"); fu.add_argument("--due")
    fu.add_argument("--note"); fu.add_argument("--done", nargs="?", const="")
    fu.set_defaults(fn=cmd_followup)

    oc = sub.add_parser("outcome", help="record the proposal outcome")
    oc.add_argument("slug")
    oc.add_argument("--outcome", required=True,
                    choices=["Accepted", "Negotiated", "Declined", "No decision"])
    oc.add_argument("--reasoning"); oc.add_argument("--loss-reason", dest="loss_reason")
    oc.add_argument("--force", action="store_true")
    oc.set_defaults(fn=cmd_outcome)

    ip = sub.add_parser("init-project", help="initialize the project from the sales record")
    ip.add_argument("slug")
    ip.add_argument("--acceptance", action="append")
    ip.add_argument("--approver", action="append", metavar="PHASE=WHO")
    ip.add_argument("--access", action="append", metavar="WHAT=WHERE",
                    help="never a credential value (MASTER.md §7.3)")
    ip.add_argument("--dependency", action="append")
    ip.add_argument("--force", action="store_true")
    ip.set_defaults(fn=cmd_init_project)

    k = sub.add_parser("kickoff", help="hold kickoff, move to Active")
    k.add_argument("slug"); k.add_argument("--approved-by", dest="approved_by")
    k.add_argument("--force", action="store_true")
    k.set_defaults(fn=cmd_kickoff)

    st = sub.add_parser("status", help="one opportunity in full")
    st.add_argument("slug"); st.set_defaults(fn=cmd_status)

    ls = sub.add_parser("list", help="the pipeline")
    ls.add_argument("--status", choices=m.STATUSES)
    ls.add_argument("--all", action="store_true")
    ls.set_defaults(fn=cmd_list)

    br = sub.add_parser("brief", help="generate an AI task packet")
    br.add_argument("slug"); br.add_argument("task", choices=sorted(ai.TASKS))
    br.set_defaults(fn=cmd_brief)

    ig = sub.add_parser("ingest", help="merge AI output back into the record")
    ig.add_argument("slug"); ig.add_argument("task", choices=sorted(ai.TASKS))
    ig.add_argument("--from", dest="from_file", help="file with the JSON result; default stdin")
    ig.set_defaults(fn=cmd_ingest)

    ck = sub.add_parser("check", help="governance check across the pipeline")
    ck.set_defaults(fn=cmd_check)

    mt = sub.add_parser("metrics", help="workflow measurement")
    mt.add_argument("--json", action="store_true")
    mt.set_defaults(fn=cmd_metrics)

    rd = sub.add_parser("render", help="re-render artifacts from the record")
    rd.add_argument("slug"); rd.set_defaults(fn=cmd_render)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = gov.repo_root(Path.cwd() / "x")
    except RuntimeError:
        root = gov.repo_root(Path(__file__).resolve())
    try:
        return args.fn(root, args)
    except (m.StageError, m.ApprovalRequired, m.OpenValueError) as e:
        err(str(e)); return 1
    except FileNotFoundError as e:
        err(str(e)); return 1
