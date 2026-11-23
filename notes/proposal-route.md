# The proposal route (Sam, 15 Nov): build brief

## Where things stand (the ONE handover)
- **Rules that bite next:** CLAUDE.md "Rules are permanent" (wording to Sam first, his numbers), the proposal route (now fail closed), 30 (a repeat names the check that missed).
- **Done (chain A chat 2, Opus high, 23 Nov, session_01U3pKQxaqn1gLmoGR6959hb):** lesson 7 step 2 framework and step 3 (my part); all in rule-needs-check.md "Built". 103 rules in source/rule_proofs.json: 34 proven, 10 partly, 5 judge, 26 next, 2 owed, 26 cannot yet. Gate on new rules (handover STOP; watcher RULES line). Rule 74 now asks every shot (proof: GTA note G4-16). Let-throughs block handover and finish.py until settled; a crashed handover check is a STOP.
- **Next:** chain A chat 3, Opus high: step 2 worst first: rule 17 on Sam's v7 stills (find their times first; plan in its entry), 41's misses, 49 (M4), 13 (M6), 11 (M5), 89 (send gate), 30 (dearest_things_named red: GTA gun note no longer flagged); rule 19 once the could-not-test chat lands. Then, as the LAST chat of chain A: Sam's report page (rule-needs-check.md "For the report", measured against rule-table.md) with, in the same message, the CLAUDE.md wording (rule-needs-check.md "Wording for Sam") and the cannot-yet list (`ruleproofs.py sam`) as numbered questions.
- **Needs Sam:** nothing yet (the wording and the cannot-yet list go with the report, one message).
- **Read:** this section; rule-needs-check.md "Built"; guides/job-packs.md "A tool job"; ruleproofs.py MAP.
- **Open rule requests:** the CLAUDE.md line "No rule without a working check" (wording ready, not written).
- **For Claude:** chain B's let-through (chat 9c3f62f3, 03:34, staging-stills stale verdict) now refuses every finish.py run until settled (`propose.py settle 9c3f62f3 ...`). Kittests at end: all pass but claude_md_sentences_never_lost ("Every stage aims at three things" moved; not this job's); rule 30's dearest_things_named fixed (the repeat finder reads archived notes). End check named: SENTENCE x3 and COST as chat 1 (not this job's; no estimate for a system job). Could-not-test build chat session_01U3pKQzaw3rkdJXunde285d had pushed nothing by 23 Nov morning; it builds the COULD NOT TEST stop in pre-flight, render, finish.py. Branches claude/gta-chat31, claude/dreamy-fermi-vkhutz: GTA's, left alone.

