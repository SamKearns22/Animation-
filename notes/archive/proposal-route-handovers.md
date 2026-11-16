
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

