# Helper B: a stopped kit-test run loses every result it had

## Leak
Yes: it quotes Sam's Y'd answer (per-run results, each written as it ends, restart re-runs only unfinished). Tested, not assumed.

## Results
- Runs lost part-way: Open Wounds chats 7 ("still going at handover") and 10 ("stopped mid-way"); the next chat reran everything (notes/archive/brexit-is-done-handovers.md lines 114, 173, checked).
- Refused handovers: 17 "STILL RUNNING" across 11 sessions; 4 "COULD NOT RUN" (no finished run), 23 Nov, 3 sessions (notes/logs/handover-end.log, checked).
- Finished results are wiped too: the problem file cites a green run at 13:03; at 13:27 the log held 123 of 145 results from a new run started about 13:11. watcher.py `kittests-bg` opens the log with "w" on every start (checked).
- That run was 18 minutes in and 22 tests short, so "about 15 minutes" is low on a busy machine; the 1800 s timeout would kill it with no verdict (watcher.py, checked).
- No `-u` or PYTHONUNBUFFERED in the launch (checked): up to about 8 KB of results sit unwritten; lines a kill loses: unchecked.
- Faults reaching Sam: none. Cost in % of a week: not in the ledger (a gap).

## The real decision
Not "add a resume log" but: what single record tells any chat, after any stop, which tests passed on the code it will hand over. Bigger lever: the adopted, unbuilt kit-tests-when change (Sam's pick 1, 25 Nov) already creates a per-test pass record with file stamps; a separate resume log would be a second record that can disagree.

## Root cause
The result is one text file whose verdict is its last line (kittests.py main prints the summary only at the end); the launcher overwrites it at every start; the gate (handover.py kittest_gate_faults) accepts nothing without that line. Any stop, timeout or new start destroys finished work.

## Approaches weighed
1. Sam's words as a standalone feature: a per-run log, skip tests listed. Risk: after a code change it skips tests that passed on old code, a false green.
2. Reframe: make the adopted per-test pass record the resume. Each result is flushed the moment its test ends, tied to the code it ran on; "unfinished" means "no result on current code", so stop, wipe and code change are one case.
3. Make runs too short to be stopped: run tests side by side across cores. A stop still loses everything.
4. Learn first: time each test, and for each stop record its cause (restart, timeout, chat end) and lines lost to buffering.

Chosen: 4, then 2, as the first piece of the kit-tests-when build.

## Proposal
**Learn (changes nothing; folds into kit-tests-when Step 0):** its traced full run also logs each test's time, and one run is killed on purpose mid-way to count lost lines.

**Change 1 (Sam's Y given):** kittests.py writes each result, flushed, as its test ends, into an append-only record keyed to the code (commit plus a hash of uncommitted changes). A new start resumes, running only tests with no result on current code. The gate accepts a full set on current code from any number of runs; "COULD NOT RUN" names the resume command. A kittest kills a run after N tests and checks a restart runs only the rest, then changes a file and checks old passes are not reused.
Numbers to beat: tests re-run after a stop on unchanged code, now 145, to 0; "COULD NOT RUN" after a stop, 4 on record, to 0.

**Change 2 (already adopted):** per-test file stamps replace the code key in the same record; no new yes.

**Timeout:** unchanged; resume makes a timeout cost only unfinished tests. Raised only if the learn step shows it bites.

**Cost:** about 0.5% of a week once, shared by all films (unchecked estimate); saves a 15 to 20 minute rerun per stop. Sam notices fewer stalled chats.

## Sam test
Q1: Yes: checkpointed results keyed to code are the expert standard.
Q2: Every handover on record (350 log lines), not one chat.
Q3: Root cause found (wipe plus end-only verdict); enforced in code and a kittest, not by choice.
Q4: Four different approaches weighed; the pick also avoids a second record.
Q5: Main risk, stale passes, closed by the key and tested; one-commit undo.
Q6: Facts sourced; the rest marked unchecked.
Q7: Not the cheap "skip what's listed" version, which would pass stale tests.
Q8: Permanent; reviewed at the film's end against both numbers.

## Lost / Added
Lost: the single overwritten log. Added: an append-only result record, resume on every start, one kittest.

## Unchecked
Cost of waits in % of a week; buffering loss; any timeout kill; who started the 13:11 run; the problem file's 146 PASS lines (log since overwritten).
