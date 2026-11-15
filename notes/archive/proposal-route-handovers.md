
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

