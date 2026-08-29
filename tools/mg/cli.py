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

from . import model as m, store, render, governance as gov, ai, metrics, intake

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


def _warn_duplicates(root: Path, company: str, email: str = "", exclude: str = "") -> bool:
    """Report look-alike opportunities. Returns True if any were found."""
    dupes = store.find_duplicates(root, company, email, exclude)
    if dupes:
        warn(f"{len(dupes)} existing opportunit{'y' if len(dupes)==1 else 'ies'} look like this one:")
        for slug, why in dupes:
            print(f"    {c(slug, C.ACC)}  — {why}")
        dim("  Splitting one prospect across two records splits their discovery too.")
    return bool(dupes)


def _confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        err(f"{prompt} Refusing in a non-interactive session — pass --yes to confirm.")
        return False
    try:
        return input(f"{prompt} [y/N] ").strip().lower() in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        print()
        return False


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
        nf = opp.next_follow_up()
        if nf:
            return f"{nf.action} — {nf.owner}" + (f", due {nf.due}" if nf.due else " (no date set)")
        return (f"Delivery in progress with no next action scheduled. "
                f"mg followup {opp.slug} --action '...' --due <date>")
    if s in m.TERMINAL:
        return "—"
    return "—"


# ---------------------------------------------------------------- commands ---

def cmd_new(root, a):
    slug = a.slug or m.slugify(a.company)
    if store.exists(root, slug):
        if not a.force:
            err(f"{slug} already exists. Pick a different --slug, or --force to replace it.")
            return 1
        existing, _ = store.load_quietly(root, slug)
        if existing is not None:
            warn(f"--force will replace {slug}: status {existing.status}, "
                 f"{len(existing.discovery.findings)} finding(s), "
                 f"{len(existing.events)} event(s).")
            dim(f"  The current version is archived and recoverable with `mg restore {slug}`.")
            if not _confirm(f"Replace {slug}?", a.yes):
                err("Cancelled."); return 1
    if _warn_duplicates(root, a.company, getattr(a, "email", "") or "", exclude=slug):
        if not a.duplicate_ok:
            err("Refusing to create a possible duplicate. "
                "Pass --duplicate-ok if these really are different organisations.")
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


def cmd_intake(root, a):
    """Create a lead from a form POST, a forwarded email, or a call note."""
    text = Path(a.from_file).read_text(encoding="utf-8") if a.from_file else sys.stdin.read()
    if not text.strip():
        err("Nothing to intake (empty input)."); return 1
    parsed = intake.parse(text)
    f = parsed["fields"]
    if not f.get("company") and not f.get("contact") and not a.company:
        err("Could not identify a company or a contact in the enquiry.")
        dim("  Pass --company to name it, or add a `Company:` line to the source.")
        return 1
    if a.company:
        f["company"] = a.company
    slug = a.slug or m.slugify(f.get("company") or f.get("contact"))
    if store.exists(root, slug) and not a.force:
        err(f"{slug} already exists. Pick a different --slug, or --force to replace it.")
        dim(f"  To add this enquiry to the existing record instead: mg followup {slug} --note ...")
        return 1
    if _warn_duplicates(root, f.get("company", ""), f.get("email", ""), exclude=slug):
        if not a.duplicate_ok:
            err("Refusing to create a possible duplicate. "
                "Pass --duplicate-ok if these really are different organisations.")
            return 1

    opp = intake.to_opportunity(parsed, slug)
    if a.source:
        opp.qualification.source = a.source
    # The unparsed enquiry is kept verbatim: the record must never lose what
    # the prospect actually wrote, and nothing here may be guessed.
    opp.log("intake", f"lead captured via {a.channel}", a.actor)
    opp.events.append(m.Event(at=m.now(), kind="enquiry", actor=a.channel,
                              detail=parsed["raw"][:4000]))
    opp.set_status(m.PROSPECT, a.actor, f"captured via {a.channel}")
    written = _save_and_render(root, opp)
    ok(f"Captured {c(slug, C.ACC)} via {a.channel}")
    head("Parsed from the enquiry")
    for k, v in f.items():
        print(f"  {k:<16}{v[:70]}{'…' if len(v) > 70 else ''}")
    if parsed["missing"]:
        head("Not stated in the enquiry — ask, do not assume")
        for k in parsed["missing"]:
            print(f"  - {k}")
    _report_render(written)
    print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
    return 0


