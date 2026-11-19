# Proposal: Record what every check catches, so retiring a check is decided on evidence

Status: open

## Problem
Sam's rule is to remove a step only if it caught nothing in three films, with his Y. That cannot be followed: there
is no usable record of what each check has caught, in which film, and whether Sam would have seen the fault if the
check had not been there. Without it, checks that never catch anything keep costing every chat, and a check that
saves Sam a note could be retired by mistake. Another job (job 1) is surveying every stage to propose what to
retire, and will need this record.

## Facts
- CLAUDE.md: "remove a step only if it caught nothing in three films, with my Y on a 'Lost:' line."
- Every film ledger's per-check field "checks" is empty: {} in all 27 notes/ledger/*.json (counted 19 Nov,
  including milburn, protest-tiers, blessed).
- A per-check counter exists: source/ledger.py record() (lines 105-126), called by source/report.py:68 for every
  check, counts runs, faults and fault kinds per check. It only works while a round is open: current() reads
  notes/ledger/.current, written only by `ledger.py round FILM N` (ledger.py ~line 890). That file is absent in a
  fresh copy (checked 19 Nov: not on GitHub), so in every new chat (each a fresh container) the counter silently
  saves nothing. Milburn had 0 rounds (milburn.md).
- "quick_checks" (source/handover.py:390-395) stores only a fault total per run, no check names: Milburn 14 runs
  (8, 4, 4, 1, 1, 0, 13, 13, 13, 13, 11, 11, 48, 48); Protest Tiers 13 runs.
- Critique passes (rule 89's fresh-eye critic) are recorded with their fault text: Milburn 6, Protest Tiers 8,
  Blessed 7, remakes_sets 9 (ledger "critique"); round files notes/ledger/milburn/round-1.txt, round-2.txt hold text.
- Chat rows carry "notes" and "repeats" (Sam's notes and repeated notes per chat); Milburn: 0 notes, 0 rounds.
- Nothing records whether a fault a check caught would have reached Sam, or which of Sam's notes a check should
  have caught (a miss).
- Checks in source/: checks.py, clipcheck, handcheck, hookcheck, kitchecks, kittests, linecheck, lookbook_check,
  musiccheck, nametest, posecheck, setcheck, viewchecks, blessed_checks, preflight.py, handover.py's quick checks.
  No "checktests" file found.
- Job 1 (surveying every stage, proposing what to retire): no proposal file in notes/proposals/ yet (checked
  19 Nov ~17:30 UTC on the main line).

## Record
notes/ledger/milburn.json
notes/ledger/milburn/round-1.txt
notes/ledger/protest-tiers.json
source/ledger.py
source/report.py
source/handover.py
source/preflight.py
source/checks.py
guides/film-quality-rules.md
notes/proposals/late-faults.md
