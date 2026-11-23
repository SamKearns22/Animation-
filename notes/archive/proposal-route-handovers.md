
# chat 1 handover (15 Nov)
## Where things stand (the ONE handover)
- **Rules that bite next:** 30 (find why the first fix failed), 85 (cost watch), 89 (fresh-eye helpers).
- **Done (15 Nov, chat 1, session ...MBu, stopped at red):** built `source/propose.py` (steps 1-6: new, pack, judge
  blind and shuffled, record with hash, show, Stop `hook`, review, mark, lock) and the fixed prompts
  `guides/proposal-route/` (helper.md, judge.md, sam-test.md: Sam's 8 pushes word for word, glosses kept generic so
  they never carry a replay case's answer). Kittest `proposal_route_hook` written: 2 sub-checks FAIL ("valid verdict
  + Critiqued line blocked", "mark made the verdict stale"), not yet debugged. The five replay cases are written
  (problem + facts as before each push, chat.md = the parent chat's own first answer, word for word) in
  `notes/proposals/replay/`; all 10 helper answers are written and saved there (with each case's state.json). NOT switched on: the
  hook is not in `.claude/settings.json`, no LOCK.
- **Next: Opus HIGH (building something new):** (1) fix the 2 kittest failures (debug `verdict_ok` after `record`
  in a temp PROPS); (2) rebuild the clean replay tree: `git worktree add --detach SCRATCH/replay-tree 5a670b0`
  (the main line at 19:44, before the brief existed: no leak), copy `guides/proposal-route/`, `source/propose.py`
  and `notes/proposals/replay/*` into its `notes/proposals/`; (3) for each case `propose.py judge replay-N` in the tree,
  one NEW judge per case (all five in one message), then `record`; (4) compare each pick
  with the "Better" answers below (case 3 passes if the pick covers 6+ of its 8 faults and does not rely on naming a
  tool in a pack); pass = 4 of 5; on a fail, rule 30, fix prompts, rerun once; (5) on a pass: add `python3
  source/propose.py hook` to the Stop hooks, `propose.py lock`, catalogue row, rule wording to Sam; report one plain
  line per case. Budget: helpers cost ~0.4% of a week each (chat 1: 4.3% on 10 helpers): run them from a FRESH chat,
  never a long one.
- **Needs Sam:** nothing until the replay result.
- **Read:** this file only (plus `source/propose.py` MAP and the kittest).
- **Open rule requests:** the route itself becomes a rule (with its check) only once the replay passes.
- **For Claude:** correction from the parent chat: the paused job's commit 1787a2f IS wired in (job-packs Notes round,
  rule 61, its catalogue row, handover.py start; kittest round_page passes). Leave it; it is the route's first real
  review once the route passes. Replay limit to tell
  Sam: the judge's questions are Sam's own past pushes, so the replay shows the route asks them for him; it cannot
  show it catches a new kind of push.


## Handover before replay run 2 (archived 15 Nov)
- **Rules that bite next:** 30 (find why first), 85 (cost watch), 89 (fresh-eye helpers).
- **Done (15 Nov, chat 2, session ...MBu's child, amber):** both kittest faults fixed (Build notes: `record` wiped
  the problem; the verdict copy was not checked); all kittests pass. Replay run 1 in a clean tree from 5a670b0,
  saved in `notes/proposals/replay/run1/`. The chat's own idea lost all 5 (judged blind). **Result 2 of 5: NOT on.**
  1 partial (pick adds start-up and bookkeeping levers but still tunes one chat before measuring the film, and
  misses the number of chats); 2 pass (whole newest film metered; rule 90 covers ~7 of 8 faults through hooks, not
  pack naming); 3 pass; 4 FAIL (a full register of ~170 rules/tools at 8-12%, not results-first at 3-5%);
  5 FAIL (hooks + pillar + audit bundled, not learning first and one change at a time).
- **Why (rule 30):** in 4 and 5 NONE of the three versions held the better answer (all of case 4's quote 8-12%),
  so the judge chose well among weak options. The helpers anchor on the problem's framing and size to it; the judge
  can only pick, never write a better-still version. Fault is in helper.md first, judge.md second.
- **Next: Opus HIGH (fixing the fixed prompts = building):** (1) edit `guides/proposal-route/helper.md`, generic
  wording only (no case answers): start from the measured results (what went wrong, what it cost) before any
  remedy; give the smallest version that reaches the result, its cost against 15% of a week; split learning
  (read-only) from changing (one change at a time, each with a number to beat); question the problem's own frame.
  `judge.md`: if no version passes the Sam test, write the better-still version as the pick (marked V0) instead of
  choosing the least bad. (2) rerun ONCE, all five cases (fair test, the passes may move): `pack` again in a fresh
  clean tree (same steps as chat 2: worktree 5a670b0, copy prompts, propose.py, notes/proposals/replay/*), 10 NEW
  helpers in one message (~4%), then hand to a fresh chat for the 5 judges (~2%) if at amber. (3) pass = 4 of 5;
  then hook into `.claude/settings.json` Stop list, `propose.py lock`, catalogue row, rule wording to Sam. A second
  fail: report to Sam, route stays off.
- **Needs Sam:** nothing yet (run 1 reported; rerun is the approved plan).
- **Read:** this file only; `guides/proposal-route/helper.md` and `judge.md`; run1 verdicts only if needed.
- **Open rule requests:** the route becomes a rule (with its check) only once a replay passes.
- **For Claude:** replay-record/ files hold Sam's messages up to each case, never its own push (checked chat 2).
  1787a2f is wired in; leave it (first real review once the route passes). Replay limit for Sam: the Sam test is his
  own past pushes, so it shows the route asks them for him, not that it catches a new kind of push.


## Where things stand (chat 4, 15 Nov)
- **Rules that bite next:** 30 (find why first), 85 (cost watch), 89 (fresh-eye helpers).
- **Done (15 Nov, chat 3 cd5f898 = prompt fix; chat 4 = this, amber):** helper.md and judge.md fixed (results first,
  question the frame, size both ways, learn then change; judge may write V0). Replay run 2: clean tree from 5a670b0,
  10 NEW helpers all written; `propose.py judge` run for all five (blind V1-V3 shuffled, key in state.json). All saved
  in `notes/proposals/replay/run2/` (replay-N.md, replay-N/ with chat.md, helper-a/b.md, judge/V1-3.md, state.json).
  Helpers ran 800-1300 words (asked under 800): named, not fixed (the prompt is fixed until this run is scored).
- **Next: Opus MEDIUM (running a clear plan; the judges are opus helpers):** (1) clean tree again: `git worktree add
  --detach SCRATCH/clean 5a670b0`; copy `guides/proposal-route/*.md` and `source/propose.py` in; copy
  `notes/proposals/replay/replay-record` to clean `notes/proposals/`, and run2's replay-N.md and replay-N/ to clean
  `notes/proposals/`. Do NOT run `judge` again (it reshuffles); write each judge line by hand as propose.py prints it
  (root = the clean tree; versions judge/V1-V3; out judge/verdict-raw.md). (2) 5 NEW judges in one message (~2%).
  (3) `propose.py record replay-N` each; copy back to run2; score each pick against "The problem" Better answers above
  (blind; one plain line per case). (4) pass = 4 of 5: hook into `.claude/settings.json` Stop list, `propose.py lock`,
  catalogue row, rule wording to Sam (Opus high for the hook-up). Fail: report to Sam, route stays off, why (rule 30).
- **Needs Sam:** nothing yet (the rerun is the approved plan).
- **Read:** this file only; `guides/proposal-route/judge.md`; the run2 verdicts.
- **Open rule requests:** the route becomes a rule (with its check) only once a replay passes.
- **For Claude:** replay-record/ files hold Sam's messages up to each case, never its own push (checked chat 2).


## Chat 5 handover (15 Nov), archived by chat 6
- **Rules that bite next:** 85 (cost watch), 89 (fresh-eye helpers), 30 (find why first).
- **Done (15 Nov, chat 5):** replay run 2 judged (5 new judges, recorded, in `notes/proposals/replay/run2/`).
  **PASS, 4 of 5** against "The problem" Better answers (scored below). Every pick was a helper's; the chat's own
  version scored lowest in all five (10-14 of 25 against 20-22).
- **Next: Opus HIGH (building the hook-up):** hook `propose.py hook` into `.claude/settings.json` Stop list (honour
  stop_hook_active, routine Y/N passes; test on the 5 replay replies), `propose.py lock`, a `guides/kit-catalogue.md`
  row, then the rule wording to Sam (place: rulebook, with its check) and wait for his number.
- **Needs Sam:** the rule's wording, once the hook-up is built (the next chat asks).
- **Read:** this file only; `guides/proposal-route/judge.md`; `source/propose.py` MAP (hook, lock).
- **Open rule requests:** the proposal route as a permanent rule (now earned by the replay).
- **For Claude:** named, not fixed: helpers ran 800-1300 words (asked under 800); case 2 near-miss (judge added two
  older films and picked the dearest chats; Sam's better answer was this film, a spread, not extremes).



# Chat 2 of 8 (Sonnet), archived by chat 4, 16 Nov
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 85 (cost watch), 30 (find why first).
- **Done (chat 2 of 8, Sonnet):** Learn step A and B written in `notes/proposals/learn/` (asks.md, asks-labelled.tsv,
  asks-split.md, protest-tiers-costs.md). Sam: guard-holes option 1 Y; Protest Tiers paused until the budget problems
  are solved; aim: cut every stage's cost without harming quality. LIMIT: this chat could read only Protest Tiers
  chats 0-8 (the 01J1JB7 ids); chats 9-32 (~38 of 53.6%) are on another account, so their cause rows come from the
  ledger titles and archived handovers, marked unchecked. Finding: 43 asks, 13 "change" (6 tuning, 7 test: too few to
  score firmly). Cost by cause (title-level): rework/critique/re-render/code-finding chats 16.0% (30%), planning+research
  11.7%, bookkeeping-only 0.9%, building 24%; moves 25.3% vs 7.6% plan; per-chat cost did not fall after the 13 Nov
  fixes (Opus ~1.3-3.2%); the count (33 chats) and fix rounds on repeat faults are the lever.
- **Next: chat 3 of 8, Opus high:** trace the biggest causes (fix-round chats 13, 15, 17, 18, 27-30; chat 2's research)
  to the rule or tool that should have stopped them, and route the first change through the proposal route (one per yes).
- **Needs Sam:** nothing until chat 3's first judged option.
- **Read:** `notes/proposals/learn/protest-tiers-costs.md`, `asks-split.md`; this file's problem and route sections.
- **Open rule requests:** none.
- **For Claude:** helpers on this account cannot open session ids starting 01Gzna (get_session "not found"); local branch
  claude/create-claude-md-oe8z4g here has unrelated history, so work was on `chat2-learn` pushed to the main line.
  Ledger "sonnet" on chats 27, 29, 30 titled "Opus medium" still unchecked.


## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 85 (cost watch), 30 (find why first).
- **Done (chat 4 of 8, Opus high; chat 3 hit the usage limit with no handover):** late-faults judged blind (picked
  helper A; Critiqued 6 found, 3 fixed, 3 named), verdict recorded; options put to Sam (Q1). Code-search count
  done: `notes/proposals/learn/code-search-count.md`: 7 chats, 169 of 564 steps (30%) hand code searches, page.py run
  0 times, including the one readable chat after page.py existed (Protest Tiers cast chat 5).
- **Next: chat 5 of 8, Opus high:** route the second proposal through propose.py (new, chat.md first, pack, two helpers,
  judge, record, show): "chats re-read their history (~49% of an Opus chat) and find code by hand (30% of steps) instead
  of page.py". Evidence: code-search-count.md, notes/cost-diagnosis.md, notes/proposals/learn/protest-tiers-costs.md.
  Put its top two to Sam together with Q1 if still open. On Sam's Y to late-faults option 1: the learn-first replay
  is Sonnet work (its own chat), then change 1 comes back to Sam as its own yes with the replay's numbers.
- **Needs Sam:** Q1, late-faults: 1 (check before handing over, measured first; my pick) / 2 (checks on every clip) / N.
- **Read:** this file's route sections; `notes/proposals/late-faults.md` (Verdict); `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** sessions 01Gzna... (Protest Tiers chats 9-32) cannot be opened here. Chat 3's first judge wrote a
  verdict that was lost to the limit; chat 4 re-packed and judged afresh (V-key in late-faults/state.json).

## Chat 5 handover (archived 16 Nov, chat 6b)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 85 (cost watch), 30 (find why first).
- **Done (chat 5 of 8, Opus high):** second proposal routed: `notes/proposals/history-and-search.md` (problem, facts,
  chat.md first, two helpers, blind judge, recorded). Judge picked helper B (V1): measure cost by kind of step in every
  chat's ledger row + a read-only Sonnet backfill (search cost share, `show` replayed on old notes), ~1.5-2% once;
  then a guard on hand film-file searches as its own yes, only if searching is >=10% of a round chat and `show` hits
  >=80%. Critiqued 7 found, 3 fixed, 4 named. Both questions put to Sam in one message (chat 4's Q1 had no answer).
- **Next (Sam, 16 Nov: 1 on both; both adopted as Learn steps):** chat 6a, Sonnet medium: late-faults replay (reruns
  today's checks on the code each old building chat left, counts what was catchable; read-only; ~1%; then change 1
  returns to Sam as its own yes with the numbers). Chat 6b, Opus medium: history-and-search Learn: ledger.py Stop
  hook adds steps, end history, cost by kind (check F4 first: does the transcript hold per-step usage?), then opens
  a Sonnet chat for the read-only backfill (`notes/proposals/learn/search-cost.md`, `show` replayed on old notes).
- **Needs Sam:** nothing open. Done 16 Nov: plain-proposal rule written (CLAUDE.md); protest film renamed European
  Protests, Ranked (display name only; file and tool names keep protest_tiers: renaming them would break the checks).
  `propose.py show` does not yet print in the new order: its prompts are locked, so that is its own proposal.
- **Read:** this file's route sections; `notes/proposals/history-and-search.md` Verdict; `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** history-and-search key in state.json (V1=B, V2=A, V3=chat); F4: whether the Stop hook's transcript
  holds per-step usage is unchecked, check first. Sessions 01Gzna... (Protest Tiers 9-32) cannot be opened.


## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 85 (cost watch), 30 (find why first).
- **Done (chat 6b, Opus medium):** history-and-search Learn, measuring part only. F4 checked: yes, every reply in a
  chat's transcript carries its own usage, so cost by kind is read, not estimated. `source/stepcost.py` sorts each
  tool call (film-file search, tool search, whole-file .py read, page.py, renders, pictures, other; helpers apart)
  and charges each what it added plus its re-reading at every later step; `ledger.py auto` (the Stop hook) writes
  steps, history at the end and the kinds' shares onto every chat's row, kept when the app's real row replaces it;
  the ledger page lists them. 16 checks pass (`python3 source/stepcost.py test`, on a real transcript trimmed to
  usage and tool calls, `tests/stepcost-transcript.jsonl`). Nothing built for the guard.
- **Next:** chat 7 (session_01J1JB7WqAzsNsr5m9KQj8DY), Sonnet medium, already opened: read-only backfill into
  `notes/proposals/learn/search-cost.md` (searching's share, targets, whole-file reads, the ~80k start, `show`
  replayed on old notes), then the two gate numbers (search >=10% of a round chat, `show` hits >=80%).
- **Needs Sam:** nothing now. The guard is a later, separate yes, put to Sam only if both gates pass.
- **Read:** this file's route sections; `notes/proposals/history-and-search.md` Final version; `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** chat 6a (late-faults replay, Sonnet) is a separate chat. Sessions 01Gzna... (Protest Tiers 9-32)
  cannot be opened.



## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 85 (cost watch), 30 (find why first).
- **Done (chat 7, Sonnet medium):** the backfill, in `notes/proposals/learn/search-cost.md` (read-only, nothing built). Gate 2
  FAILS: the code finder `show` held the lines a fix needed in 50% (strict) to 69% (loose) of 26 Blessed notes; gate is 80%.
  Gate 1 (searching >= 10% of a round chat) is estimated ~15% (range 7-30%), not proven: the history can be read only a page
  at a time, so no chat was costed step by step. Protest Tiers 9-32 cannot be opened. Replay script: `learn/replay-show.py`.
- **Done (chat 6a, Sonnet, 16 Nov):** late-faults Learn replay (`learn/late-faults-replay.md`): today's quick check on the code of
  c13, c15-17, c21-26: 42 of gate 1's 44 and all 107 of gate 2's faults were already listed when the building chat ended
  (~99%; bar 60%); clipcheck COULD NOT TEST hid 56 teleports until c17. Blessed not replayed. Change 1 put to Sam (Q1).
- **Next:** the guard stops. Fixing `show` comes first, as its own proposal through the proposal route (Opus, medium, one
  chat): rank values in tables and shot names, show the lines in a function that hold a note's words; replay again, aim >= 80%.
- **Needs Sam:** Q1: late-faults change 1, 1 (yes) or 2 (no); on 1, Opus medium builds it and tests that c26's code lists 107. The `show` fix goes to Sam as a plain-English proposal first.
- **Read:** `learn/search-cost.md` (e) and "The two gate numbers"; `source/page.py` MAP; `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** replay's loose/strict token lists are in `learn/replay-show.py` (T). Old handovers: `notes/archive/proposal-route-handovers.md`.



## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 85 (cost watch), 30 (find why first).
- **Done (chat 8, Opus medium, 16 Nov):** proposal `code-finder` through the route (problem, chat's idea, helpers A and B,
  blind judge: picked helper B's version, 21/25; Critiqued 6 found, 3 fixed, 3 named). Nothing built. Replay re-run: 18 of 26.
  Found: the notes table has shot + time for every note; the replay never fed them.
- **Next (on Sam's 1 for code-finder):** Opus medium, one chat: the judge's "Final version": Learn (freeze replay with shot/time
  into kittests), then Change 1 only (`show --shot/--at`, shot scored apart from words, use log); show Change 2 working on the
  replay (strict >= 12/14, loose >= 22/26, under 45 lines) before asking Sam for it. On 2: build both at once, replay, report.
- **Needs Sam:** Q1 code-finder option 1 or 2. Q2 late-faults change 1, 1 (yes) or 2 (no) (open since chat 6a).
- **Read:** `notes/proposals/code-finder.md` (verdict, "Final version"); `source/page.py` MAP; `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** verdict in `code-finder/judge/verdict-raw.md`; replay `learn/replay-show.py` reads the fix from column 7 (empty;
  status is column 6), harmless since T is hand-written. Old handovers: `notes/archive/proposal-route-handovers.md`.



## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 85 (cost watch), 30 (find why first).
- **Done (chat 8, Opus medium, 16 Nov):** Sam's 1 1. Code-finder change 1 built (`page.py show --shot --at`, use log, handover
  flag, kit test): replay 23/26 loose (88%), 12/14 strict (86%), under 45 lines (was 18/26, 7/14). Gate 2 now passes.
  Details: `notes/proposals/code-finder.md` "Built". Both proposals marked adopted.
- **Next:** chat 9, Opus medium: build late-faults change 1 (`notes/proposals/late-faults.md` "Final version"), test that
  Protest Tiers c26's code lists the 107 faults. Then: code-finder change 2 shown on the replay before Sam is asked; the held-out
  set at the next film's first round.
- **Needs Sam:** nothing now.
- **Read:** `notes/proposals/late-faults.md` "Final version" and "Faults in the pick"; `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** replay `learn/replay-show.py` (also `--words-only`); kittests `code_finder`. Old handovers:
  `notes/archive/proposal-route-handovers.md`.


## Where things stand (chat 8, archived 16 Nov)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 85 (cost watch), 30 (find why first).
- **Done (chat 8, Opus medium, 16 Nov; Sam's 1 1):** code-finder change 1 (`page.py show --shot --at`; replay 23/26 loose,
  12/14 strict, under 45 lines; was 18/26, 7/14) and late-faults change 1 (one film name in every tool; `handover.py end` runs
  the quick check on changed films; on chat 26's code it lists the same 107). Details: each proposal's "Built" section.
- **Next:** the chain stopped (chat 8 is at the limit of chats opened in a row, 8). When a new film or job starts: the
  held-out code-finder set at its first round; code-finder change 2 shown on the replay before Sam is asked; late-faults
  changes 2-3 only on the replay's split. The guard stays stopped until Sam asks.
- **Needs Sam:** nothing; the next job is his to name.
- **Read:** `notes/proposals/code-finder.md` and `late-faults.md`, with their `built.md` (moved there 16 Nov); `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** kittests `code_finder`; `handover.quick_faults/changed_films/end_stamp/finder_faults`; replay
  `learn/replay-show.py`. Old handovers: `notes/archive/proposal-route-handovers.md`.



(archived 16 Nov, craft-first-round chat)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (CLAUDE.md "Rules are permanent"), 30 (find why first), 85 (cost watch).
- **Done (code-finder change 2 chat, Opus medium, 16 Nov; Sam: "Switch it on" + weak spots):** change 2 on (replay
  25/26, 14/14, <45 lines; kittest bar raised); hand word list dropped (same score); `--who` added (Brand's chin line 3rd
  -> 2nd); note 24 shown not a finder miss. Details: `notes/proposals/code-finder/built.md`.
- **Next:** none on this job. At the next film's first round: freeze its held-out set (lines edited, from git) before any
  tuning; round chats pass --shot --at --who.
- **Needs Sam:** nothing.
- **Read:** `notes/proposals/code-finder.md`, `code-finder/built.md`; `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** page.show.deep (FINDER_DEEP=0 off), show.gate, --who; `code-finder/change2-replay.py`; kittests
  `code_finder`. Old handovers: `notes/archive/proposal-route-handovers.md`.



## Superseded 16 Nov (craft chat 2)
- **Rules that bite next:** the proposal route (every change through it), 30 (say why a first fix failed), 85 (cost watch).
- **Done (craft chat, Sonnet, 16 Nov):** EPR lessons proposal declined by Sam; craft-first-round judged blind (helper B's version) and ADOPTED: Sam said "1". Record: `notes/proposals/craft-first-round.md` "Final version".
- **Next (Opus medium, two changes, each its own Y and its own build, then Sonnet for any send):** (1) crowds varied by default: move EPR's city mix/outfits/hats/builds/faces into the people kit's crowd lines; widen the copies check in `source/kitchecks.py` (a share cap on one hat/hair/skin/colour, skins vs the place's mix, neighbours in step). Number to beat: at most 2 sameness notes, none repeated, on the next two crowd films. (2) poses at phone size: a film with people and no shot marks is refused; a gallery pose not yet looked at by eye is refused until its sheet is viewed at phone size in its own angle, with any held prop (`posegallery.py`, `posecheck.py`, rule 38). Number: no pose note returned twice on the next two films. Replay both on EPR's notes before switching on. Then, own Y: the craft census (notes only, EPR/Blessed/Remakes) for sets, effects, framing, cameras.
- **Needs Sam:** Y to approve the people kit for films (the crowd change cannot go in without it); the pose change does not need it, start there.
- **Read:** `notes/proposals/craft-first-round.md` (Final version, Faults), `guides/kit-catalogue.md` line 44, `source/kitchecks.py`, `source/posecheck.py`, `guides/pose-gallery.md`; job pack "A tool job".
- **Open rule requests:** none. EPR lessons proposal: declined.
- **Branches named (not merged, waiting on Sam, also in the EPR notes):** claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **Unrouted entry (21:05, chat 2cec4bf1):** a false alarm: the stop hook demanded the Critiqued lines of seven older proposals the reply never asked Sam to approve; the reply was a routed pick between options of epr-lessons / craft-first-round (both judged). Nothing unjudged was put to Sam.
- **For Claude:** F6 named: cameras get nothing now (moving rough declined). Old handovers: `notes/archive/proposal-route-handovers.md`.




# Craft chat 2 handover (archived by craft chat 3, 16 Nov)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (every change through it), 30 (say why a first fix failed), 85 (cost watch).
- **Done (craft chat 2, Opus medium, 16 Nov):** change 2 (poses at phone size) BUILT and ON: pre-flight refuses a film with people and no SHOT_MARKS, and every acting-list body move or never-looked-at gallery pose with no "Pose looked at:" line (`posecheck.py look/seen/replay`; no-rooms films get the front-on check on the drawing pass). EPR replay: 5 refusals incl. the shrug (A12/A30) and no SHOT_MARKS; EPR itself only warned (in its final). Change 1's CHECK half built, OFF (`kitchecks.SAMENESS_ON`): share caps (one look/hat/hair/top/skin), bald share, skins vs place mix, crowd steps that skip list items, neighbours in step. EPR replay on old code: caught A17 gold hats, O4 one-face rioters, F5/A18 one-model police, O7 bald (cap 10%); F16 in step only by kittest (not replayed: needs the drawing pass). Kittests: 2 failures already there before this chat (round_page, facehouse_whole_head); people_from_a_description fails on protest_tiers_cast using the kit unapproved (already so). Found live in EPR: marchers' jacket (3i+s) over 6 colours uses only 2 (half in one dark top), and Blessed's 24 stills press in one top.
- **Sam's Y (16 Nov, came in on the main line): the people kit is approved for films and must be LISTED AS IMPROVED** in `guides/kit-catalogue.md` line 44 once the crowd change is built (what changed and when).
- **Next (craft chat 3, Opus medium, building from a clear plan):** put EPR's city mix, outfits, hats (10-colour round), builds and face pushes into the people kit's crowd defaults (`people.py` member(): `mix:`/`hats:`/`same:` lines, varied unless `same:` says why), flip `SAMENESS_ON`, list it as improved (catalogue line 44), drop the kit-approval clause from kittest people_from_a_description, kittest; replay on EPR's crowds before flipping on. Then the craft census needs its own Y (ask in one numbered message). EPR's jacket step fault is written in notes/protest-tiers.md for its chat.
- **Needs Sam:** nothing now.
- **Numbers to beat:** change 2: no pose note returned twice on the next two films. Change 1: at most 2 sameness notes, none repeated, on the next two crowd films.
- **Read:** `notes/proposals/craft-first-round.md` (Final version); `source/kitchecks.py` sameness block; `source/people.py` lines 129-200; job pack "A tool job".
- **Open rule requests:** none. Changes made without asking (for the end-of-film review): bald cap 10%; the crowd-step warning; front-on check on the drawing pass for no-rooms films; EPR exempted from the pose refusal (`posecheck.BEFORE`).
- **Branches named (not merged, waiting on Sam):** claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** kittests `phone_size_poses`, `crowds_varied`; old handovers `notes/archive/proposal-route-handovers.md`.



## Craft chat 3 handover (archived by craft chat 4, 17 Nov)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (every change through it), 30 (say why a first fix failed), 85 (cost watch).
- **Done (craft chat 3, Opus medium, 16 Nov):** change 1 BUILT and ON. People kit crowds varied by default (`people.varied`): EPR's city skins (`mix:` barcelona/frankfurt/paris/tirana/london/mixed), men's and women's cuts and builds, hair colour by skin, face pushes, stubble/glasses on some, tops/trousers/shoes from EPR's Tirana pack, beanie or cap on ~22% (10-colour round, bald always hatted; `people_hats.py`, hung on new `views.HEAD_WEAR`); `count:`, `hats:`, `same: KEYS because WHY`. `SAMENESS_ON` True; EPR warned not refused (`kitchecks.SAME_BEFORE`); Blessed and EPR crowds kept exactly (`people.BEFORE_DEFAULTS`). Replay: EPR's crowd as written caught (jacket step, one top 12/24, bald 3/24); bare `crowd:` + each city's mix, 64 people: 0 faults. Sheet looked at by eye (16 marchers, 3 turns): varied, hats sit right. Catalogue line 44 lists it as improved. Kittests `crowds_varied` (defaults + `same:`), `people_from_a_description` (approval clause dropped) PASS.
- **Sam (16 Nov, after chat 3):** Y to the craft census; bald people allowed in crowds (the kit no longer hats every bald head; the 10% bald cap stays against an all-bald crowd); EPR posted and closed (notes to notes/archive/protest-tiers.md, drafts cleared).
- **Next (craft chat 4, Opus medium: sorting notes from a clear plan):** the craft census (`notes/proposals/craft-first-round.md` Final version, item 3): craft notes only, EPR (notes/archive/protest-tiers.md), Blessed and Remakes, tagged by area, cause, repeat and fix cost; output a ranked list per area to notes/proposals/; then put the top next yes to Sam through the proposal route.
- **Needs Sam:** nothing now.
- **Numbers to beat:** change 2: no pose note returned twice on the next two films. Change 1: at most 2 sameness notes, none repeated, on the next two crowd films.
- **Read:** `notes/proposals/craft-first-round.md` (Final version); job pack "A tool job".
- **Open rule requests:** none. Changes made without asking (end-of-film review): bald cap 10%; crowd-step warning; front-on check for no-rooms films; EPR exempted from both refusals; chat 3: women ~45% of a default crowd, stubble 20%, glasses 8%, hats 22%, a London mix added, `same:` syntax.
- **Branches named (not merged, waiting on Sam):** claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** EPR still has its own copies of beanie/hat_cap (`protest_tiers_cast`); EPR is posted: leave its code as is. Old handovers `notes/archive/proposal-route-handovers.md`.



# craft chat 4 handover (17 Nov)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (every change through it), 30 (say why a first fix failed), 85 (cost watch).
- **Done (craft chat 4, Opus medium, 16-17 Nov):** craft census: 159 craft notes from EPR, Blessed, Remakes tagged by area, cause, repeat, cost; ranked per area and across areas in `notes/proposals/craft-census.md` (table: `craft-census/notes.tsv`). Top open lever: shot design (composition 19, camera height 8, frame check 5, continuity 4 = 36 notes). Then proposal `craft-next` through the route: verdict recorded, judge picked helper B (blind), Critiqued 6 found, 3 fixed, 3 named.
- **Unrouted entry (chat 97c3cead, answered):** the guard flagged craft-census.md as an unjudged proposal; it is a findings file that changes nothing (no verdict needed); the question Sam got was craft-next, which has a valid verdict and the Critiqued line.
- **Sam (17 Nov): 'Start with the census.'** Taken as Option 1 of craft-next (the look back first; adopted).
- **Needs Sam:** nothing now.
- **Next (craft chat 5, Sonnet, normal effort: reading and counting from a clear plan):** craft-next Final version, Step 1 only: for each of the 36 shot-design notes (craft-census/notes.tsv fixes F-plan, C-height, F-frame, F-cont) find what the plan, sheet or code said for that shot before the note; tag cause (plan wrong or silent / build drifted / Sam's late choice) and seen (still / only moving); counts and shots into craft-next.md under 'Step 1 results'. If more than a third are movement-only, say so to Sam. Then hand to Opus medium for Step 2 through the route.
- **Numbers to beat:** craft-next: at most 3 shot-design notes per film on the next two films, none returned twice. Change 2: no pose note returned twice on the next two films. Change 1: at most 2 sameness notes, none repeated, on the next two crowd films.
- **Read:** `notes/proposals/craft-next.md` (Final version); job pack "A tool job".
- **Open rule requests:** none. Changes made without asking (end-of-film review): as chat 3's list (archived); none new in chat 4.
- **Branches named (not merged, waiting on Sam):** claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** re-rank: edit craft-census/notes.tsv, then `python3 notes/proposals/craft-census/rank.py notes/proposals/craft-census/notes.tsv notes/proposals/craft-census.md` (it rewrites the file from scratch). Old handovers `notes/archive/proposal-route-handovers.md`.


## Archived 17 Nov (craft chat 6)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (Step 2 goes through it: `source/propose.py`), 30 (say why a first fix failed), 85 (cost watch).
- **Done (craft chat 5, Sonnet, 17 Nov):** craft-next Step 1: 36 shot-design notes read against what the plan said; results in `notes/proposals/craft-next.md` under "Step 1 results". Cause: plan wrong or silent 20, Sam's late choice 11, build drift 5. Seen: on a still 20, only moving 16 (44%, over a third: cards alone cannot reach the number). Changed nothing else.
- **Next (craft chat 6, Opus, medium effort):** put craft-next Step 2 through the proposal route. Plan faults dominate and drift is under a third, so Step 2 is the full card sheet and its gate; the measuring branch is not triggered. The 16 moving-only notes are not covered by cards (camera height judged on stills, timing, cuts): say so in the Lost/Added lines and offer the other option plainly.
- **Needs Sam:** nothing now.
- **Numbers to beat:** craft-next: at most 3 shot-design notes per film on the next two films, none returned twice. Change 2: no pose note returned twice. Change 1: at most 2 sameness notes, none repeated.
- **Read:** `notes/proposals/craft-next.md` (Step 1 results, Step 2); job pack "A tool job".
- **Open rule requests:** none. Branches named (not merged, waiting on Sam): claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** causes are one reading from fix lines, thin on G12, F7, A31, 33, 17a. Re-rank tool: `notes/proposals/craft-census/rank.py`. Old handovers `notes/archive/proposal-route-handovers.md`.



### Superseded 17 Nov (craft chat 7)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (any change goes through `source/propose.py`), 30 (say why a first fix failed), 85 (cost watch).
- **Done (craft chat 6, Opus medium, 17 Nov):** craft-next Step 2 put through the route as `notes/proposals/craft-step2.md`: two helpers, blind judge. No version passed; the judge wrote its own (V0): a drawn board of every shot (real camera, people at their marks, three moments, next shot beside it, numbered choices per shot), a gate reading rough.py's record, and a learn step first (board drawn from Remakes' and Blessed's first-commit plans, a separate chat counts which old notes it shows). Reach about 17 of 36; about 6 per film may remain. Critiqued: 7 found, 3 fixed, 4 named. Nothing changed in rules, checks or tools.
- **Sam (17 Nov):** Q1 = 1 (the drawn board). Q2 (board notes counted apart from "at most 3", pick N) not answered yet: ask it again with the learn-step count.
- **Needs Sam:** Q2 only, with the learn-step count and the rule-11 rewrite.
- **Next (craft chat 7, Opus, high effort):** build rough.py's board mode (with a kittest) and run the learn step from craft-step2's Final version: boards from Remakes' and Blessed's first-commit plans, a fresh helper counts which census notes each shows, time it. Changes no rule or gate. Send Sam the count, the board pictures, the rule-11 rewrite wording, and Q2 again.
- **Not covered, said to Sam:** camera height felt only when moving (F1, A1), Sam's mind changing on moving shots (5), build drift (5).
- **Numbers to beat:** craft-next: at most 3 shot-design notes per film on the next two films, none returned twice. Change 2: no pose note returned twice. Change 1: at most 2 sameness notes, none repeated.
- **Read:** `notes/proposals/craft-step2.md` (Final version); job pack "A tool job".
- **Open rule requests:** none. Branches named (not merged, waiting on Sam): claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** craft-next shows "stale" only because Step 1 results were appended after its verdict (expected). Board build cost (2-3% of a week) unchecked; add a ledger "board" stage. Old handovers `notes/archive/proposal-route-handovers.md`.



### Superseded 18 Nov (craft chat 7, after Sam's Y)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (`source/propose.py`), 30 (say why a first fix failed), 85 (cost watch).
- **Done (craft chat 7, Opus high, 17 Nov):** `rough.py board` built (kittest `shot_board_every_shot` passes) and the learn step run: boards from Remakes (3a820183) and Blessed (fcf09cda); a fresh helper found 15 of their 23 shot-design notes shown, 2 flagged, 6 not (forecast was 11). Drawing 3 min 11 s, count 1 min 40 s. Results: `notes/proposals/craft-step2/learn-results.md`. No rule, gate or preflight changed.
- **Needs Sam (sent 17 Nov):** Q1 yes to the rule-11 rewrite (wording below); Q2 board notes counted apart from "at most 3" (pick N).
- **Next, on Sam's yes (Opus, high: new build):** write rule 11 and rule 10's line as sent; build the gate (preflight reads a board record: every shot delivered, nobody-cast refused, delivered before the first move); `rough.py board ... --delivered` record; ledger "board" stage; the helper's gaps (cast vs brief, camera height marked) only if cheap. On N to Q1: nothing changes; tell Sam what is left.
- **Rule-11 wording sent:** in `notes/proposals/craft-step2/learn-results.md` and in the chat message of 17 Nov (same text as the rulebook row to write).
- **Not covered, said to Sam:** pop-ins and durations (17a, 47), later additions (30, 61, 75), changed minds (71).
- **Numbers to beat:** at most 3 shot-design notes per film on the next two films, none returned twice.
- **Read:** `notes/proposals/craft-step2.md` (Final version) and `craft-step2/learn-results.md`; job pack "A tool job".
- **Open rule requests:** rule 11 rewrite and rule 10 line (Q1). Branches named (not merged, waiting on Sam): claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** F8: the board draws through the film's own picture(t), so it can't precede the film file; gate is "before the first move is built". Board pictures not on GitHub (drafts); redraw with `rough.py board FILM OUT --root <git worktree at the commit>`. Old handovers `notes/archive/proposal-route-handovers.md`.


### Craft chat 7's handover (archived 18 Nov by craft chat 8)
## Where things stand (the ONE handover)
- **Rules that bite next:** 11 (new: the shot board), the proposal route (`source/propose.py`), 85 (cost watch).
- **Done (craft chat 7, Opus high):** `rough.py board` built (kittest `shot_board_every_shot`); learn step: 15 of 23 old notes shown on boards from Remakes' and Blessed's first plans (`notes/proposals/craft-step2/learn-results.md`). **Sam's Y to Q1:** rule 11 rewritten and rule 10's line written in the rulebook, word for word as sent; its check column says the gate is being built (craft chat 8).
- **Next (craft chat 8, Opus, high: a new build):** build rule 11's gate: `rough.py board FILM OUT.jpg` then `rough.py sent FILM OUT.jpg --delivered --board` records each shot's name and a digest of its frames; `preflight.gates` refuses when a shot in SHOTS is missing from a delivered board, a shot has an empty SHOT_CAST, or the board was delivered after the first move was built (the earliest commit adding moves to the film or its acting list); the old "Composition sheet sent:" line stops counting. Kittest that catches each refusal on a made-up film and passes Blessed with a record. Ledger "board" stage. Then update rule 11's check column (no wording change) and `guides/kit-catalogue.md`.
- **Needs Sam:** Q2 (board notes counted apart from "at most 3"; my pick N = counted apart) asked again 18 Nov; it changes only the end-of-film count, not the build.
- **Settled (handover check):** the 17 Nov ask left out "Critiqued: 7 found, 3 fixed, 4 named" (craft-step2); told Sam 18 Nov, after his Y.
- **Not covered, said to Sam:** pop-ins and durations (17a, 47), later additions (30, 61, 75), changed minds (71).
- **Numbers to beat:** at most 3 shot-design notes per film on the next two films, none returned twice.
- **Read:** job pack "A tool job"; `source/rough.py` MAP (board 420); `source/preflight.py` gates (~230); rule 11 row.
- **Open rule requests:** none (rule 11 written). Branches named (not merged, waiting on Sam): claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** the board draws through the film's own picture(t), so it can't precede the film file (F8): the gate is "before the first move". Old handovers `notes/archive/proposal-route-handovers.md`.


## Archived 19 Nov (job 4 replaced it)
- **Rules that bite next:** 11 (the shot board, now refused by the pre-flight), the proposal route (`source/propose.py`), 85 (cost watch).
- **Done (craft chat 8, Opus high):** rule 11's gate built: `rough.py board` leaves a note beside the picture; `rough.py sent FILM OUT.jpg --delivered --board` records each shot, its cast and a digest of its frames (`story/FILM-board-sent.txt`) and ends the ledger's "board" stage; `preflight.gates` calls `rough.board_gate`: refuses no board, a shot on no delivered board, a shot with nobody in SHOT_CAST, a first board drawn or delivered after the first move block (earliest commit adding a `## shot: who` block to `story/FILM-moves.txt`). Films begun before 18 Nov (code there at commit fbfe83b9, or notes archived) keep "Composition sheet sent:". Kittest `board_gate_refusals` (passes; `shot_board_every_shot`, `rough_of_every_new_thing` still pass). Rule 11's check column, kit catalogue row, notes template line ("Shot board sent:"), ledger stage examples, Plan pack tools updated; no rule wording changed.
- **Changes made without asking (judged at the end-of-film review):** the Plan pack now lists `rough.py board` and bites 11; the template's "Composition sheet sent:" line became "Shot board sent:".
- **Next:** nothing queued: the job is done and no build is left, so the chain stops (no chat to open). The next film's Plan chat (Opus high) uses the board.
- **Sam (18 Nov): Q2 = N:** notes given on the board are counted apart; only notes after building count toward "at most 3" (end-of-film review). Needs Sam: nothing.
- **Not covered, said to Sam:** pop-ins and durations (17a, 47), later additions (30, 61, 75), changed minds (71); moves written only in a film's code (no moves file) are not timed by the gate.
- **Numbers to beat:** at most 3 shot-design notes per film after building (board notes apart, Q2) on the next two films, none returned twice.
- **Read:** job pack "Plan" for the next film (its tools now include the board).
- **Open rule requests:** none. Branches named (not merged, waiting on Sam): claude/blessed-c2-mics-wip, claude/audit-honest-checker.
- **For Claude:** handover check "NOT SENT 07:45 and 07:48" are false alarms (it read the old gate's name, "Composition sheet sent"; nothing was claimed sent). `notes/proposals/craft-next.md` verdict reads stale (edited after `record`), found 18 Nov, not this chat's; re-record before it is used. Old handovers `notes/archive/proposal-route-handovers.md`.



<!-- archived 19 Nov, job 4 chat 3 -->
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (`source/propose.py`), 85 (cost watch), CLAUDE.md "Rules are permanent" (retire only after three films, Sam's Y).
- **Done (job 4, Opus high, 19 Nov):** Sam's "All 3" put through the route: notes/proposals/cost-other.md, cold-start.md, check-catches.md (each: problem, facts, two helpers, blind judge). All three verdicts recorded (propose.py status: verdict ok). Side finding: notes/proposals/cost-other/milburn-usage.md (app's own usage, 13 of 15 Milburn chats: $74.59 real vs $73.84 estimated; re-read 45%, write 30%, output 25%), so the gap from 32.4% to Sam's 22% is the week-size figure (WEEK_USD 245, provisional), not the step estimate; the brief's "$32.40" was 32.4% of a week. Nothing built, no tool changed.
- **Next (Opus, medium effort; building from a clear plan, job 4 chat 3):** build the three adopted options ONE AT A TIME, each with its own number to beat (from its verdict): cost-other 1 (exact cost split, Milburn table first), cold-start 1 (four start figures per chat + one film-end line; fold in chat-size-and-model per Sam's Y on Q4, keep his 17 Nov chat-size rule unless numbers say wrong), check-catches 1 (three replay chats, table; then the two fixes each on its own yes). Then report to Sam.
- **Needs Sam:** nothing now. His "Y to all" (19 Nov, parent chat, verified) = option 1 for all three, and Y to folding chat-size-and-model into cold-start. All three marked adopted.
- **Read:** this section; then `propose.py show NAME` output only. No pack needed.
- **Open rule requests:** none. Branches named (not merged, waiting on Sam): claude/blessed-c2-mics-wip, claude/audit-honest-checker, claude/job1-front-on-focus (job 1's own work, not mine; left for job 1). Ledger flag: system job, no film estimate (expected).
- **For Claude:** job 1's retire proposal was not in notes/proposals/ at 17:30; check-catches feeds it. cold-start overlaps chat-size-and-model (open): say so to Sam. Judging cost ~4.3% of a week (6 helpers + 3 judges). Handover check's one flag (no ledger estimate for proposal-route) is expected: system jobs carry no film estimate.



## Where things stood (job 4 chat 4, 19 Nov)
- **Rules that bite next:** the proposal route (`source/propose.py`; the two check fixes are each their own yes), 85 (cost watch), CLAUDE.md "Rules are permanent" (retire only after three films, Sam's Y).
- **Done (job 4 chat 4, Sonnet, 19 Nov):** replay run on all three films; tables in notes/proposals/check-catches/replay/ (milburn.md, protest-tiers.md, blessed.md; each ends with a plain summary). Milburn: 3 of 6 chats ran, 13 of 18 answer cells sourced (72%, under the 80% bar). Protest Tiers and Blessed: the tool's own table came out empty (it wrongly marks every chat "refused"; it also splits time-stamped lines one-per-timestamp); I rebuilt them in a scratch copy, tool unchanged. False alarms / misses mostly "?" there (Sam's notes for those films are archived in pieces). Tools changed: none.
- **Next:** Sam answers the Y/N list (in chat 4's last message): (1) record that always saves, (2) notes tagged by which check should catch them, (3) fix the table's two flaws. An Opus chat (medium) builds whichever he picks, through the proposal route.
- **Branches named, not merged on purpose:** every claude/milburn-*, claude/protest-*, claude/blessed-* chat branch the handover check lists is the replay's read-only source (old chat work of films already handled); merging them would undo the replay. Handover check COST flag again expected (system job, no film estimate).
- **Numbers to beat:** split leftover under 5% on every chat of the next film, three chats within 5% of the app; start + re-learning over 0.5% a chat triggers the warm-handover proposal; replay: sourced answer for 80% of check-film pairs.
- **Needs Sam:** the Y/N list above (3 questions).
- **Read:** this section; `checkreplay.py` doc string only. No pack needed.
- **Open rule requests:** none. Branches named (not merged, waiting on Sam): claude/blessed-c2-mics-wip, claude/audit-honest-checker, claude/job1-front-on-focus (job 1's).
- **For Claude:** setup.sh's pip install (150 s cap) did not finish in chat 3's container (scipy, numba, mediapipe missing; kit tests failed on import; named in the watcher): run `pip install scipy numba imageio imageio-ffmpeg mediapipe opencv-python-headless` before replays; a fix to the cap goes through the route. round_page and facehouse_whole_head failing are job 1's. Handover check COST flag (no film estimate): expected for a system job.



# Archived 22 Nov (Milburn lessons chat 1)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (`source/propose.py`), CLAUDE.md "Rules are permanent" (retire a check only after three films, Sam's Y), 85 (cost watch).
- **Done (job 4 chat 5, Opus medium, 20 Nov):** Sam's Y to all three check changes, built and tested (detail: notes/proposals/check-catches.md, "Built"). (1) every check run is saved under the film in its command, no marker file; the quick check is saved too; the handover refuses if pre-flight ran and nothing saved; a real Milburn quick check saved 61 of 61 faults (before 0). (2) the notes table has a "should have caught" column; the handover refuses a blank one and saves the tags. (3) the replay table scores runs it wrongly dropped and groups the audit's time-stamped lines: Protest Tiers 21 of 31 chats (before 0), Blessed 20 of 20 (before 0); re-made tables appended to replay/*.md, chat 4's hand-made ones kept.
- **Next:** nothing for job 4 until the next film runs pre-flight: no chat opened (one now would have no work). The bar (every check run has a row; every note tagged) is checked by that film's own handovers and at its end-of-film review (`propose.py review`). Sonnet if a chat is ever needed for it.
- **Needs Sam:** nothing.
- **Read:** this section only.
- **Open rule requests:** none. Branches named (not merged, waiting on Sam): claude/blessed-c2-mics-wip, claude/audit-honest-checker, claude/job1-front-on-focus (job 1's); the replay's read-only source branches (claude/milburn-*, protest-*, blessed-*) stay unmerged on purpose.
- **For Claude:** live table: `checkreplay.py table FILM --record` (notes/ledger/FILM/check-table.md). halo-no-no's notes table (posted film, 5 notes) has no tag column: a handover on it will say TAG; add the column then. Kit test cost_rows_reach_the_main_line fails here before and after (no costwatch module in this container): not this job's. Handover check COST flag: expected for a system job. Its RECORD flag on milburn (chat 5): the test pre-flight ran in a throwaway copy on purpose, so the real record has nothing; the flag firing is the check working. The saver missed 1 of Sam's messages in chat 4 (his Y to the three changes, 20 Nov): recorded here.



## Handover, Milburn lessons chat 1 (22 Nov)
- **Rules that bite next:** the proposal route (`source/propose.py`: pack, two helpers, blind judge, record, then Sam), 85 (cost watch), CLAUDE.md "Questions are numbered" (one judged lesson at a time, pick first).
- **Done (Milburn lessons chat 1, Opus high, 22 Nov):** Sam: "Milburn: begin all". The 8 parked lessons un-parked (Status lines). shared-check-fixes MERGED into named-lines (same cause: false lines that bury real faults; its problem, facts and chat version copied in; marked replaced:named-lines). guard-film-questions got the status chat's fact (the guard's blocked reply still reaches Sam, so he saw one message 3 times) and was re-packed. All 7 packed; 14 helpers started; the account's 5-hour limit stopped them at 17:20. Helper answers on disk (complete, each ends with its unchecked list): staging-stills A+B, notes-model A+B, rule-needs-check A+B, brow-limit A only, named-lines B only. None yet: could-not-test, guard-film-questions.
- **Next (chat 2, Opus high):** run the missing helpers with the exact lines `propose.py pack NAME` prints (no re-pack needed unless a problem file changed: could-not-test A+B, guard-film-questions A+B, brow-limit B, named-lines A); then `propose.py judge NAME` + one judge each, `record`, `show`. Bring Sam ONE judged lesson at a time, in plain words, numbered question, pick first, queue order: could-not-test, staging-stills, named-lines, guard-film-questions, notes-model, brow-limit, rule-needs-check (two small ones may share a message). Sam's 19 Nov words stand: no check deleted; "fix and test" for the guard; brow limit enforced by the kit; no rule without a working check. Builds on his picks may go to an Opus medium chat.
- **Needs Sam:** nothing until the first judged lesson.
- **Read:** this section; guides/job-packs.md "A tool job"; propose.py MAP.
- **Open rule requests:** none. Branches: claude/gta-chat31 filed as a record by the status chat (not merged: main line newer); claude/dreamy-fermi-vkhutz (source/gta_story_post.py, 2 h old) belongs to a running GTA chat: not this job's, left alone.
- **For Claude:** handover check flags: SENTENCE (CLAUDE.md "Choose views..." line reworded on 21 Nov in another chat, it still holds the words with a NEW-shot rider: not this job's) and COST (no estimate: expected for a system job). Status chat = session_01GznaATLDiLViEJgr9HLUfs (its other messages, Walliams, cost ideas, were answered there). Cost: red at 5.6% of a week (5.2 of it helpers), stopped by the account limit, so the chain could not open chat 2 itself; Sam starts it (another account).



# Archived 23 Nov (chain B chat 1)
## Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (propose.py: show, then Sam, then `mark`), 85 (cost watch), CLAUDE.md "Questions are numbered" (one judged lesson at a time, pick first).
- **Done (Milburn lessons chat 2, Opus high, 22 Nov, session_01U3pKQyM6KwJ9VCHUrPtX7S):** the 6 missing helpers ran on the existing packs (all still valid, no re-pack); all 7 judged and recorded (`propose.py show NAME` for each). could-not-test put to Sam (pick 1: test on Milburn first, then a stop no chat can skip plus automatic cover; 2: stop now). Picks: staging-stills helper A, could-not-test B; others in each file.
- **Next (chat 3 opened two chains, 22 Nov):** A) lesson 7 rule-needs-check: step 1 list (Sonnet) from notes/proposals/rule-needs-check/rule-list.html plus the six guides, then step 2 build (Opus high), step 3 shared with could-not-test. B) builds in queue order, one Opus-high chat each, each opening the next: staging-stills, named-lines, guard-film-questions, notes-model, brow-limit. EVERY chain ends with Sam's report (his ask, 22 Nov): each rule changed or added: what it said before, what it says now, the difference made (measured where possible, else 'not measured yet'), and how it should behave from now on. A scheduled task at 03:30 UK (23 Nov) wakes chat 3 to resume any chain stopped by usage running out.
- **Needs Sam:** nothing now. All 7 lessons adopted (option 1 each). Sam, 22 Nov ~23:10 UK: "Continue with 7. Please report back on all changes rules and what the difference you have made is, and how it should behave in the future. With all these jobs, please continue at 3:30 if usages runs out." Q2 (read the six guides too) unanswered: taken as my pick Y, told Sam with an Added line.
- **Read:** this section; guides/job-packs.md "A tool job"; propose.py MAP.
- **Open rule requests:** none. Branches: claude/gta-chat31 and claude/dreamy-fermi-vkhutz belong to the GTA chats (not this job's), left alone.
- **For Claude:** chat 3 end check named: branch claude/could-not-test-replay is the live could-not-test test chat's (it merges its own); SENTENCE 'Choose views the drawing can carry.' is still in CLAUDE.md, only split by bold marks and the 21 Nov 'new shot only' clause (false flag); COST: system job, no estimate (as chat 1). chat 3 start named, not this job's: watcher BROKEN 'saver missed 1 message' (20 Nov, an earlier chat's) and 'bench_move.py unwired' (bench-speedup build's own chat wires it). Handover check: UNROUTED entry 22:40 is a false block (could-not-test was judged; the guard wanted the other five Critiqued lines too); SENTENCE and COST as chat 1 (not this job's; no estimate for a system job). The Stop hook blocks a reply that names several touched proposals unless each one's Critiqued line is in it (it counts every proposal this turn recorded, not only the one asked): record the others in a turn that asks Sam nothing, so the guard does not show Sam a repeat (the guard-film-questions lesson itself). Helpers found: could-not-test overlaps named-lines (same code gap); Milburn cost 22% (app) vs 32.85% (ledger table), unchecked. Cost at handover: amber, 3.4% of a week (3.0 helpers).


## Archived 23 Nov (chain B chat 2 start)

<!-- archived 23 Nov, chain A chat 2 -->
## Where things stand (the ONE handover)
- **Rules that bite next:** CLAUDE.md "Rules are permanent" (rule wording shown first, then Sam's yes), the proposal route, 85 (cost watch).
- **Done (chain B chat 1, staging-stills, Opus high, 23 Nov, session_01U3pKR27nDhvqq7xXsinsRV):** step 1 look back (notes/proposals/staging-stills/learn.md: 5 staging repeats over 4 films, all built before a board; gate met); step 2 built: source/staging.py, wired into film_engine.render (clips) and rough.board_gate (animatic), `rough.py board --shots`, job pack "Notes round" line, watcher promise; kittests staging_stills_milburn_replay and staging_stills_note_finder pass. Report entry 1 in notes/proposals/lessons-report.md.
- **Done (chain A chat 1, Sonnet, 22 Nov):** lesson 7 step 1: `notes/proposals/rule-needs-check/rule-table.md` (103 rules + six guides + 65 notes sorted). The four numbers: by-hand/judge-not-run 9, did not fire 4, no rule 10, ran and missed 15 (13 of them GTA shot 4's body/car/arm checks); 22 notes were direction changes, 5 unplaced. 42 of 103 rules ever proved on a bad example; 29 guide rule lines have no check. Cost: about 40 steps; app figure not readable here, ledger has no estimate for a system job (unmeasured).
- **Next:** chain B chat 2 (Opus high): named-lines, opened by this chat with the same prompt. Then guard-film-questions, notes-model, brow-limit (that last chat sends Sam the whole lessons report).
- **Next:** chain A chat 2, Opus high: lesson 7 step 2 (rules as proven promises, worst first by rule-table.md's 'What step 2 should take first') and step 3 (fail closed; list_sessions first for the could-not-test chat so nothing is built twice). The LAST chat of chain A ends with Sam's report as a page or file (every rule changed or added: before, after, difference measured or 'not measured yet', future behaviour); any rule wording shown to Sam first. Chain B (builds in queue order) as before. 03:30 UK scheduled wake resumes stopped chains.
- **Needs Sam:** Q1 (asked 23 Nov): rule 11 and rule 87 wording for staging-stills (exact text in lessons-report.md entry 1). On Y, write both rows of guides/film-quality-rules.md (and their check columns) and mark the proposal file's last line done.
- **Read:** this section; guides/job-packs.md "A tool job"; the lesson's proposal "Final version".
- **Open rule requests:** rule 11 and 87 wording (Q1 above).
- **For Claude:** kittest dearest_things_named FAILS on the main line before this chat's work too (GTA ledger repeat flag; not this job's). Branches claude/gta-chat31 and claude/dreamy-fermi-vkhutz are GTA's, left alone; claude/could-not-test-replay is merged on the main line by its own chain (start listed it). Handover check: SENTENCE (CLAUDE.md wording, an earlier commit, not this job's) and COST (no estimate for a system job) named as chat 3; PUSH sent at handover. Chain A (rule-needs-check) and could-not-test run in their own sessions (list_sessions, 23 Nov): nothing built twice.



# Archived 23 Nov (could-not-test build chat)
## Where things stand (the ONE handover)
- **Rules that bite next:** CLAUDE.md "Rules are permanent" (wording to Sam first, his numbers), the proposal route (now fail closed), 30 (a repeat names the check that missed).
- **Done (chain B chat 2, named-lines, Opus high, 23 Nov, session_01U3pKQy7WWrKYXdcVwSbKkN):** the learning step (changes nothing): notes/proposals/named-lines/learn.md. Milburn's 61 named lines: 37 blind, 8 false (+60 removed in film code), 14 chosen, 2 unsettled, 0 real; 3 Sam notes were already a printed line; 10 check fixes sit in film code; kit tests 108/112 (round_page already repaired). Report entry 2 in notes/proposals/lessons-report.md. Chain B chat 1 (staging-stills): built, report entry 1.
- **Done (chain A chat 2, Opus high, 23 Nov, session_01U3pKQxaqn1gLmoGR6959hb):** lesson 7 step 2 framework and step 3 (my part); all in rule-needs-check.md "Built". 103 rules in source/rule_proofs.json: 34 proven, 10 partly, 5 judge, 26 next, 2 owed, 26 cannot yet. Gate on new rules (handover STOP; watcher RULES line). Rule 74 now asks every shot (proof: GTA note G4-16). Let-throughs block handover and finish.py until settled; a crashed handover check is a STOP.
- **Next (chain A):** chat 3, Opus high: step 2 worst first: rule 17 on Sam's v7 stills (find their times first; plan in its entry), 41's misses, 49 (M4), 13 (M6), 11 (M5), 89 (send gate), 30 (dearest_things_named red: GTA gun note no longer flagged); rule 19 once the could-not-test chat lands. Then, as the LAST chat of chain A: Sam's report page (rule-needs-check.md "For the report", measured against rule-table.md) with, in the same message, the CLAUDE.md wording (rule-needs-check.md "Wording for Sam") and the cannot-yet list (`ruleproofs.py sam`) as numbered questions.
- **Next (chain B, after Sam's yeses):** session_01U3pKQy7WWrKYXdcVwSbKkN builds each yes of named-lines (kittest + watcher promise each), then opens guard-film-questions (Opus high, same prompt), then notes-model, brow-limit (the last sends Sam the whole lessons report). Change 4's handover stop goes on chain A's gate, not beside it.
- **Needs Sam (chain B waits here):** named-lines Q1 change 2 + rule 59 wording, Q2 change 3, Q3 change 4 (exact text in lessons-report.md entry 2). Change 1 not asked: built once, by the could-not-test build chat (session_01U3pKQzaw3rkdJXunde285d). Staging-stills Q1 (rules 11, 87) still goes to session_01U3pKR27nDhvqq7xXsinsRV.
- **Read:** this section; guides/job-packs.md "A tool job"; the lesson's proposal "Final version" (named-lines: also learn.md "What the results decide"); chain A: rule-needs-check.md "Built", ruleproofs.py MAP.
- **Open rule requests:** rule 59 (named-lines Q1); rules 11 and 87 (staging-stills Q1); the CLAUDE.md line "No rule without a working check" (wording ready, not written).
- **For Claude:** chain B's let-through (chat 9c3f62f3, 03:34, staging-stills stale verdict) refuses every finish.py run until settled (`propose.py settle 9c3f62f3 ...`). named-lines: the one switch is film_engine.lock_fault's faults_named plus finish.py --faults-named and preflight's critique gate (line 593); records go in waivers.py's exceptions table (add a kind column; blind refused); change 3 starts in the places and moves kits and milburn_voice's cleaned takes. Kittests red before both chains: dearest_things_named (rule 30), claude_md_sentences_never_lost (CLAUDE.md headings reworded by Sam's 21-22 Nov statements; also handover SENTENCE x3); body_check_* need the makehuman clone (blocked in this container). COST: no estimate for a system job. Branches claude/gta-chat31, claude/dreamy-fermi-vkhutz: GTA's, left alone.



## Replaced 23 Nov by chain A chat 3
- **Done (chain A chat 2, Opus high, 23 Nov, session_01U3pKQxaqn1gLmoGR6959hb):** lesson 7 step 2 framework and step 3 (my part); all in rule-needs-check.md "Built". 103 rules in source/rule_proofs.json: 34 proven, 10 partly, 5 judge, 26 next, 2 owed, 26 cannot yet. Gate on new rules (handover STOP; watcher RULES line). Rule 74 now asks every shot (proof: GTA note G4-16). Let-throughs block handover and finish.py until settled; a crashed handover check is a STOP.
- **Next (chain A):** chat 3, Opus high: step 2 worst first: rule 17 on Sam's v7 stills (find their times first; plan in its entry), 41's misses, 49 (M4), 13 (M6), 11 (M5), 89 (send gate), 30 (dearest_things_named red: GTA gun note no longer flagged); rule 19: could-not-test has landed (23 Nov), use cover.py. Then, as the LAST chat of chain A: Sam's report page (rule-needs-check.md "For the report", measured against rule-table.md) with, in the same message, the CLAUDE.md wording (rule-needs-check.md "Wording for Sam") and the cannot-yet list (`ruleproofs.py sam`) as numbered questions.


# Archived 23 Nov (chain A chat 4)
## Where things stand (the ONE handover)
- **Rules that bite next:** CLAUDE.md "Rules are permanent" (wording to Sam first, his numbers), the proposal route (now fail closed), 30 (a repeat names the check that missed).
- **Done (chain B chat 2, named-lines, Opus high, 23 Nov, session_01U3pKQy7WWrKYXdcVwSbKkN):** learning step (notes/proposals/named-lines/learn.md); Sam Y Y Y; change 2 BUILT: each warning its own answer in the notes' "## Exceptions" (waivers.split/todo/release), wired into pre-flight's stamp, film_engine lock and picture-check hold, humancheck finish/name (GTA, gta_rehearse, bench_move pass their notes), finish.py Hook Text and readable; --faults-named passes no list (critique gate, rule 89, unchanged); rule 59 wording written; kittests named_lines_each_answered, named_lines_body_each_answered, render_lock updated; watcher promise waivers.py. Report entry 2 updated.
- **Done (could-not-test build, Opus high, 23 Nov, session_01U3pKQzaw3rkdJXunde285d):** Sam's pick 1 built and tested, all three: cover.py feeds the clipping check from the drawing (each places piece, each arm at its pose depth); COULD NOT TEST in the pre-flight stamp, refused by the render tool and finish.py before --faults-named (only an Exceptions row with Sam's Y); the render keeps each frame's text/KEEP_CLEAR boxes, finish.py measures captions and Hook Text on them. Replay beat both numbers, 0 false alarms (notes/proposals/could-not-test/test.md "The build", change list there). Sam's report sent. Chain ends here.
- **Done (chain A chat 3, Opus high, 23 Nov):** step 2 worst first, each proof a kittest on the saved example (rule_proofs.json updated): 49 dome_not_a_carrot (M4; facehouse.dome_faults, red on the pick sheet), 13 mouth_name_that_does_not_exist_stops (M6), 11 board_gate_milburn_reverse (M5, Milburn's real board record), 19 could_not_test_cover/readable (M19, the build landed), 17 solid_check_shot4_v7 (G7-3 on v7 frames 12/18; partly: bonnet G7-2 and water G7-7 still pass, measured), 89 body_send_gate (videos; partly: stills not gated). 41 measured on v4 at Sam's stills (clip time - 3.0): 1.00 s and 4.92 s pass with no Jason fault (miss kept, plan in entry). Now 37 proven, 9 partly, 26 cannot yet. The start STOP (4 BROKEN: 62, 70, 30, W8) was stale: all three kittests pass. Sam's report page published: https://claude.ai/artifact/GvxQmawCmy9vyZGKc65N13 (source notes/proposals/rule-needs-check/report.html). CHAIN A ENDS HERE.
- **Chat 3 end check named:** SENTENCE x3 (in CLAUDE.md, split by bold marks or reworded by Sam's 21-22 Nov statements: false flag, as before); COST (system job, no estimate); PUSH (sent at the end).
- **Sam's answers (23 Nov ~05:50 UTC, "Y to all"):** Q1 Y: CLAUDE.md "No rule without a working check" written with rule_proofs N25 and the rulebook's last table (one commit). Q2 2a: the plain-check proposal, option 1 (Step 0 learn + Change 1; Changes 2 and 3 keep their own conditions). Let-through 9158c1df settled (routed: the Q1 ask missed its Critiqued line). Sam: "Continue all working chats at 8:35" (UK = 08:35 UTC): one-shot wakes set.
- **Next (chain A):** chat 4, Opus high, opened idle and woken at 08:35 UK: plain-check option 1 (notes/proposals/plain-check.md "Final version"): Step 0 (the two checkers on paper, tested on Sam's 19 Nov messages), then Change 1 (judge.md "For Sam" as fixed fields through the lock; parser refuses a missing field; record refuses without the reader's pass), each with its kittest and rule_proofs entries (W1-W5, W7, W9, N1, N8, N11-N15 move from cannot yet as each is proven). After it: 41 (curled limbs, flat legs, v4 1.00/3.12/4.92 s), 17 (bonnet, water), 5 (wire bench_move).
- **Next (chain B):** chat 3, Opus high (opened by chat 2): named-lines part 2 = change 3 (shared inputs: places/moves kits hand scene(t), layers, facing, on=, cam_for, separate rooms; voices reads the cleaned takes the film plays; the "move to shared" handover stop for film-code check fixes) and change 4 (a kittest red at two handovers in a row, or unable to run, stops the handover; on chain A's gate). Then guard-film-questions, notes-model, brow-limit (the last sends Sam the whole lessons report).
- **Needs Sam (chain B):** Q1 (asked 23 Nov): the "every rule and fix is for all films" wording (Sam's 23 Nov words; exact text in chain B chat 2's reply and lessons-report.md entry 2); his Y comes to session_01U3pKQy7WWrKYXdcVwSbKkN or chat 3, which writes it in CLAUDE.md "Rules are permanent". Staging-stills Q1 (rules 11, 87) still goes to session_01U3pKR27nDhvqq7xXsinsRV.
- **Read:** this section; guides/job-packs.md "A tool job"; the lesson's proposal "Final version" (named-lines: also learn.md "What the results decide"); chain A: rule-needs-check/built.md, ruleproofs.py MAP.
- **Open rule requests:** "every rule and fix is for all films" (Sam 23 Nov, chain B Q1); rules 11 and 87 (staging-stills Q1); none for chain A (the CLAUDE.md line is written).
- **For Claude:** could-not-test: GTA is on preflight.COVER_BEFORE (its people have no depth) until its chat wraps them in cover.person; first render after this re-draws cached frames once (each needs its .read.json). Kit tests red: claude_md_sentences_never_lost only (dearest_things_named fixed by chain A chat 2: the repeat finder reads archived notes). Build chat end check named: QUICK CHECK and RECORD satire_template (a smoke run of pre-flight on the template, not a film: refused at its gate as a template is); SENTENCE x3 (the sentences are in CLAUDE.md, split by bold marks: false flag, as chat 1); COST (system job, no estimate); RULE 30: fixed since (chain A chat 2). chain B's let-through (chat 9c3f62f3, 03:34, staging-stills stale verdict) refuses every finish.py run until settled (`propose.py settle 9c3f62f3 ...`). named-lines: the one switch is film_engine.lock_fault's faults_named plus finish.py --faults-named and preflight's critique gate (line 593); records go in waivers.py's exceptions table (add a kind column; blind refused); change 3 starts in the places and moves kits and milburn_voice's cleaned takes. Kittests red before both chains: claude_md_sentences_never_lost (CLAUDE.md headings reworded by Sam's 21-22 Nov statements; also handover SENTENCE x3); body_check_* need the makehuman clone (blocked in this container). COST: no estimate for a system job. Branches claude/gta-chat31, claude/dreamy-fermi-vkhutz: GTA's, left alone. Chain B chat 2 end check: QUICK CHECK lines on grand_theft_autism and gta_rehearse (no brief checklist, board, HOOK, KEEP_CLEAR, SHOT_MARKS) are GTA's own older gaps, shown only because chat 2 changed one line in each (the body check reads GTA's notes): GTA's chats own them, and change 3's move-to-shared stop should catch a film with its own renderer. Kittests run for chat 2's change: named_lines x2, render_lock, could_not_test x2, body x5 all PASS; the full suite not re-run (amber).


## Archived 23 Nov (chain A chat 6 took over)
- **Rules that bite next:** CLAUDE.md "Statement Two" (say "can't yet" rather than build a check that only looks like it works), "Rules are permanent" (wording to Sam first), 30 (a repeat names the check that missed).
- **Done (chain A chat 4, Opus high, 23 Nov, session_01U3pKQyAtuihjk78U16wCxZ):** plain-check Step 0 (changes nothing): checker A (fixed fields + code names) and the blind reader (3 versions) on 25 saved messages. Nothing met the bar: A and every reader fail all 7 asks Sam was happy with too; the good asks hold as many unexplained coined phrases (6-15) as the confusing ones (7-11). Numbers and why: notes/proposals/plain-check/step0/learn.md. Built, not wired: propose.shape_faults / code_names / reader_verdict / sam_words; guides/proposal-route/reader.md (not in the lock yet). rule_proofs: nothing moves (no check proven).
- **Sam's answer (23 Nov, Q1 = 2):** build Change 1 with the fixed fields only; the reader (C3) is advice to the writer, never a gate (record does NOT refuse without its pass). Was: build Change 1 with the reader as a gate that holds every ask until each coined phrase is explained (asks get longer) = 1 (my pick); or the fixed fields only, reader as advice = 2. Critiqued: 7 found, 3 fixed, 4 named.
- **Next (chain A):** chat 5 (Opus high, opened by chat 4): rule 41 (curled limbs, flat legs, v4 1.00/3.12/4.92 s), 17 (bonnet G7-2, water G7-7), 5 (wire bench_move or name it in watcher OFF). Sam's Q1 answer comes back to chat 4, which opens the Change 1 build (Opus medium: plan is clear): judge.md For Sam as fields through the lock (add reader.md to PROMPT_FILES, `propose.py lock --verdict plain-check`); parse(fields) for new verdicts only (state shape 2; old verdicts parse as before, or every old proposal breaks); show in field order; record refuses a verdict whose For Sam lacks a field (no reader gate, Sam's 2); `propose.py reader NAME` packs the C3 reader as advice (its unexplained phrases printed for the writer to explain); review's lessons through `propose.py plain`; kittests: Milburn lessons must-fail, a field-shaped ask passes, reader_verdict on the saved reader3 files, proposal_route_hook fixture updated; rulebook row names the check; rule_proofs N8/W2 move only then.
- **Done (chain B chat 2, named-lines, Opus high, 23 Nov, session_01U3pKQy7WWrKYXdcVwSbKkN):** learn step (named-lines/learn.md); Sam Y Y Y; change 2 BUILT (each warning its own written answer in the notes' "## Exceptions"; no switch passes a list: pre-flight, render, body check, finish.py; rule 59 wording written; kittests named_lines_each_answered, named_lines_body_each_answered; watcher promise waivers.py). Sam's Y ("needs testing") to "Every rule and fix is for all films": written in CLAUDE.md, the rulebook's last table, rule_proofs N26 (owed). Report entry 2.
- **Next (chain B):** chat 3 (Opus high, running, session_01U3pKR2taFPq31QroZMAKSe): named-lines changes 3 (shared inputs + the move-to-shared handover stop, whose kittest must catch Blessed's 7 film-code check fixes, Milburn's voice takes, GTA's solids: N26's test) and 4 (kit test red at two handovers stops it), then opens guard-film-questions; then notes-model, brow-limit (the last sends Sam the whole lessons report). Staging-stills Q1 (rules 11, 87) still goes to session_01U3pKR27nDhvqq7xXsinsRV.
- **Read:** this section; guides/job-packs.md "A tool job"; plain-check/step0/learn.md; plain-check.md "Final version".
- **Open rule requests:** none new.
- **For Claude:** chain B: named-lines Q1-Q3 and the all-films rule answered (see chain B lines); staging-stills Q1 waits on Sam; let-through 9c3f62f3 still to settle. Kit tests red before this chat: claude_md_sentences_never_lost; body_check_* (makehuman clone). Step 0 readers ran as general-purpose Sonnet (no reader agent type yet); 19 Nov cse_ chats unreadable from this account. Branches claude/gta-chat31, claude/dreamy-fermi-vkhutz, claude/gta-chat46-build: GTA's (another account's chats), left alone. End check named: SENTENCE x3 (CLAUDE.md headings reworded by Sam 21-22 Nov: false flag, as chats 1-3); COST (system job, no estimate); PUSH (sent at the end).

## archived by chain B chat 3 (23 Nov)
- **Done (chain B chat 2, named-lines, Opus high, 23 Nov, session_01U3pKQy7WWrKYXdcVwSbKkN):** learn step (named-lines/learn.md); Sam Y Y Y; change 2 BUILT (each warning its own written answer in the notes' "## Exceptions"; no switch passes a list: pre-flight, render, body check, finish.py; rule 59 wording written; kittests named_lines_each_answered, named_lines_body_each_answered; watcher promise waivers.py). Sam's Y ("needs testing") to "Every rule and fix is for all films": written in CLAUDE.md, the rulebook's last table, rule_proofs N26 (owed). Report entry 2.


# Archived 23 Nov (chain A chat 5 start)
## Where things stand (the ONE handover)
- **Rules that bite next:** CLAUDE.md "Statement Two" (the reader is advice: never claim it proves plain words), "No rule without a working check" (N8/W2 only partly: system asks), 30 (a repeat names the check that missed).
- **Done (chain B chat 3, named-lines part 2, Opus high, 23 Nov, session_01U3pKR2taFPq31QroZMAKSe):** change 3 BUILT: kitinputs.py (the kits hand every check its inputs from the drawing: roster, pop-ins, cameras, facings, measured camera, words, sizes, line subjects, hems; depth from drawn size in cover.py), takes.py (Milburn's take cleaning shared; voices.py reads the registered take, flags a raw read), plan.py (places apart, flat floors, pitch, module SHOT_MARKS), the move-to-shared STOP in handover.py end. Change 4 BUILT: kittest_gate_faults (red at two handovers or could not run = STOP; notes/logs/kittest-reds.log), on chain A's gate. Milburn replay: 68 -> 36 lines, blind 37 -> 6 (named), false plan 8 -> 0, voice 0 false (85 raw). Kittests: named_lines_shared_inputs_milburn, move_to_shared_catches_film_fixes, kittest_red_twice_stops_handover, plan_places_apart_and_flat_floors, takes_cleaned_and_registered (all PASS); claude_md_sentences_never_lost fixed (sentences.SAM_REWORDED). Watcher promises: kitinputs.py, takes.py. Report entry 2 updated.
- **Done (chain A chat 6, Opus medium, 23 Nov, session_01U3pKR2YBAWAT7MzS7D1T9N):** plain-check Change 1 built with Sam's answer 2. judge.md For Sam = fixed fields (Problem, numbered steps, Why, You'd notice, Other option, Lost, Added; no code names), reader.md added to the lock, locked under --verdict plain-check. pack marks state shape 2; parse refuses a shape-2 option failing shape_faults (old verdicts parse as shape 1: status unchanged); show prints field_text in order; `propose.py reader NAME` packs the C3 reader (Sonnet) on show's text and prints its phrases, never blocks; `propose.py plain FILE` = checker A per item (Milburn review: 0 of 22 pass); review writes a fields-shaped Lessons section. Kittests plain_check_fields (new) and proposal_route_hook (fixture in fields; missing field and file name refused; mutation-checked) pass. Rulebook "Messages to me" row names the check. rule_proofs N8, W2 -> partly (system asks only): 38 proven, 11 partly, 24 cannot yet. plain-check marked adopted.
- **Next (chain A):** chat 5 (session_01U3pKR1Z6SWGi4RSahgw7hK, Opus high) carries the chain: rules 41, 17, 5. Change 1's number to beat: no "explain"/"don't understand" from Sam on the next 3 system asks (ledger search); then Change 2 (the hook asks for the shown option text) goes to Sam, its own yes. Every new ask: run `propose.py reader NAME` before sending and explain the phrases it lists.
- **Next (chain B):** chat 4, Opus high (opened by chat 3): guard-film-questions (notes/proposals/guard-film-questions.md "Final version", its own first step before any gate), then notes-model, brow-limit (the last sends Sam the whole lessons report as a plain page).
- **Needs Sam:** nothing for this job.
- **Read:** this section; guides/job-packs.md "A tool job".
- **Open rule requests:** none new.
- **Chat 3 (chain B) end check named:** BRANCH claude/gta-v5-sound-draft and the other gta branches: GTA's, left alone; SENTENCE x4 ("Locked by Sam", "Just go"): from other chats' CLAUDE.md commits 34f49840 and 0945cc85, not this chat (Sam's own rewordings are now known to sentences.SAM_REWORDED; these two were not checked against his words here); FREEZE 20->21: in the start-up kit run before this chat's edits (another chat's); COST: system job, no estimate; RECORD milburn: the replay runs on finished Milburn were taken out of its record on purpose (not a round of the film).
- **For Claude:** chain B chat 3: kitinputs.fill runs in preflight after install_probes (kf proxy passed to housestyle, plan, viewchecks, camfeel, linecheck, landmarks, sizes, cast_faults); the film's own inputs always win. Left blind on Milburn (named): 2b tiny figures (milburn_sets.field, not views.person: needs a kit far-figure piece), cameras for shots 3 and 6, audits (needs the render pass to keep each person's drawing). Not done: the full kittest suite re-run (amber); the render's picture pass with kf (audits still the film's). The move-to-shared STOP reads source/ diffs since the last handover-end line of another chat; GTA's own renderer files count (gta = initials). staging-stills Q1 waits on Sam; let-through 9c3f62f3 still to settle. Kit tests red before: claude_md_sentences_never_lost; body_check_* (makehuman clone). No reader agent type yet (general-purpose Sonnet). Branches claude/gta-chat31, claude/dreamy-fermi-vkhutz, claude/gta-chat46-build: GTA's (another account's chats), left alone. plain-check's existing proposals are shape 1 (no fields), by design. End check named: SENTENCE x3 (CLAUDE.md headings reworded by Sam 21-22 Nov: false flag, as chats 1-5); COST (system job, no estimate); PUSH (sent at the end).