def cmd_hold(root, a):
    opp = store.load(root, a.slug)
    if a.release:
        if not opp.hold.on_hold:
            warn(f"{a.slug} is not on hold."); return 1
        opp.hold = m.Hold()
        opp.log("hold", "released", a.actor)
        _save_and_render(root, opp)
        ok(f"{a.slug} released from hold — stage {opp.pipeline_stage()}")
        print(f"\n{c('Next:', C.B)} {_next_action(root, opp)}")
        return 0
    if not a.reason:
        err("A hold needs a reason. An opportunity paused without one is an "
            "opportunity that quietly disappears.")
        return 1
    opp.hold = m.Hold(on_hold=True, reason=a.reason, since=m.today(),
                      revisit_on=a.revisit or "")
    opp.log("hold", f"on hold: {a.reason}", a.actor)
    if a.revisit:
        opp.follow_ups.append(m.FollowUp(
            action=f"Revisit hold: {a.reason}", owner=a.owner or "Founder",
            due=a.revisit, note="auto-created when placed on hold"))
    _save_and_render(root, opp)
    ok(f"{a.slug} on hold — {a.reason}")
    if a.revisit:
        dim(f"  Revisit scheduled for {a.revisit}")
    else:
        warn("  No revisit date. Use --revisit <date> so it resurfaces.")
    return 0


def cmd_next(root, a):
    """The whole pipeline: stage, what happened last, what happens next, gaps."""
    loaded, broken = store.load_all_with_errors(root)
    if broken:
        err(f"{len(broken)} record(s) unreadable and NOT shown below:")
        for slug, msg in broken:
            print(f"    {slug}: {msg}")
        dim("  `mg check` explains; `mg restore <slug>` recovers.\n")
    opps = [o for o in loaded if o.status not in m.TERMINAL]
    if not opps:
        warn("Nothing open. `mg intake` or `mg new` to capture a lead.")
        return 0
    overdue = []
    head(f"{len(opps)} open opportunit{'y' if len(opps)==1 else 'ies'}")
    order = ["NEW", "QUALIFYING", "QUALIFIED", "DISCOVERY", "SOLUTION",
             "PROPOSAL", "NEGOTIATION", "WON", "PROJECT INITIALIZED", "ON HOLD"]
    for o in sorted(opps, key=lambda x: (order.index(x.pipeline_stage())
                                         if x.pipeline_stage() in order else 99, x.slug)):
        stage = o.pipeline_stage()
        nf = o.next_follow_up()
        last = next((e for e in reversed(o.events)
                     if e.kind in ("status", "proposal", "followup", "hold", "intake")), None)
        print(f"\n  {c(o.slug, C.B)}  {c(stage, C.ACC)}"
              + (c(f"  (held: {o.hold.reason})", C.WARN) if o.hold.on_hold else ""))
        print(f"    last    {last.detail[:72] if last else '—'}")
        print(f"    next    {nf.action[:72] if nf else _next_action(root, o)}")
        print(f"    owner   {nf.owner if nf else 'Founder'}"
              + (f"    due {nf.due}" if nf and nf.due else ""))
        if nf and nf.due and nf.due < m.today():
            overdue.append((o.slug, nf))
            print(f"    {c('OVERDUE', C.ERR)}")
        gaps = _gaps(root, o)
        if gaps:
            print(f"    {c('missing', C.WARN)} {'; '.join(gaps[:3])}")
    targets, tbroken = store.load_all_targets(root)
    if tbroken:
        err(f"{len(tbroken)} target(s) unreadable: " + ", ".join(x for x, _ in tbroken))
    from . import growth as _gr, growth_cli as _gc
    live = [t for t in targets if t.status not in _gr.TARGET_TERMINAL]
    if live:
        head(f"{len(live)} live target{'' if len(live)==1 else 's'}   "
             + c("(growth engine — upstream of the pipeline)", C.D))
        for t in sorted(live, key=lambda x: _gr.TARGET_STATUSES.index(x.status)):
            print(f"\n  {c(t.slug, C.B)}  {c(t.status, C.ACC)}"
                  + (f"   {t.fit.band}" if t.fit.band else ""))
            print(f"    next    {_gc._next(t)}")
            if t.status == _gr.MONITORING:
                last = next((e for e in reversed(t.events) if e.kind == "monitor"), None)
                if last:
                    print(f"    why     {last.detail[:70]}")
    if overdue:
        head(f"{len(overdue)} overdue")
        for slug, nf in overdue:
            print(f"  {slug:<24}{nf.action[:50]}  {c('due ' + nf.due, C.ERR)}")
    return 0