## Learn step brief (Sam, 15 Nov: "We are aiming to cut the cost of every stage of production as greatly as possible
without harming quality"; read-only, changes nothing outside notes/proposals/learn/)
Protest Tiers, from notes/ledger/protest-tiers.json (stage spend vs plan, % of a week): plan + unplanned extras 10.1
(0.7 planned), cast 6.0 (2.1), sets 4.7 (3.7), moves 11.3 (3.1), animatic 1 2.1 (1.4), round 1: cast 3.7, sets 1.3,
moves 14.0 (4.5). Total 53.2 of ~20 planned, 33 chats at 0.2-3.2% each. Moves (both passes) 25.3, nearly half.
Prior work to reuse, not redo: notes/cost-diagnosis.md (Job A/B: re-reading history ~49% of an Opus chat; chats
over 200k cost most; rework of returned faults), notes/budget-job.md (Remakes).
- **A (guard-holes Learn):** every decision put to Sam (Y/N, numbered choice, "Need", "Decide") in the Protest
  Tiers and Blessed chats: list_events kinds ["result"] (the turn's final reply), never a whole chat's every kind;
  then notes/, notes/archive/, notes/morning-report.md where no reply exists. One line each with chat and source, in
  notes/proposals/learn/asks.md. Then ONE fresh blind helper labels each "change" (rules, tools, checks, kits, how
  films are built, anything that outlives this film) or "routine", one-line reason; split by a fixed seed into a
  tuning half and a test half. Say the count of change asks (under 30 in the test half: say so).
- **B (cost by cause):** for each Protest Tiers chat (sid in the ledger json): get_session usage (cache read/write,
  output, history at end; no event paging), its stage, and from its result events: the round's notes, repeats,
  renders. Table in notes/proposals/learn/protest-tiers-costs.md: chat, stage, % of a week, history at end, and for
  moves and plan stages the cause per chat (rework of a returned fault, re-render, critique helpers, code finding,
  start-up reading, bookkeeping), "unchecked" where the record does not show it. Also: which of the 13 Nov
  cost-diagnosis fixes were in force and whether that stage's cost fell.
- **Stop:** at 3% of a week, or done; commit, push, hand over to chat 3 (Opus high) via create_session.

## The rule as first sent to Sam (15 Nov, chat 6; superseded by the install-route verdict's wording)
"Every change goes to helpers before it comes to me (Sam, 15 Nov; takes in 'search before suggesting', 12 Nov). Any change to rules, tools, checks, kits or how the films are built, however small (not animatics, renders, clips or film notes): first the problem and the facts are written down with no answer, after searching the rulebook and kit list for the closest rule or tool; two fresh helpers, from fixed prompts nobody edits, each write their own answer without seeing Claude's; a fresh judge scores all three blind (quality, fewer notes and faults, cost against 15% of a week, risk, can it be undone), asks my eight questions of each, and picks one. I see the top two in plain English with Lost/Added lines and 'Critiqued: N found, N fixed, N named'. A guard refuses any message asking me to approve a change without the judge's verdict. No trials: when I call a film complete, every change since the last film is checked against its results, and any that needs changing goes through this again."

## Replay run 2 scores (15 Nov, chat 5; one line per case)
1. PASS: number of chats is the lever (32 chats, 1.6% each); measure every chat's cause across the film first.
2. MISS: covers kinds of work, but adds two older films and picks the dearest chats (Sam: this film, a spread, not extremes).
3. PASS: root cause "tools reach a chat only as text"; counts use, tests whether page.py lands, enforced by refusal, numbers.
4. PASS: results first, trace to the rule that should have caught it, self-filling ledger row, 3-5% of a week.
5. PASS: read-only learning step apart; one change per Y, each with its evidence and number to beat.

## The problem (evidence from this chat, 15 Nov)
Claude's proposals are a first plausible idea, sized small and cheap, anchored on that idea; they only got better
when Sam pushed. Sam cannot code and cannot be the system's critic. In one chat Sam pushed five times, each giving a
better answer (these are the replay cases):
1. Code-finding fix proposed (looking at code is ~30% of a chat's steps). Push: "Is this what you would suggest as an
   AI efficiency expert?" -> Better: the fix is modest; the number of chats, start-up reading and bookkeeping (~30% of
   chat 31) are bigger levers; measure across the film before tuning one chat.
2. Bill check of the cheapest and dearest chat proposed. Push: "What would get us the best result? ... or just this
   film" -> Better: this film (newest tools), a spread across every kind of work, not extremes.
3. A "pillar" rule (fixes aim for the biggest result). Push: "Critique that rule and make sure it will
   comprehensively deliver" -> 8 faults: vague "thorough", no root cause, "used" is not "worked", no numeric target,
   a lesser option invites half-fixes, unchecked claims told to Sam, only after failures, no enforcement.
   Further: naming a tool in a pack already failed (`guides/job-packs.md` notes round names `page.py`; chats 29 and
   31 ran it 0 times, and searched code by hand 25 and 26 times).
4. A full audit of all ~64 rules and ~115 tools (8-12% of a week). Push: "Is this the most intelligent thing to do
   and the best way to adhere to statement 1?" -> Better: results first (the film's cost by stage and Sam's notes,
   catchable vs taste), trace only those to the rules/tools that should have stopped them, and make measuring
   automatic at every handover (free, from the chat's own record); ~3-5%.
5. Push: "Saying yes to anything now carries huge risk" -> Better: split learning (read-only, safe) from changing
   (one change at a time, with evidence and a number to beat).
Also: Claude told Sam "the tools weren't used" before checking (it was true, but unchecked).

## The route (Sam's Y; step 6 is Sam's own wording)
Scope by KIND, never by the chat's own cost estimate: any change to rules, tools, checks, kits or how films are built
(not animatics, renders, clips or film notes).
1. The chat writes the problem and the raw facts, NO solution, to `notes/proposals/NAME.md`.
2. Two fresh helpers, each from a fixed prompt file the chat does not edit, each given only the problem file and the
   paths to the raw record (never the chat's idea), write their own approach.
3. A third fresh helper, the judge (fixed prompt file), scores every version, the chat's included, on a fixed list:
   high quality, fewer notes and faults, cost against 15% of a week, risk, can it be undone; answers the Sam test
   (Sam's pushes above, word for word, 8 questions at most, merged not added); picks one; writes its verdict into the
   proposal file, word for word, with the file's hash.
4. Enforced where the work happens: a Stop hook blocks any reply that asks Sam to approve a change while
   `notes/proposals/` holds no matching verdict for it. Detect by the proposal file (written this turn, or named in
   the reply), not by wording alone. Must honour `stop_hook_active` (no endless loop) and never block routine Y/N
   questions (animatic, final render).
5. Sam sees the top two options in plain English, with Lost/Added lines, and "Critiqued: N found, N fixed, N named"
   counted from the file.
6. **No trials, nothing temporary (Sam, 15 Nov).** When Sam declares a film complete, Claude reviews every change made
   since the last film against that film's results (Sam's notes, faults he caught, cost from the ledger). Any change
   that needs changing goes through steps 1-5.
Measure (automatic, in the end-of-film review): how often a proposal is later replaced, notes and cost per film.
Not "how often Sam pushes" alone (it falls if Sam tires).

## Replay test (it must pass before the route is switched on)
For each of the five cases, write only the problem and facts as they stood BEFORE Sam's push, run steps 1-3, and
compare the judge's pick with the "Better" answer above. Pass: the route reaches the better answer (or one the judge
shows is better still) in at least 4 of 5 without Sam's push. Report each case to Sam in one plain line. On a fail,
find why (rule 30), fix the prompts, rerun once; then report either way.

## Build notes
- **Kittest fixes (15 Nov, chat 2; rule 30, why):** (a) `record` wrote `open(f,'w').write(problem_text(name)...)`:
  Python opens (truncates) the file before reading it, so every recorded proposal lost its problem and read as stale.
  Fixed by reading first. (b) `verdict_ok` hashed the raw verdict, not the copy in NAME.md, so an edit below the
  verdict went unseen; it now checks the copy is word for word. kittest `proposal_route_hook` passes.
- Reuse: rule 89's critic helper (`.claude/agents/critic.md`, `source/critique.py`) for how helpers are started
  and their reports saved; handover.py's .jsonl reading; the Stop hook list in `.claude/settings.json`.
- Kittests for the hook (blocks a change proposal without a verdict, passes one with it, passes a routine animatic
  Y/N, honours stop_hook_active). Catalogue row. MAP at the top of any new file.
- After it is on, the next jobs go through it: the paused code-tool job, the results-first review of Protest Tiers,
  the automatic per-chat measuring. Sam: "the entire system could benefit".
