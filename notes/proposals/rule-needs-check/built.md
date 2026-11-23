# rule-needs-check: what was built (moved out of the proposal file 23 Nov, chain A chat 3: the judge's verdict must stay the proposal file's last words)

## Built (chain A chat 2, 23 Nov, Opus high; steps 2 and 3)
**Step 2, rules as proven promises.**
- `source/rule_proofs.json`: all 103 rules (ids as rule-table.md), each with status proven / partly / judge / next /
  owed / cannot yet, its kittests, its saved example, and plan / owed / learn; rank = worst first. "By hand" is not a
  status. Today: 34 proven, 10 partly, 5 judge, 26 next, 2 owed (rule 5: solid-body-moves; rule 19: could-not-test),
  26 cannot yet. `python3 source/ruleproofs.py` (summary), `faults` (the gate), `sam` (Sam's list).
- The gate: `handover.py end` runs `rule_faults`: a new rulebook row or a new CLAUDE.md rule (bold phrase or heading
  not in the 23 Nov baseline) with no entry and saved example is a STOP. The watcher runs the same check every Stop and
  prints one RULES line at every chat start; a proven rule whose kittest fails is shown as BROKEN (4 found at once:
  rules 62, 70, W8 (the finish tests, fixed: they now use their own empty proposal log) and 30 (dearest_things_named:
  the GTA gun note is no longer flagged as a repeat; not fixed here, on the list)). kittest `rule_proofs_gate`.
- New proof, worst first: rule 74 (by hand, 4 notes): pre-flight now asks for acting rows for EVERY shot with someone
  in it, as the rule has said since 20 Nov (before: one row per spoken line, so GTA shot 4 had none: note G4-16).
  kittest `acting_rows_every_shot` on GTA's notes before and after chat 17. Warns on old films, refuses on new.
- Rule 17 (ran and missed, 5 notes): not built. Measured: today's body-through-solid check on the whole of v7's shot 4
  takes over 8 minutes even at every 6th frame; the proof must first find the time of each of Sam's v7 stills. Plan in
  its entry.
**Step 3, fail closed (my part; the COULD NOT TEST stop is the could-not-test build chat's, not built here).**
- A let-through of the proposal guard's second try now blocks: `handover.py end` lists it as STOP (never cleared by
  naming it in the notes) and `finish.py` refuses every animatic and final while any let-through since 23 Nov is
  unsettled, with no `--faults-named` way past. Settle: `propose.py settle CHAT8 "routed: NAME"` or
  `"false block: why"` (false blocks kept for the end-of-film review). First one caught at once: chat 9c3f62f3,
  03:34 (staging-stills verdict stale): chain B must settle it before any animatic.
- A handover check that crashes is a STOP ("CHECK COULD NOT RUN"), not a skipped line. `handover.py end` writes
  REFUSED in the end log when STOP lines remain, and the next chat's `start` prints STOP on it.

**Chat 3 (23 Nov, Opus high):** proofs added for 49, 13, 11, 19, 17 (partly), 89 (partly); 41 measured, misses kept. Report sent as a page (report.html beside this file). Numbers: 42 rules with a proof at step 1, 37 proven + 9 partly after the strict re-check; of the 38 rule-covered notes, caught on their own saved example: 4 before chain A (G4-7, G7-1, G7-4, G8), 10 now (+G4-16, M4, M5, M6, M19, G7-3).
**For the report (Sam's ask, 22 Nov ~23:10), so far:** rule 74 (before: a row per spoken line; now: every shot; GTA's
shot 4 would have been caught before Sam saw it: note G4-16, 1 of the 9 by-hand notes); the proposal route (before: a
let-through was logged and listed; now: it stops the handover and every animatic until settled: 39 let-throughs in a
week before; measured at the next film's end); the handover check (before: any fault could be "written in the notes";
now: STOP lines cannot); "no rule without a working check" (new; gate on). Not measured yet: notes on rule-covered
faults on the next film (Milburn 38 of 65 notes, from step 1), at that film's end.

**Wording for Sam (not written yet; needs his number):** CLAUDE.md, "Rules are permanent", a new bullet after "New
rules and lessons are proposed first": "- **No rule without a working check** (Sam's Y, 22 Nov): a rule counts only
when its check has caught a saved example of its own fault (a still, my words or a message); "by hand" is not a
check. A new rule comes with its example or the handover is refused; a rule whose check can't be built yet is listed
for me with what must be learned first." On his Y, add its entry (anchor "No rule without a working check", example:
step 1's 61 unproven rules) in the same commit, or the gate refuses the handover.
