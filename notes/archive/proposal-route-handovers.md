
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

