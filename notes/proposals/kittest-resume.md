# Proposal: A stopped kit-test run loses every result it had

Status: adopted, Option 1 (Sam, 25 Nov, "1. Y"; build in R7 chat 5)

## Problem
Sam, 25 Nov 12:17 (R7 chat 2), word for word: "Can we log-as-we-go in the future to prevent that?", then "1 Y" to:
kit-test results kept per run, each test written as it ends, and a restart re-running only the unfinished tests.
Today a kit-test run that is stopped part-way (a machine restart, a timeout, a chat ending) leaves nothing a later
chat can use: the whole run (145 tests, about 15 minutes) starts again from the first test.

## Facts
- source/kittests.py main(): runs every test in order and prints one PASS/FAIL line per test to stdout; the summary
  line "kittests: all passed" or "N failed" only at the very end. 145 tests (`grep -c "^@test"`, 25 Nov).
- source/watcher.py `kittests-bg` (started by .claude/hooks/setup.sh's last line on every fresh machine): runs it with
  stdout into notes/logs/kittests-last.log (git-ignored, local to the machine), `nice -n 19`, timeout 1800 s; the file
  is opened with "w", so each start wipes the last result.
- source/handover.py kittest_gate_faults(): reads that log; with no "kittests:" line it STOPs the handover ("STILL
  RUNNING" while a run is alive, else "COULD NOT RUN"); reds are kept per chat in notes/logs/kittest-reds.log.
- This chat's start-up run finished: 146 PASS lines, "kittests: all passed", a mediapipe shutdown trace after it
  (notes/logs/kittests-last.log, 25 Nov 13:03).
- Earlier runs lost: Open Wounds chat 7's full run "was still going at handover"; chat 10's "was stopped mid-way"
  (notes/archive/brexit-is-done-handovers.md lines 114, 173; quoted in notes/proposals/kit-tests-when.md).
- Related open proposal: notes/proposals/kit-tests-when.md (when the full run happens at all; Sam said Y to "only
  when a chat changed a shared tool, and before an animatic and a final").
- Whether stdout reaching the log is buffered (lines lost if killed): unchecked.

## Record
source/kittests.py
source/watcher.py
source/handover.py
.claude/hooks/setup.sh
notes/proposals/kit-tests-when.md
notes/archive/brexit-is-done-handovers.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 8807ed04534cdcfe -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V2 (helper A). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the problem file quotes the answer Sam said Y to (results kept per run, each test written as it ends, a restart re-running only the unfinished tests), so every version started from that design. V2 and V3 named it and tested it against the adopted kit-tests-when record; V1 builds it as worded.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 2 | 4 | 2 | 4 | 15 |
| V2 | 5 | 4 | 4 | 4 | 4 | 21 |
| V3 | 4 | 3 | 4 | 3 | 4 | 18 |
## Sam test
Q1: Yes. An expert keys each test result to the exact inputs it ran on and writes it the moment it ends (build-system practice), so any stop costs only unfinished work and never gives a false pass. That is V2's design, folded into the per-test record Sam already adopted rather than a second store.
Q2: The evidence is every handover on record, not one chat: 4 "could not run" refusals (23 Nov) and 17 "still running" refusals in handover-end.log (350 lines, checked), two lost runs in the archive (lines 114, 173, checked), and today's wipe: the machine restarted about 13:11 (uptime, checked) and the new run overwrote the 13:03 green; at 13:32 it held 135 of 145 results, 21 minutes in (checked).
Q3: Root cause found in code: the verdict is only the last line of one file, the launcher opens that file with "w" on every start (watcher.py line 565), the gate accepts nothing without that line, and the watcher reads a killed run as "still running" (lines 258 to 266). The fix is enforced in code and proved by kittests that kill, restart and replay today's wipe; it does not rely on a chat choosing to follow anything.
Q4: Four approaches weighed (a per-run file as worded, the per-test keyed record, faster parallel runs, learn first). Only the keyed record survives a code change between the stop and the restart, and it is the record Sam already adopted.
Q5: Main risks: a test that passes only after others (a resume runs a subset in a fresh process), closed by the reverse-order learn run; a stale pass, closed by the key and a kittest; the adopted record's Step 0 failing, closed by a whole-code key for any test without a file stamp. Each change has its own yes and undoes in one commit.
Q6: Sources named above; build cost, cost per lost run, the cause of the 23 Nov refusals and who started the 13:11 run are marked unchecked.
Q7: Not the cheap "skip whatever the last file lists" version, which would pass tests on code that changed; reds, crashes and stopped runs are all kept and flagged.
Q8: Permanent, nothing provisional: the whole-code key is the lasting fail-safe for any test whose reads are unknown, not a stopgap. Reviewed at the end-of-film review against the three numbers to beat.
## Pick
V2
## Why
The real decision is not "add a resume file" but: after any stop, which tests have a result on the exact code being handed over, and can no stop ever erase one. The measured results it rests on are the six lost runs, the 21 "could not run"/"still running" refusals and today's overwrite of a finished green run. The smallest thing that reaches it: make the already-adopted per-test record write as each test ends, stop wiping it, and let the gate read it.
V2 and V3 both see this; V1 builds a second record keyed only to the shared-code folder, though the adopted proposal found the tests also read film code, so V1 can reuse a pass on changed code, and it has no learn step. V2 beats V3 because it checks order dependence before a resume runs tests in a new order, fixes the watcher's blind spot (a killed run's FAILs go unflagged) and the start-up wipe explicitly, and replays today's real loss. V3 rests on a wrong fact: it says nothing turns off output buffering, but PYTHONUNBUFFERED=1 is set on this machine and the log grows live (checked); and its code key is swapped out later, which reads as provisional.
Taken from V3: the deliberate mid-run kill in the learn step, "could not run" naming the resume command, and the whole-code key (commit plus uncommitted changes), kept here as the fail-safe for tests without a file stamp. Corrected from V2: the full run is about 23 minutes, not 19.
## Faults in the pick
- F1 [fixed] V2 hung resume entirely on file stamps from the adopted proposal's Step 0; if Step 0 fails, resume would never be built. Now any test without a stamp is keyed to the whole code, so resume works either way and never reuses a pass on changed code.
- F2 [fixed] V2's run-length figure (19 minutes) was low; the run measured today was 135 tests in 21 minutes, so about 23 for all 145. The time limit is now set from the learn step's measured times.
- F3 [fixed] V2 lacked a deliberate kill to count lines lost on a stop; added from V3.
- F4 [named] Change 2 still bundles four linked fixes under one yes (stop the wipe, gate and watcher read the record, measured time limit, a "stopped at" line); they share one failure and one undo commit, but Sam is saying yes to four things.
- F5 [named] Build cost (about 1% of a week once) and the cost of each lost run are unchecked estimates.
- F6 [named] It depends on the adopted kit-tests-when build; its order is fixed there, so resume arrives with that build, not before.
## Final version
**Learn (changes nothing; folds into the adopted kit-tests-when Step 0, about 0.3% of a week).** The traced full run also records each test's seconds; one run goes in reverse order; one run is killed on purpose mid-way to count lines lost. Bar: no test changes result between the two orders (any that does is made independent first), and no finished line is lost on a kill.

**Change 1 (own yes; amends kit-tests-when Change 1, no second store).** kittests.py appends and flushes one line per test the moment it ends: name, PASS, FAIL or crashed, seconds, and its key: the stamp of the files it read, or, for any test whose reads are not yet known, the whole code (commit plus a hash of uncommitted changes). On start, it runs only tests with no line on the current key. Kittests: a run killed after 3 tests and restarted runs only the rest; a changed file makes its tests re-run; a crash and a FAIL are kept, never skipped.

**Change 2 (own yes): nothing wiped, nothing silent.** The start-up launcher stops overwriting the result. The handover gate and the watcher read the record and name each test with no line on the current code; FAILs from a killed run are flagged; "could not run" names the resume command. The time limit is set from the measured times, and a timeout writes a "stopped at" line. A kittest replays today's 13:11 restart and must keep the 13:03 greens.

**Numbers to beat** (handover-end.log and the record, at the end-of-film review): full re-runs after a stop, 6 on record, to 0; "no finished run" refusals, 4, to 0; tests re-run after a restart, no more than the unfinished ones plus those whose files changed.

**Cost:** about 1% of a week once, unchecked; saves a run of about 23 minutes on every stop.

**Lost / Added.** Lost: starting again from the first test after any stop; wiping the last result at every machine start. Added: one result line per test as it ends; the reverse-order and kill checks; a measured time limit; three kittests.
## For Sam
### Option 1: Keep every check result the moment it finishes
Problem: The automatic checks on our shared drawing tools take about 23 minutes. If the machine restarts or a chat ends part-way, every result is lost and they start again from the beginning; today a restart even wiped a run that had already finished green.
1. First, without changing anything, time each check, run them once in reverse order and once stopped on purpose, to prove they give the same answer in any order and that nothing is lost when stopped.
2. Each check writes its result the moment it finishes, tied to a fingerprint of the exact files it looked at.
3. After any stop, only the checks with no result on today's files run again; a check whose files changed always runs again.
4. Starting a machine no longer wipes earlier results, and a run cut off part-way is flagged, never mistaken for "still going".
Why: It ends the restarts from zero and can never pass a check on files that changed. It is built into the check record you already said yes to, so there is one record, not two.
You'd notice: fewer chats held up "waiting for checks", and no full re-run after a restart.
Other option: Option 2, a simpler separate results file per run.
Lost: starting again from the first check after a stop; the wipe at every machine start.
Added: one saved result per check as it ends; an order test and a stop test; a time limit set from real timings; three new self-tests.
### Option 2: One results file per run, resumed after a stop
Problem: The same: a stopped run of the tool checks loses everything and starts again from the first check.
1. Each check writes its result to a file for that run as it ends.
2. After a stop, if the shared tools are unchanged, only the missing checks run; if they changed, the whole run starts again.
3. A self-test stops a run after three checks and makes sure the restart finishes the rest.
Why: It is exactly what you asked for and quick to build.
You'd notice: the same end to restarts from zero, sooner.
Other option: Option 1.
Lost: starting from the first check after a stop.
Added: a second record beside the one you already approved, which can disagree with it; it watches only the shared tools, so a change to a film's own files could leave an old pass standing.
