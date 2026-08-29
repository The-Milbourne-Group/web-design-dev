#!/usr/bin/env bash
# End-to-end test of the commercial pipeline.
#
# Drives one realistic opportunity from lead to Active delivery, plus a lost
# deal and a disqualified lead, asserting the governance guards fire where the
# operating system says they must. Creates `zz-e2e-*` opportunities and removes
# them at the end, so it never leaves fixture data in clients/.
#
#   tools/e2e.sh            run and clean up
#   tools/e2e.sh --keep     leave the records in place for inspection
set -uo pipefail
cd "$(dirname "$0")/.."
MG=./mg
KEEP=${1:-}
PASS=0; FAIL=0
SCRATCH=$(mktemp -d)
trap 'rm -rf "$SCRATCH"; [ "$KEEP" = "--keep" ] || rm -rf clients/zz-e2e-* growth/zz-e2e-*' EXIT

ok()   { PASS=$((PASS+1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf '  \033[31m✗\033[0m %s\n' "$1"; }
step() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# expect_fail "label" cmd...   — the command MUST exit non-zero
expect_fail() { local l="$1"; shift; if "$@" >/dev/null 2>&1; then bad "$l (expected refusal, was allowed)"; else ok "$l"; fi; }
expect_ok()   { local l="$1"; shift; if "$@" >/dev/null 2>&1; then ok "$l"; else bad "$l"; "$@" 2>&1 | sed 's/^/      /'; fi; }
expect_status(){ local s; s=$(python3 -c "
import sys,json;print(json.load(open('clients/$1/opportunity.json'))['status'])"); \
  [ "$s" = "$2" ] && ok "status is $2" || bad "status is $s, expected $2"; }

rm -rf clients/zz-e2e-* growth/zz-e2e-*

step "1 · Lead intake from a real channel"
cat > "$SCRATCH/enquiry.txt" <<'MAIL'
From: Dan W <dan@zz-e2e-joinery.example>
Subject: Website enquiry
Company: ZZ E2E Joinery
Phone: 01752 887 431
How did you hear about us: Referred by an architect

We are pitching for commercial fit-out contracts and our website makes us look
like a two-man operation. We want to win more of the tenders we are shortlisted
for. Can we talk?

Kind regards
Dan
MAIL
expect_ok "email enquiry captured" $MG intake --from "$SCRATCH/enquiry.txt" \
  --channel email --slug zz-e2e-main
expect_status zz-e2e-main Prospect
python3 -c "
import json;o=json.load(open('clients/zz-e2e-main/opportunity.json'))
assert o['company']['name']=='ZZ E2E Joinery', o['company']['name']
assert o['contacts'][0]['name']=='Dan W', o['contacts'][0]
assert o['contacts'][0]['email']=='dan@zz-e2e-joinery.example'
assert 'architect' in o['qualification']['source']
assert 'two-man operation' in o['qualification']['problem']
assert any(e['kind']=='enquiry' for e in o['events']), 'raw enquiry not retained'
" && ok "company, contact, email, source and problem parsed; raw enquiry retained" \
  || bad "intake parsing lost information"
expect_ok "form enquiry captured" bash -c "echo '{\"company\":\"ZZ E2E Form Co\",\"your name\":\"A Tester\",\"email\":\"a@zz-e2e-form.example\",\"message\":\"Site is dated\",\"how did you hear\":\"Google\"}' | $MG intake --channel form --slug zz-e2e-form"
$MG set zz-e2e-main --industry "Joinery" --size "~28 staff" \
  --desired-outcome "Win more commercial tenders" >/dev/null 2>&1

step "2 · Qualification refuses incomplete evidence"
expect_fail "blocked: missing authority, ICP signals, feasibility, stage" \
  $MG qualify zz-e2e-main --outcome Qualified --approved-by Founder
expect_ok "evidence recorded" $MG set zz-e2e-main --authority --decision-maker \
  --contact "Dan W" --role "Managing Director" \
  --fit-signal "Have proven they can sell and operate successfully" \
  --signal "Website fails to establish credibility or communicate value" \
  --stage Entry --feasible
cat > "$SCRATCH/q.json" <<'JSON'
{"confirmed_facts":["Stated in the enquiry: pitching for commercial fit-out contracts"],
 "assessment":"Reads as Entry stage, but the enquiry does not establish budget authority.",
 "missing_information":["Who controls budget"],
 "recommended_outcome":"Clarification required",
 "recommended_next_action":"Call to establish decision authority"}
JSON
expect_ok "qualification analysis ingested" $MG ingest zz-e2e-main qualify --from "$SCRATCH/q.json"
python3 -c "
import json;q=json.load(open('clients/zz-e2e-main/opportunity.json'))
assert q['qualification']['recommended_outcome']=='Clarification required'
assert q['qualification']['outcome']=='', 'agent recommendation was applied as a decision'
assert q['status']=='Prospect', q['status']
assert q['qualification']['confirmed_facts'] and q['qualification']['assessment']
" && ok "facts and assessment separate; recommendation recorded, not applied" \
  || bad "agent recommendation leaked into the decision"
expect_fail "blocked: no founder approval" $MG qualify zz-e2e-main --outcome Qualified
expect_ok "founder qualifies" $MG qualify zz-e2e-main --outcome Qualified \
  --approved-by Founder --reasoning "Strong problem fit; decision-maker confirmed."
expect_status zz-e2e-main Qualified

step "3 · Discovery, with mandatory playback"
expect_ok "discovery held" $MG discovery zz-e2e-main --held-on 2026-09-03 --attendee "Dan W"
cat > "$SCRATCH/d.json" <<'JSON'
{"findings":[
 {"ref":"D1","topic":"Current state","statement":"Site built 2016, nobody can edit it","confirmed":true,"source":"Dan W"},
 {"ref":"D2","topic":"Trigger","statement":"Lost 3 of 4 shortlisted tenders; website cited in debriefs","confirmed":true,"source":"Dan W"},
 {"ref":"D3","topic":"Inference","statement":"Unpublished project photography is likely the highest-value asset","confirmed":false,"source":"Inferred from D1/D2"}],
 "objectives":["Win more shortlisted tenders"],
 "problems":["Website undermines credibility at the tender verification step"],
 "constraints":["Half a day per week of client content capacity"],
 "risks":["Content capacity is the critical path"],
 "unknowns":["Who controls the domain"],
 "assumptions":["Q1 means January"],
 "success_indicators":[{"indicator":"Shortlist-to-win rate","data_source":"Client tender log"}],
 "stakeholders":[{"name":"Dan W","role":"MD","influence":"Decides"}]}
JSON
expect_ok "analysis ingested" $MG ingest zz-e2e-main discovery-analysis --from "$SCRATCH/d.json"
python3 -c "
import json;d=json.load(open('clients/zz-e2e-main/opportunity.json'))['discovery']['findings']
c=sum(1 for f in d if f['confirmed']);i=len(d)-c
assert c==2 and i==1, (c,i)
" && ok "facts and inferences held separate (2 confirmed, 1 inferred)" \
  || bad "fact/assumption separation lost"
expect_fail "blocked: solution design before playback" $MG solution zz-e2e-main --restate "x"
expect_ok "playback confirmed" $MG discovery zz-e2e-main --playback 2026-09-05

step "4 · Solution design refuses unsourced scope"
cat > "$SCRATCH/bad.json" <<'JSON'
{"problem_restatement":"Website misrepresents the firm at tender stage",
 "requirements":[{"ref":"R1","statement":"Case study library","source":"D2","kind":"Confirmed","capability":"website-development","in_scope":true},
                 {"ref":"R9","statement":"Client login portal","source":"","kind":"Confirmed","in_scope":true}],
 "stage":"Entry","feasibility":"Within capability"}
JSON
$MG ingest zz-e2e-main solution --from "$SCRATCH/bad.json" >/dev/null 2>&1
expect_fail "blocked: requirement R9 has no source" $MG solution zz-e2e-main --approved-by Founder
expect_ok "bad requirement removed" $MG drop zz-e2e-main --requirement R9 --yes
cat > "$SCRATCH/sol.json" <<'JSON'
{"problem_restatement":"Website misrepresents the firm at the tender verification step",
 "requirements":[
  {"ref":"R1","statement":"Commercial case study library from existing photography","source":"D2","kind":"Confirmed","capability":"website-development","in_scope":true},
  {"ref":"R2","statement":"CMS so the client can publish without a third party","source":"D1","kind":"Confirmed","capability":"website-development","in_scope":true},
  {"ref":"R3","statement":"Enquiry measurement baseline","source":"Assumption — inferred from D3","kind":"Assumed","capability":"optimization-and-support","in_scope":true},
  {"ref":"R4","statement":"Tender document templating","source":"D2","kind":"Confirmed","in_scope":false,"deferred_reason":"Expansion candidate; not the credibility problem"}],
 "stage":"Entry","feasibility":"Within capability; client content capacity is the constraint",
 "open_dependencies":["Q-009 — no approved stack, CMS is a per-project decision"]}
JSON
expect_ok "sourced solution ingested" $MG ingest zz-e2e-main solution --from "$SCRATCH/sol.json"
expect_ok "founder approves solution" $MG solution zz-e2e-main --verified --approved-by Founder
expect_status zz-e2e-main Proposal

step "5 · Proposal issuance gate"
expect_fail "blocked: Q-007 and Q-011 open" $MG propose zz-e2e-main --approved-by Founder
expect_fail "blocked: price with the gate uncleared" \
  $MG gate zz-e2e-main --terms "Phase one at £18,500" --approved-by Founder
expect_ok "founder decides terms for this engagement" $MG gate zz-e2e-main \
  --terms-decided --deliverables-defined --approved-by Founder \
  --terms "Fixed fee for the scope in §2, invoiced in three stages." \
  --note "This engagement only; Q-007 remains open company-wide."
expect_fail "blocked: issuance without founder approval" $MG propose zz-e2e-main
expect_ok "proposal issued" $MG propose zz-e2e-main --approved-by Founder \
  --valid-until 2026-10-15 --follow-up-due 2026-09-15

step "6 · Follow-up and close"
expect_ok "follow-up completed" $MG followup zz-e2e-main --done "Confirm receipt" --note "Dan confirmed"
expect_ok "next action scheduled" $MG followup zz-e2e-main \
  --action "Confirm decision" --owner Founder --due 2026-09-22
expect_ok "proposal accepted" $MG outcome zz-e2e-main --outcome Accepted --reasoning "Agreement signed"
expect_status zz-e2e-main Onboarding

step "7 · Project initialization carries the record forward"
expect_fail "blocked: kickoff before acceptance criteria" $MG kickoff zz-e2e-main --approved-by Founder
expect_ok "project initialized" $MG init-project zz-e2e-main \
  --acceptance "Case studies published and findable" \
  --acceptance "Client publishes unaided" \
  --approver "Design=Dan W" --approver "Launch=Dan W" \
  --access "Domain registrar=client's own account" \
  --dependency "Client: case study approvals"
python3 -c "
import json;o=json.load(open('clients/zz-e2e-main/opportunity.json'))
reqs=[r for r in o['solution']['requirements'] if r['in_scope']]
b=open('clients/zz-e2e-main/PROJECT_BRIEF.md').read()
missing=[r['ref'] for r in reqs if r['ref'] not in b]
assert not missing, missing
assert o['discovery']['risks'][0][:20] in b, 'risks not carried'
assert o['discovery']['assumptions'][0][:15] in b, 'assumptions not carried'
assert 'Tender document templating' in b, 'exclusions not carried'
" && ok "scope, risks, assumptions and exclusions carried without re-entry" \
  || bad "data continuity broken between sales and project"
expect_ok "kickoff held" $MG kickoff zz-e2e-main --approved-by Founder
expect_status zz-e2e-main Active
python3 -c "
import json;o=json.load(open('clients/zz-e2e-main/opportunity.json'))
b=open('clients/zz-e2e-main/PROJECT_BRIEF.md').read()
q=o['qualification']
assert q['assessment'][:40] not in b, 'internal assessment transferred to the project'
assert 'Clarification required' not in b, 'agent recommendation transferred'
assert q['outcome_reasoning'][:25] not in b, 'internal decision reasoning transferred'
assert 'highest-value asset' not in b, 'unconfirmed inference transferred as fact'
scope=b.split('### In scope')[1].split('### Explicitly out of scope')[0]
assert '\`R3\`' in scope and '(assumed)' in scope, 'assumed requirement lost its label'
" && ok "internal reasoning and inferences withheld; scope and labels transferred" \
  || bad "project initialization transferred information it should not"

step "8 · Hold and release"
expect_fail "blocked: hold with no reason" $MG hold zz-e2e-form
expect_ok "placed on hold" $MG hold zz-e2e-form --reason "Contact on leave" --revisit 2026-12-01
python3 -c "
import sys;sys.path.insert(0,'tools')
from mg import store, governance as g
from pathlib import Path
root=g.repo_root(Path('tools/mg/governance.py').resolve())
o=store.load(root,'zz-e2e-form')
assert o.hold.on_hold and o.pipeline_stage()=='ON HOLD', o.pipeline_stage()
assert o.status=='Prospect', 'hold must not overwrite the authoritative status'
assert o.next_follow_up(), 'hold with a revisit date must schedule a follow-up'
" && ok "ON HOLD is derived; status preserved; revisit scheduled" || bad "hold model wrong"
expect_ok "released from hold" $MG hold zz-e2e-form --release

step "9 · A lost deal must record why"
$MG new --company "ZZ E2E Lost" --slug zz-e2e-lost --source "Cold outreach" \
  --contact "R Patel" --problem "Site is dated" --outcome-wanted "More enquiries" >/dev/null 2>&1
$MG set zz-e2e-lost --authority --decision-maker --contact "R Patel" \
  --fit-signal "Have a meaningful business objective" \
  --signal "Outdated digital presence relative to the business's actual standing" \
  --stage Entry --feasible >/dev/null 2>&1
$MG qualify zz-e2e-lost --outcome Qualified --approved-by Founder --reasoning "Fit" >/dev/null 2>&1
$MG discovery zz-e2e-lost --held-on 2026-09-04 --playback 2026-09-06 >/dev/null 2>&1
echo '{"problem_restatement":"Dated site","requirements":[{"ref":"R1","statement":"Rebuild","source":"client statement","kind":"Confirmed","capability":"website-development","in_scope":true}],"stage":"Entry","feasibility":"ok"}' > "$SCRATCH/s2.json"
$MG ingest zz-e2e-lost solution --from "$SCRATCH/s2.json" >/dev/null 2>&1
$MG solution zz-e2e-lost --verified --approved-by Founder >/dev/null 2>&1
$MG gate zz-e2e-lost --terms-decided --deliverables-defined --approved-by Founder >/dev/null 2>&1
$MG propose zz-e2e-lost --approved-by Founder >/dev/null 2>&1
expect_fail "blocked: decline with no loss reasoning" $MG outcome zz-e2e-lost --outcome Declined
expect_ok "decline with reasoning" $MG outcome zz-e2e-lost --outcome Declined \
  --loss-reason "price — went with a cheaper supplier; off-strategy per D-007" \
  --reasoning "Chose lowest bid"
expect_status zz-e2e-lost Lost

step "10 · Disqualification keeps its evidence"
$MG new --company "ZZ E2E Disqualified" --slug zz-e2e-dq --source "Web form" \
  --contact "T Nolan" --problem "Wants unlimited changes for a flat fee" \
  --outcome-wanted "Cheapest option" >/dev/null 2>&1
expect_ok "disqualified with reasoning" $MG qualify zz-e2e-dq --outcome Disqualified \
  --approved-by Founder --reasoning "Shopping on price alone and expects unlimited work — two ICP.md §6 signals."
[ -f clients/zz-e2e-dq/QUALIFICATION.md ] && ok "directory retained as ICP evidence" \
  || bad "disqualified directory lost"

step "11 · Hardening: capability gate, merge safety, recovery"
cat > "$SCRATCH/oos.json" <<'JSON'
{"requirements":[{"ref":"R7","statement":"Native mobile app","source":"D1","kind":"Confirmed","capability":"mobile-apps","in_scope":true}]}
JSON
$MG ingest zz-e2e-lost solution --from "$SCRATCH/oos.json" >/dev/null 2>&1
expect_fail "blocked: capability not in SERVICES.md §3" \
  $MG solution zz-e2e-lost --approved-by Founder
expect_ok "out-of-scope requirement removed" $MG drop zz-e2e-lost --requirement R7 --yes
echo '{"findings":[{"ref":"DX","topic":"z","statement":"later finding","confirmed":true,"source":"client"}]}' > "$SCRATCH/m2.json"
$MG ingest zz-e2e-main discovery-analysis --from "$SCRATCH/m2.json" >/dev/null 2>&1
python3 -c "
import json;f=json.load(open('clients/zz-e2e-main/opportunity.json'))['discovery']['findings']
refs=[x['ref'] for x in f]
assert 'D1' in refs and 'DX' in refs, refs
" && ok "re-ingest merges; earlier findings survive" || bad "re-ingest destroyed prior findings"
echo '{"findings":[{"ref":"DY","statement":"x","confirmed":"maybe"}]}' > "$SCRATCH/amb.json"
expect_fail "blocked: ambiguous confirmed value" \
  $MG ingest zz-e2e-main discovery-analysis --from "$SCRATCH/amb.json"
expect_fail "blocked: duplicate company" bash -c \
  "$MG new --company 'ZZ E2E Joinery' --slug zz-e2e-dupe"
printf '{"slug": "zz-e2e-form", broken' > clients/zz-e2e-form/opportunity.json
# `mg check` exits non-zero when it finds issues, so capture then grep —
# piping under `set -o pipefail` would report the exit code, not the match.
CHECK_OUT=$($MG check 2>&1 || true)
grep -q "cannot be read" <<<"$CHECK_OUT" && ok "unreadable record surfaced by check" || bad "corrupt record hidden"
NEXT_OUT=$($MG next 2>&1 || true)
grep -q "unreadable" <<<"$NEXT_OUT" && ok "unreadable record surfaced by next" || bad "corrupt record silently omitted"
expect_ok "record recovered from history" $MG restore zz-e2e-form --yes
python3 -c "
import json;d=json.load(open('clients/zz-e2e-form/opportunity.json'))
assert d['company']['name']=='ZZ E2E Form Co', d['company']
" && ok "restored record is the real one" || bad "restore returned wrong content"

step "12 · Growth engine: target to lead"
rm -rf growth/zz-e2e-*
expect_ok "target identified" $MG target add --company "ZZ E2E Fabrication" \
  --slug zz-e2e-tgt --via "Targeted outbound" --campaign "zz-e2e" \
  --contact "R Tester" --role "Managing Director" --email "r@zz-e2e-fab.example"
expect_fail "blocked: duplicate target" $MG target add --company "ZZ E2E Fabrication" --slug zz-e2e-tgt2
cat > "$SCRATCH/res.json" <<'JSON'
{"research":[
 {"ref":"E1","statement":"Announced a second site","kind":"confirmed","source":"News page","observed_on":"2026-08-29"},
 {"ref":"E2","statement":"Website footer reads 2019","kind":"confirmed","source":"Their site","observed_on":"2026-08-29"},
 {"ref":"E3","statement":"Probably losing enquiries","kind":"inference","source":"Reasoned from E2"},
 {"ref":"E4","statement":"Whether they tender for frameworks","kind":"unknown","source":""}]}
JSON
expect_ok "research ingested" $MG target ingest zz-e2e-tgt target-research --from "$SCRATCH/res.json"
python3 -c "
import json;r=json.load(open('growth/zz-e2e-tgt/target.json'))['research']
k={x['ref']:x['kind'] for x in r}
assert k=={'E1':'confirmed','E2':'confirmed','E3':'inference','E4':'unknown'}, k
" && ok "evidence typed: confirmed / inference / unknown held apart" || bad "evidence typing lost"
cat > "$SCRATCH/badev.json" <<'JSON'
{"research":[{"ref":"E9","statement":"They use SAP","kind":"confirmed","source":""}]}
JSON
expect_fail "blocked: confirmed evidence with no source" \
  $MG target ingest zz-e2e-tgt target-research --from "$SCRATCH/badev.json"
cat > "$SCRATCH/ass.json" <<'JSON'
{"signals":[{"signal":"Digital infrastructure that has not kept pace with growth","kind":"problem","evidence_ref":"E1"}],
 "band":"Strong","reasoning":"Growing, site stopped in 2019.","recommended_action":"Initiate outreach"}
JSON
expect_ok "fit assessed" $MG target ingest zz-e2e-tgt target-assess --from "$SCRATCH/ass.json"
cat > "$SCRATCH/badmsg.json" <<'JSON'
{"purpose":"reach out","subject":"hi","body":"You are losing enquiries right now.","grounded_in":["E3"]}
JSON
$MG target ingest zz-e2e-tgt target-message --from "$SCRATCH/badmsg.json" >/dev/null 2>&1
expect_fail "blocked: draft resting on an inference" \
  $MG target approve zz-e2e-tgt --approved-by Founder --yes
cat > "$SCRATCH/msg.json" <<'JSON'
{"purpose":"Second site while the site reads 2019","subject":"Your expansion",
 "body":"I saw the second site announcement. Your website footer still reads 2019.",
 "grounded_in":["E1","E2"]}
JSON
expect_ok "grounded draft accepted" $MG target ingest zz-e2e-tgt target-message --from "$SCRATCH/msg.json"
expect_fail "blocked: approval without founder" $MG target approve zz-e2e-tgt --yes
expect_ok "founder approves" $MG target approve zz-e2e-tgt --approved-by Founder --channel email --yes
expect_fail "blocked: convert before any response" $MG target convert zz-e2e-tgt
expect_ok "recorded as sent" $MG target sent zz-e2e-tgt --channel email --on 2026-09-02
expect_fail "blocked: convert on no response yet" $MG target convert zz-e2e-tgt
expect_ok "positive response recorded" $MG target respond zz-e2e-tgt --kind positive --text "Worth a call."
expect_ok "converted to a lead" $MG target convert zz-e2e-tgt --to zz-e2e-converted
python3 -c "
import json
q=json.load(open('clients/zz-e2e-converted/opportunity.json'))['qualification']
facts=' '.join(q['confirmed_facts'])
assert 'second site' in facts and 'source:' in facts, facts
assert 'Probably losing enquiries' not in facts, 'inference crossed as a confirmed fact'
assert 'inference, not fact' in q['assessment'], q['assessment'][:80]
assert 'Targeted outbound' in q['source'], q['source']
assert q['fit']['problem_signals'], 'ICP signals not carried'
" && ok "confirmed facts carried with sources; inference carried as labelled assessment" \
  || bad "evidence boundary broken on conversion"
expect_fail "blocked: disqualify with no reasoning" $MG target disqualify zz-e2e-tgt2 --reason ""
$MG target add --company "ZZ E2E Cheap" --slug zz-e2e-dq --via "Warm network" >/dev/null 2>&1
expect_ok "target disqualified with reasoning" $MG target disqualify zz-e2e-dq \
  --reason "Shopping on price alone — ICP.md §6, off-strategy per D-007"
GM=$($MG metrics --json 2>/dev/null)
python3 -c "
import json,sys
sys.path.insert(0,'tools')
from pathlib import Path
from mg import store, metrics, governance as g
root=g.repo_root(Path('tools/mg/governance.py').resolve())
t,_=store.load_all_targets(root); o=store.load_all(root)
s=metrics.growth_summary(t,o)
assert s['contacted']>=1 and s['positive']>=1 and s['converted']>=1, s
assert s['by_channel'].get('email',{}).get('converted',0)>=1, s['by_channel']
" && ok "growth metrics attribute the conversion to its channel" || bad "growth attribution broken"

step "13 · Governance check, pipeline view and metrics"
expect_ok "governance check clean" $MG check
expect_ok "pipeline view renders" $MG next
$MG metrics --json > "$SCRATCH/m.json"
python3 -c "
import json;s=json.load(open('$SCRATCH/m.json'))
assert s['leads']>=4, s['leads']
assert s['won']>=1 and s['lost']>=2, s
assert s['close_rate'] is not None, 'proposal-to-close not computable'
assert s['avg_proposal_hours'] is not None, 'proposal build time not computable'
" && ok "pipeline metrics computable (close rate, proposal build time)" \
  || bad "metrics not computable"

printf '\n\033[1m%s\033[0m\n' "$PASS passed, $FAIL failed"
[ "$KEEP" = "--keep" ] && printf 'Records kept in clients/zz-e2e-*\n'
exit $((FAIL > 0))