def _gaps(root: Path, opp: m.Opportunity) -> list[str]:
    """Information the opportunity's current stage still needs."""
    stage = {m.PROSPECT: "qualification", m.QUALIFIED: "qualification",
             m.DISCOVERY: "discovery", m.PROPOSAL: "solution",
             m.ONBOARDING: "project"}.get(opp.status)
    gaps = list(gov.missing_for(stage, opp)) if stage else []
    if opp.status == m.PROPOSAL and not opp.proposal.issued_on:
        blockers = gov.proposal_gate(root, opp)
        if blockers:
            gaps.append(blockers[0].split(" — ")[0])
    return gaps


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

    unmapped = gov.unmapped_requirements(root, opp)
    if unmapped and not a.force:
        err("Requirement(s) not delivered by an approved capability:")
        for ref, why in unmapped:
            stmt = next((r.statement for r in opp.in_scope() if r.ref == ref), "")
            print(f"    {ref}  {stmt[:56]}  — {why}", file=sys.stderr)
        dim("  Offers are assembled from the capabilities in `SERVICES.md` §3. "
            "Work outside them is not something the company has said it does, and "
            "proposing it is how an engagement gets sold that cannot be delivered.")
        dim("  Tag each requirement with one of: "
            + ", ".join(gov.capability_keys(root)))
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
    clashes = gov.contradictions(opp)
    if clashes:
        head("Unresolved contradictions in discovery")
        for topic, items in clashes:
            print(f"  {c(topic, C.WARN)}: " + " | ".join(i.split(':')[0] for i in items))
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
    # An engagement with no next action is one that goes quiet. What delivery
    # waits on first is almost always a client-side dependency.
    if not opp.open_follow_ups():
        first = (opp.project.client_dependencies
                 or ["Confirm delivery start with the client"])[0]
        opp.follow_ups.append(m.FollowUp(
            action=f"Delivery checkpoint — {first}", owner="Founder",
            due=a.first_review or "", note="auto-created at kickoff"))
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — kickoff held, status {c(m.ACTIVE, C.ACC)}")
    _report_render(written)
    return 0


def cmd_drop(root, a):
    """Remove a finding or a requirement from the record.

    Merging on ingest means a mistaken analysis leaves residue. Without this an
    operator would have to hand-edit the JSON, which is how records get broken.
    """
    opp = store.load(root, a.slug)
    removed: list[str] = []
    if a.finding:
        keep, gone = [], []
        for f in opp.discovery.findings:
            (gone if f.ref in a.finding else keep).append(f)
        if gone:
            opp.discovery.findings = keep
            removed += [f"finding {f.ref}: {f.statement[:50]}" for f in gone]
    if a.requirement:
        keep, gone = [], []
        for r in opp.solution.requirements:
            (gone if r.ref in a.requirement else keep).append(r)
        if gone:
            opp.solution.requirements = keep
            removed += [f"requirement {r.ref}: {r.statement[:50]}" for r in gone]
    if not removed:
        wanted = (a.finding or []) + (a.requirement or [])
        err(f"Nothing matched {', '.join(wanted) or 'the given refs'}.")
        return 1
    head(f"Removing from {a.slug}")
    for r in removed:
        print(f"  {r}")
    if not _confirm("Remove these?", a.yes):
        err("Cancelled."); return 1
    opp.log("drop", "; ".join(removed)[:300], a.actor)
    written = _save_and_render(root, opp)
    ok(f"{a.slug} — removed {len(removed)} item(s)")
    dim(f"  Previous version archived; recover with `mg restore {a.slug}`.")
    _report_render(written)
    return 0


