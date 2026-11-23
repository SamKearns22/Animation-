
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

