## Leak
The problem file states the answer Sam said Y to ("run only when a chat changed a shared tool, and before an animatic and a final; a film-only chat skips"). Judged below, not assumed.

## Results
- Handover refused "KIT TESTS STILL RUNNING" 15 times across 11 chats, 23-25 Nov; "COULD NOT RUN: no finished run" 4 more (notes/logs/handover-end.log).
- Handovers went out on runs that did not test the handed-over code: chat 7's run "still going at handover", chat 10's "stopped mid-way" (notes/archive/brexit-is-done-handovers.md 114, 173). Chat 13 re-ran tests by hand after its shared fixes (notes/brexit-is-done.md).
- The gate accepts any finished run on the machine, started at boot (handover.py kittest_gate_faults; setup.sh), so later changes go untested.
- kittests-last.log is not in git (git ls-files): every fresh machine re-proves code that already passed.
- Kit tests read film files: 33 paths into notes/, 11 into story/, 17 imports of film code (grep of source/kittests.py). A notes-only change (GTA's notes archived) turned move_to_shared_catches_film_fixes red (handover.py comment, line 480).
- A chain-B chat inherited chain A's red body_check_back_view via the main line, red at 4 handovers (kittest-reds.log; commit e822c8fb).
- Of 99 chats since 20 Nov, about 24-27 changed no shared code by path (git log by session trailer; my count, approximate).
- Cost of waiting in % of a week: not in the ledger (notes/ledger/brexit-is-done.md has no such line). Gap.

## The real decision
Not "which chats may skip" but: before a handover or render, has the exact code and data the tests read passed? The bigger lever is tying the gate to the code, not to the machine or the chat's edits.

## Root cause
The gate proves "a run finished on this machine", not "this code passed". So (1) every fresh machine re-runs and waits, because no passing result survives the chat; (2) a run started at boot can wave through code changed afterwards. Sam's rule fixes (1) only, and by the wrong test: "what this chat edited" misses film-file changes the tests read and shared changes merged in from other branches.

## Approaches weighed
1. Sam's rule by path (film files skip). Misses both cases above.
2. Reframe, chosen: record a fingerprint of every file the tests read with each green run, in git; skip only when nothing in it changed.
3. Make the run fast enough for every chat. Leaves the stale-run gap.
4. Run tests on GitHub after each push. Availability unchecked; reds land on the next chat.
5. Learn-first: measure before changing (below).

## Proposal
**Learn first (changes nothing, about 0.4% of a week):** one recorded full run on a fresh machine giving: the files the 141 tests read; run time; then replay the last 99 chats' changes to count, under approach 1 and 2, how many runs are skipped and whether any past red (the five in kittest-reds.log) would have been missed. Approach 2 must miss none; approach 1 is expected to miss at least the notes-archive red.

**Change 1 (own yes):** kittests.py writes a fingerprint of its read files with each run's result to a committed record. handover.py end: fingerprint matches a green record, pass with no run and no wait; else it needs a finished run on this fingerprint. Enforced by handover.py; a kit test replays the notes-archive and merged-branch cases. Number to beat: "STILL RUNNING" refusals on unchanged code from 15 to 0; reds missed: 0.

**Change 2 (own yes):** finish.py refuses an animatic or final unless the fingerprint has a green full run (Sam's "always before"). Override word still applies. Number: animatics sent on untested code, 0 (finish log).

**Change 3 (own yes, after 1):** setup.sh starts the boot run only when the fingerprint differs, keeping the early warning when it matters.

Cost: about 0.4 plus 1.5% of a week, once, shared by all films; nothing added per film against the 15%. The saving is mostly waiting time (tokens unchecked).

Sam would notice: chats touching nothing tested hand over without waiting.

## Sam test
Q1: Yes; build systems rerun tests by what they read.
Q2: 99 chats and every red on record.
Q3: Enforced by handover.py and finish.py; replayed cases prove it.
Q4: Five approaches; this fixes wait and stale run.
Q5: Each change undoable alone; replay first.
Q6: Sources named; estimates marked.
Q7: Stronger trigger over cheaper path rule.
Q8: Permanent; reviewed at film end.

## Lost / Added
Lost: the full run on every fresh machine when nothing it tests changed.
Added: a committed record of green runs; a run before every animatic and final; one kit test.

## Unchecked
Exact run time; % of a week spent waiting; exact count of film-only chats; whether tests read files outside git (e.g. downloaded models) that a fingerprint must also cover.