def cmd_restore(root, a):
    backups = store.list_backups(root, a.slug)
    if not backups:
        err(f"No archived versions for {a.slug}."); return 1
    if a.list:
        head(f"{len(backups)} archived version(s) — {a.slug}")
        for i, b in enumerate(backups):
            try:
                d = json.loads(b.read_text(encoding="utf-8"))
                desc = f"status {d.get('status','?')}, {len(d.get('events',[]))} events"
            except json.JSONDecodeError:
                desc = c("unreadable", C.ERR)
            print(f"  [{i}] {b.stem:<20} {desc}")
        dim(f"\n  mg restore {a.slug} --version <n>")
        return 0
    idx = a.version
    if not _confirm(f"Restore {a.slug} from version [{idx}] ({backups[idx].stem})? "
                    f"The current record is archived first.", a.yes):
        err("Cancelled."); return 1
    try:
        src = store.restore(root, a.slug, idx)
    except (store.RecordError, IndexError) as e:
        err(str(e)); return 1
    opp = store.load(root, a.slug)
    _save_and_render(root, opp)
    ok(f"{a.slug} restored from {src.name} — status {opp.status}")
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
    opps, broken = store.load_all_with_errors(root)
    if broken:
        err(f"{len(broken)} record(s) unreadable and NOT listed: "
            + ", ".join(s for s, _ in broken))
        dim("  `mg check` explains; `mg restore <slug>` recovers.\n")
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
    changed = ai.ingest(opp, a.task, data, replace=a.replace)
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
        clashes = gov.contradictions(opp)
        if clashes:
            head("Same topic, different sources — resolve before solution design")
            for topic, items in clashes:
                print(f"  {c(topic, C.WARN)}")
                for it in items:
                    print(f"    {it}")
            dim("  Only one version can be carried into a proposal. Confirm which, "
                "or record the disagreement as an open question.")
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
    opps, broken = store.load_all_with_errors(root)
    problems = len(broken)
    head("Governance check")
    if broken:
        err(f"{len(broken)} record(s) cannot be read:")
        for slug, msg in broken:
            print(f"    {slug}: {msg}")
            if store.list_backups(root, slug):
                dim(f"      recoverable: mg restore {slug}")
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

    targets, _ = store.load_all_targets(root)
    if targets:
        g = metrics.growth_summary(targets, opps)
        head("Growth engine")
        for label, key, note in [
            ("Identified", "identified", ""),
            ("Researched", "researched", ""),
            ("Assessed", "assessed", f"{g['strong_fit']} strong fit"),
            ("Contacted", "contacted", f"{g['messages_sent']} message(s) sent"),
            ("Responded", "responded",
             f"{g['response_rate']}% of contacted" if g["response_rate"] is not None else ""),
            ("Positive", "positive",
             f"{g['positive_rate']}% of contacted" if g["positive_rate"] is not None else ""),
            ("Converted to leads", "converted",
             f"{g['conversion_rate']}% of contacted" if g["conversion_rate"] is not None else ""),
            ("Disqualified", "disqualified", ""),
        ]:
            print(f"  {label:<22}{c(str(g[key]), C.B):<14}{c(note, C.D)}")
        d = g["downstream"]
        head("Outbound → pipeline   " + c("(what the activity actually produced)", C.D))
        print(f"  {'Became qualified':<22}{d['qualified']}")
        print(f"  {'Reached discovery':<22}{d['discovery']}")
        print(f"  {'Reached proposal':<22}{d['proposed']}")
        print(f"  {'Won':<22}{d['won']}")
        if g["by_channel"]:
            head("By channel   " + c("(D-026 priority order — this is the performance evidence)", C.D))
            print(f"  {'channel':<22}{'sent':>6}{'resp':>6}{'pos':>6}{'conv':>6}")
            for ch, r in sorted(g["by_channel"].items(), key=lambda kv: -kv[1]["sent"]):
                print(f"  {ch[:20]:<22}{r['sent']:>6}{r['responded']:>6}"
                      f"{r['positive']:>6}{r['converted']:>6}")
        if len(g["by_campaign"]) > 1 or "uncategorised" not in g["by_campaign"]:
            head("By campaign")
            print(f"  {'campaign':<22}{'targets':>8}{'contacted':>10}{'pos':>6}{'conv':>6}")
            for k, r in sorted(g["by_campaign"].items(), key=lambda kv: -kv[1]["targets"]):
                print(f"  {k[:20]:<22}{r['targets']:>8}{r['contacted']:>10}"
                      f"{r['positive']:>6}{r['converted']:>6}")
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
    n.add_argument("--force", action="store_true", help="replace an existing record")
    n.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    n.add_argument("--duplicate-ok", dest="duplicate_ok", action="store_true",
                   help="create even though a similar opportunity exists")
    n.set_defaults(fn=cmd_new)

    it = sub.add_parser("intake", help="capture a lead from a form, email or note")
    it.add_argument("--from", dest="from_file", help="file with the enquiry; default stdin")
    it.add_argument("--channel", default="manual",
                    help="how it arrived: form, email, phone, referral, manual")
    it.add_argument("--company", help="override or supply the company name")
    it.add_argument("--source", help="override the recorded source (evidence for Q-008)")
    it.add_argument("--slug"); it.add_argument("--force", action="store_true")
    it.add_argument("--yes", action="store_true")
    it.add_argument("--duplicate-ok", dest="duplicate_ok", action="store_true",
                    help="capture even though a similar opportunity exists")
    it.set_defaults(fn=cmd_intake)

    hd = sub.add_parser("hold", help="pause or resume an opportunity")
    hd.add_argument("slug")
    hd.add_argument("--reason"); hd.add_argument("--revisit", help="date to resurface it")
    hd.add_argument("--owner")
    hd.add_argument("--release", action="store_true")
    hd.set_defaults(fn=cmd_hold)

    nx = sub.add_parser("next", help="every open opportunity: stage, last, next, owner, gaps")
    nx.set_defaults(fn=cmd_next)

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
    k.add_argument("--first-review", dest="first_review",
                   help="date of the first delivery checkpoint")
    k.add_argument("--force", action="store_true")
    k.set_defaults(fn=cmd_kickoff)

    dr = sub.add_parser("drop", help="remove a finding or requirement from a record")
    dr.add_argument("slug")
    dr.add_argument("--finding", action="append", metavar="REF")
    dr.add_argument("--requirement", action="append", metavar="REF")
    dr.add_argument("--yes", action="store_true")
    dr.set_defaults(fn=cmd_drop)

    rs = sub.add_parser("restore", help="recover an earlier version of a record")
    rs.add_argument("slug")
    rs.add_argument("--version", type=int, default=0, help="0 = most recent archived")
    rs.add_argument("--list", action="store_true", help="show archived versions")
    rs.add_argument("--yes", action="store_true")
    rs.set_defaults(fn=cmd_restore)

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
    ig.add_argument("--replace", action="store_true",
                    help="discard what is already recorded instead of merging into it")
    ig.set_defaults(fn=cmd_ingest)

    # ---- growth engine: mg target <verb> ----
    from . import growth as _gr, growth_cli as _gc
    tg = sub.add_parser("target", help="the growth engine: identify, research, reach out")
    tsub = tg.add_subparsers(dest="target_cmd", required=True)

    ta = tsub.add_parser("add", help="identify a target company")
    ta.add_argument("--company", required=True)
    ta.add_argument("--slug"); ta.add_argument("--via", help="how it was found — Q-008 evidence")
    ta.add_argument("--campaign"); ta.add_argument("--website"); ta.add_argument("--industry")
    ta.add_argument("--size"); ta.add_argument("--location")
    ta.add_argument("--contact"); ta.add_argument("--role"); ta.add_argument("--email")
    ta.add_argument("--force", action="store_true")
    ta.add_argument("--duplicate-ok", dest="duplicate_ok", action="store_true")
    ta.set_defaults(fn=_gc.cmd_add)

    tb = tsub.add_parser("brief", help="AI packet for a growth task")
    tb.add_argument("slug")
    tb.add_argument("task", choices=["target-research", "target-assess", "target-message"])
    tb.set_defaults(fn=_gc.cmd_brief)

    ti = tsub.add_parser("ingest", help="merge growth AI output")
    ti.add_argument("slug")
    ti.add_argument("task", choices=["target-research", "target-assess", "target-message"])
    ti.add_argument("--from", dest="from_file")
    ti.add_argument("--replace", action="store_true")
    ti.set_defaults(fn=_gc.cmd_ingest)

    td = tsub.add_parser("research", help="show how to research this target")
    td.add_argument("slug")
    td.set_defaults(fn=lambda r, a: _gc.cmd_brief(r, type("A", (), {"slug": a.slug, "task": "target-research"})()))

    tas = tsub.add_parser("assess", help="show how to assess fit")
    tas.add_argument("slug")
    tas.set_defaults(fn=lambda r, a: _gc.cmd_brief(r, type("A", (), {"slug": a.slug, "task": "target-assess"})()))

    tdr = tsub.add_parser("draft", help="begin an outreach draft")
    tdr.add_argument("slug"); tdr.add_argument("--force", action="store_true")
    tdr.set_defaults(fn=_gc.cmd_draft)

    tc = tsub.add_parser("compose", help="record a message you wrote yourself")
    tc.add_argument("slug"); tc.add_argument("--purpose"); tc.add_argument("--channel")
    tc.add_argument("--body"); tc.add_argument("--body-file", dest="body_file")
    tc.add_argument("--grounded-in", dest="grounded_in", action="append", metavar="REF")
    tc.add_argument("--force", action="store_true")
    tc.set_defaults(fn=_gc.cmd_compose)

    tap = tsub.add_parser("approve", help="founder approval before sending")
    tap.add_argument("slug"); tap.add_argument("--approved-by", dest="approved_by")
    tap.add_argument("--channel"); tap.add_argument("--yes", action="store_true")
    tap.add_argument("--force", action="store_true")
    tap.set_defaults(fn=_gc.cmd_approve)

    ts = tsub.add_parser("sent", help="record that you sent it")
    ts.add_argument("slug"); ts.add_argument("--channel"); ts.add_argument("--on")
    ts.add_argument("--follow-up", dest="follow_up")
    ts.set_defaults(fn=_gc.cmd_sent)

    tr = tsub.add_parser("respond", help="record a response")
    tr.add_argument("slug")
    tr.add_argument("--kind", required=True,
                    choices=["positive", "neutral", "negative", "none"])
    tr.add_argument("--text"); tr.add_argument("--on")
    tr.set_defaults(fn=_gc.cmd_respond)

    tm = tsub.add_parser("monitor", help="park a target with a reason")
    tm.add_argument("slug"); tm.add_argument("--reason"); tm.add_argument("--revisit")
    tm.set_defaults(fn=_gc.cmd_monitor)

    tdq = tsub.add_parser("disqualify", help="disqualify with reasoning")
    tdq.add_argument("slug"); tdq.add_argument("--reason")
    tdq.set_defaults(fn=_gc.cmd_disqualify)

    tcv = tsub.add_parser("convert", help="turn an engaged target into a lead")
    tcv.add_argument("slug"); tcv.add_argument("--to", help="clients/<slug> to create")
    tcv.add_argument("--force", action="store_true")
    tcv.set_defaults(fn=_gc.cmd_convert)

    tl = tsub.add_parser("list", help="the target pipeline")
    tl.add_argument("--all", action="store_true")
    tl.set_defaults(fn=_gc.cmd_list)

    tsh = tsub.add_parser("show", help="one target in full")
    tsh.add_argument("slug")
    tsh.set_defaults(fn=_gc.cmd_show)

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
        try:
            root = gov.repo_root(Path(__file__).resolve())
        except RuntimeError as e:
            err(str(e)); return 2
    try:
        return args.fn(root, args)
    except (m.StageError, m.ApprovalRequired, m.OpenValueError, store.RecordError) as e:
        err(str(e))
        return 1
    except ValueError as e:
        # Raised by model.as_bool when an AI hands back an ambiguous boolean.
        err(str(e))
        return 1
    except FileNotFoundError as e:
        path = getattr(e, "filename", None)
        err(f"File not found: {path}" if path else str(e))
        return 1
    except PermissionError as e:
        err(f"Permission denied: {getattr(e, 'filename', e)}")
        return 1
    except OSError as e:
        err(f"Filesystem error: {e}")
        dim("  No record was written. Re-run once the cause is resolved.")
        return 1
    except KeyboardInterrupt:
        print()
        err("Interrupted. Records are written atomically, so nothing is half-saved.")
        return 130
    except Exception as e:                      # noqa: BLE001 — last resort
        err(f"Unexpected {type(e).__name__}: {e}")
        dim("  The record on disk was not modified unless a success line printed above.")
        dim("  `mg check` reports any record left unreadable; `mg restore <slug>` recovers one.")
        return 1
