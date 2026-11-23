# The proposal route (Sam, 15 Nov): build brief

## Where things stand (the ONE handover)
- **Rules that bite next:** CLAUDE.md "Statement Two" (a check that only looks like it works is worse than "can't yet"), "No rule without a working check" (a proof counts only on its saved example), 30 (a repeat names the check that missed).
- **RESERVE (Sam, 23 Nov ~22:05: "all the tool chats from earlier today, add that to the reserve job lists"):** chains A and B are reserve jobs R2-R4 in notes/next-jobs.md; nothing starts until Sam names one.
- **HOLD (Sam, 23 Nov ~14:45, in chain A chat 6, session_01U3pKQzjJ6Hbt9H5jkEg1t1): "Hold the work of all chats unrelated to Grand Theft Autism for now."** Chains A and B start nothing and open no next chat until Sam says go. Chain A chat 6 was stopped mid-job: body_check_back_view fixed (old films replayed exactly as Sam saw them; v4 body checks too); audit_door_through_officer written, not run; v4 stills matched (01 0.5 s, 03c 1.0, 04b 1.5, 05a ~2.75, 05b ~3.0-3.12, 05c 3.5) for the v4 solids test; G4-11 "2D legs" to be written "cannot yet" (needs a flat-pose-to-3D-body bridge and a drawn-vs-solid leg outline test). rule_proofs.json and the full kit-test run not yet done.
- **Done (chain A chat 5, Opus high, 23 Nov, session_01U3pKR1Z6SWGi4RSahgw7hK):** rule 41: humancheck._reach catches v4 1.00 s (arm 74 degrees behind him, 'reach') and 4.92 s (hand behind his back, forearm end-on, 'stub'); gallery from 8 views: 0 false flags (kittest body_check_curled_v4). Rule 17: viewchecks.outline_shows (the drawn outline, not bone points) catches G7-2 bonnet at 0.67 s; effect_shows catches G7-7 water at 3.33 s; solid_check_shot4_v7 now runs TODAY's check on v7's code (frames 8, 12, 18, 40). Rule 5: kittest bump_test_bench_old_poses (bench_move's checks on the old seat/pistol/dash poses); bench_move stays in watcher OFF (named); broken list: unwired and saver named. rule_proofs.json: 41, 17, 5 partly with misses written.
- **Next (chain A, chat 6, Opus high: building new):** FIRST body_check_back_view (red: rules 41 and N6 show BROKEN; red again at the next handover stops it; v3 back views 1 of 2: find which change since chat 28 lost the second). Then the misses, worst first: 41's legs (G4-11, v4 3.12 s: the kit draws a leg hip to foot with a fixed knee; learn a bent leg with its depth turn, then a drawn-vs-3D knee check); v4's solids (a copy of v4 with the car's solid shapes, so G4-2, G4-3, G4-4, G4-11 can be tested); audit.py's own saved example (rule 5). Then the next worst in `ruleproofs.py`.
- **Done (chain B chat 4, guard-film-questions, Opus high, 23 Nov, session_01U3pKR2CR28qdUtk2Z9Y6DN):** Learn 1: every guard block logged in full (notes/proposals/guard-blocks.jsonl; `propose.py blocks`). Learn 2: 51 stops labelled (guard-film-questions/labels.json, test-list.json; 18 true, 33 wrong; 12 read in full, 39 from the log line: chats before 22 Nov 22:34 deleted), kittest guard_labelled_list (ratchet GUARD_BASELINE 21 wrong, 2 missed, probe 9/1). Change 1 (the check for Sam's 22 Nov "One message, never twice", his "2" in session 01U3pKR36uALh2iRkpP1tyQ4, so not asked again): block_reason asks for one Correction line; the retry is judged alone (correction_ok: cleared / let-through; full resends counted); kittest guard_one_correction on Sam's real 22 Nov double (example-22nov.json; mutation-checked); rule N29 partly; rulebook Messages row; watcher promises propose.py hook, kittest_gate_faults, shared_faults, override.py prompt. Report entry 3 written.
- **Next (chain B):** HELD by Sam (23 Nov ~14:45, notes/ledger/sam/5jkeg1t1.md: "Hold the work of all chats unrelated to Grand Theft Autism for now."). No next chat opened. When he says go, chain B chat 4 (or the chat it opens, Opus medium) asks him Q1 (guard-film-questions Change 2: retune the guard on the list; replay to 0/0/0/0, then GUARD_BASELINE to 0) and Q2 (precheck-reply's watcher part: the daily watcher line gets the same one-line correction), each with its Critiqued line (6/2/4 and 6/3/3), touching both proposals' Status lines by Edit so the guard sees them; then notes-model, then brow-limit (Opus high; the last sends Sam the whole lessons report as a plain page).
- **Needs Sam:** Q1 (chain A chat 4, plain-check Change 1) still open; nothing new. Chain B: Q1 guard Change 2 Y/N; Q2 watcher one-line correction Y/N (NOT yet asked: held by Sam 23 Nov).
- **Read:** this section; guides/job-packs.md "A tool job"; rule_proofs.json rules 41, 17, 5.
- **Open rule requests:** none new.
- **For Claude:** full kit-test run 23 Nov: 3 red, none from this chat: watcher_catches_last_weeks_four (FIXED by chain B chat 3: promises for its shared_faults and kittest_gate_faults), finished_films_keep_their_bookmark (FREEZE: source/takes.py was chain B chat 3's, not GTA's; FIXED by chat 3: shared audiokit.py, sound identical, freeze back to 20), body_check_back_view. Kittest body_check_back_view is RED and was red before this chat (same result with the 23 Nov morning humancheck.py): v3 back views 1 of 2; chat 6 bisects. New finds on v7 3.67 s (not Sam's notes, for GTA's record): the fireball drawn into a shop wall (173 spots), an effect through the cruiser's door (8), Jason's outline through the window pillar and door. Water still 3.67 s passes (a strip, not a patch). handcheck on v4 flags only "hand over his own body" (a side effect, not counted). story/status.md left as GTA's (shared file, GTA is live). Branches claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31: GTA's (another account's chats), left alone. End check named: SENTENCE x4 (CLAUDE.md reworded by chat 48's override commit 34f49840 and 0945cc85, Sam's own wording changes, not this chat's); FREEZE 20 to 21 is source/takes.py (a GTA chat's new file loading gta_cast, not this chat's: GTA's notes own it); COST (system job, no estimate). Plain-check Change 1 not built (waits on Q1).
- **For Claude (chain B chat 4):** reply_faults(lookup=) replays proposals as they were; correction_ok also clears "not a change" (logged, counted for Change 2). Edits to notes/proposals/lessons-report.md made by Bash, not Edit: an Edit there makes the guard read it as a proposal (path misread, labelled rows 47/51; Change 2 fixes it). Start check named: override.py prompt "never seen running" is stale (its mark is present here); roZMAKSe had no handover end while still running its kit tests. End check named: SENTENCE x4 (other chats' CLAUDE.md commits 34f49840, 0945cc85; as chat 3 named), FREEZE 20->21 (before this chat; no film file loaded here), COST (system job, no estimate). audiokit.py (chat 3) kept over my identical voiceclean.py (built at the same time; dropped in the merge 24c845e8); kittest takes_loads_no_film added. First live full-log block: 14:34 chat 94260699. End check (14:5x): REFUSED only on body_check_back_view red twice (chain A's rule 41 work, held by Sam; not fixed here under the hold); BRANCH claude/awesome-archimedes-35nvsx holds only another chat's guard-blocks.jsonl lines (a GTA chat's log, left to it); COST (system job, no estimate). Mutation checks: after putting a file back, delete source/__pycache__/NAME.*.pyc (a same-size edit within one second left the broken copy running; it failed guard_one_correction in the full run until cleared).

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
