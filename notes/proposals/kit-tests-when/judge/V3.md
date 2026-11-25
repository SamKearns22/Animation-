# Helper A: when the kit tests run

## Leak
The problem file carries a solution Sam said Y to ("run only when a chat changed a shared tool, and before an animatic and a final"). I set it aside and tested it.

## Results
- Waits: the handover check refused with "KIT TESTS STILL RUNNING" 15 times in 11 chats from 23 to 25 Nov (notes/logs/handover-end.log). From first refusal to accepted end: 9 to 12 min where nothing else blocked (00:23 to 00:32, 21:02 to 21:14).
- Crashes: "KIT TEST COULD NOT RUN" 10 times (kit_people_never_generic, womens_builds; same log). Some tests break on some machines, whatever the chat changed.
- Reds carried between chats: body_check_back_view red at 4 handovers in a row, tools_switched_on at 2 (notes/logs/kittest-reds.log). The run does catch faults one chat leaves for the next.
- The run checks the wrong code. setup.sh starts it at chat start, so it tests the code the chat inherited, not the chat's own changes. The handover gate (handover.py kittest_gate_faults) only reads that start-up log. Chat 13 re-ran tests by hand after its shared fixes (notes/brexit-is-done.md line 54). Chats 7 and 10 never got a full run on their final code (notes/archive/brexit-is-done-handovers.md lines 114, 173).
- "Film-only" is not safe. 14 of the 141 tests import film code (brexit_is_done_action, gta_cast, milburn and others; source/kittests.py lines 4912, 4937, 855, 4733). A chat that changes only its film's files can still turn a kit test red. Under the Y'd wording, that red would wait until the animatic.
- Cost: Open Wounds has spent 27.89% over 12 chats, about 2.3% each (notes/ledger/brexit-is-done.md). The test run itself costs nothing, because it runs in the background. The cost is in the waiting and re-tried handovers: unchecked, roughly 0.05 to 0.1% a chat. "Tool search" alone takes 14 to 24% of each chat (same ledger), which is a much bigger lever.
- Not on record: how many chats changed only film files. Commit counts suggest few: 203 of 250 commits that touched code since 18 Nov touched shared code (git log, my own film-prefix list, approximate).

## The real decision
The question is not "every chat or key stages". It is: **which version of the code has a test result, and does every animatic and final stand on a tested version?** The answer applies across the whole film and all its chats. Today the timing is wrong both ways. Chats wait for a test of code they did not write, while their own changes go untested.

## Root cause
The result is tied to a machine and a chat (a log written at start-up) when it should be tied to the code it tested. So every fresh machine runs everything again, even if nothing changed. And a chat's own changes are never tested unless someone remembers to re-run by hand.

## Approaches weighed
1. Sam's Y as worded: run when shared files changed, plus before animatic and final. This uses a folder rule, misses the 14 tests that read film code, and still waits at handover.
2. Reframe: a run is valid for exactly the files it read. Each run records every file it read, with a fingerprint of each. A new run is needed only when one of those files has changed. The check happens at handover, on the chat's final code, and finish.py refuses an animatic or final made on untested code.
3. Choose tests by hand: a table of which tests cover which tool. Quick, but it decays as tools are added.
4. Learn first: measure which chats changed what, and which reds came from whom, before changing anything.

I choose 2. It tests the right code, never waits when nothing the tests read has changed, and needs no list kept by hand. The learning in 4 is largely done above. What remains is folded into 2's own record.

## Proposal
**Learned (already, above):** the waits, the crashes, the wrong-code timing and the 14 film-reading tests.
**Change 1 (one change):**
- kittests.py records every module and data file each run opens, using Python's own import list and file-open hook, with a fingerprint of each. It saves this, with the run's reds, to a committed record.
- `handover.py end` re-runs only if a file in that record changed. It runs on the chat's final code and keeps the rule that a test red twice in a row stops the handover.
- setup.sh stops starting a run.
- finish.py refuses an animatic or final unless the current code has a recorded run with no stopping reds. "Override" still applies, through the existing override.refuse.

Enforced in code, not by a chat reading a rule. It inherits the crash rule, so the 10 crashes still stop a handover. Fixing the crashing tests is a separate later change with its own evidence.
**Numbers to beat:**
1. "STILL RUNNING" refusals: 15 in 11 chats, target 0 in chats whose files are unchanged.
2. Animatics and finals made on untested code: chats 7 and 10, target 0 (finish.py log).
3. Kit-test reds first seen by a later chat: 2 cases above, target 0 (kittest-reds.log).

All are measured at the end-of-film review.
**Cost:** a one-time build of about 1 to 1.5% of a week, done in a building chat (Opus). After that, about nil per chat and some savings. Within 15% a film.
**What Sam would notice:** fewer chats stalling at the handover, and an animatic is never made on code that hasn't been tested.

## Sam test
Q1 Expert: tying a test result to the exact files it covers is standard practice for avoiding repeat test runs.
Q2 Best result: the decision is judged across the whole film's chats, on the log, the reds log and the ledger, not one chat.
Q3 Comprehensive: the root cause (a result tied to a machine, not to code) is named and fixed. It is enforced in handover.py and finish.py, with three numbers to measure it by.
Q4 Most intelligent: four different approaches were weighed. This is the only one that both cuts the waits and tests each chat's own changes.
Q5 Risk: if a file read isn't recorded, it would wrongly skip a run. To guard against that, the record covers every module and file opened, and the check fails shut if the record is missing. It can be undone in one commit.
Q6 Checked: sources are named for each fact. The cost per chat is marked unchecked.
Q7 Not cheap: it adds tests where the cheap rule skips them (the film-code tests, each chat's own changes).
Q8 Nothing temporary: a permanent change, reviewed against the film's results when it ends.

## Lost / Added
Lost: the run at every start-up (only an exact repeat of a recorded run is skipped).
Added: a test run on each chat's own final code; a refusal in finish.py when the code is untested; a committed record of each run.

## Unchecked
- Wait cost in % of a week.
- How many chats changed only film files.
- Whether the tests read files the import list and file-open hook would miss (for example, files read by subprocesses the tests start).
