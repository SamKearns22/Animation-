# Proposal: A stopped kit-test run loses every result it had

Status: open

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
