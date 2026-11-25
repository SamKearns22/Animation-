# Helper A: kittest-resume

## Leak
Yes: the problem file quotes Sam's Y'd answer (results per run, each test written as it ends, restart re-runs only the unfinished). Tested, not built.

## Results
- **Today a restart wiped a finished green run.** Restart 13:11:00 (`/proc/uptime`); a new run at 13:11:31 reopened kittests-last.log with "w" (watcher.py line 565), erasing the 13:03 "all passed". The disk survived (`ran/_since` is from 23 Nov). Checked.
- **Runs lost:** 4 "no finished kit-test run" refusals in 3 chats on 23 Nov (handover-end.log). Open Wounds chats 7 and 10 also lost theirs (brexit-is-done-handovers.md lines 114, 173). That is at least 6 in 3 days. Cause on 23 Nov: unchecked.
- 17 "STILL RUNNING" refusals in 12 chats (handover-end.log).
- **Run length:** 123 tests in about 16 minutes today, so about 19 for all 145 (limit 1800 s). Per-test times: recorded nowhere (a gap).
- **Watcher blind spot:** watcher.py `kittest_faults` treats a log with no summary line as "still running", so a killed run's FAIL lines go unflagged (lines 258 to 266).
- PYTHONUNBUFFERED=1 is set here (elsewhere: unchecked). Cost per lost run in % of a week: unchecked.

## The real decision
Keep each test's result tied to the code it tested, so no stop loses it. Sam already adopted a per-test stamp record (kit-tests-when.md); resume is the same mechanism. Make that record write as each test ends; build no second store.

## Root cause
1. One whole-run log is the only record, and its last line is the only proof the run finished.
2. Every machine start, a resume included, truncates that log.
3. Results do not say what code they tested, so partial results could not be trusted.
4. A timeout kill writes nothing, and the watcher reads the silence as "still running".

## Approaches weighed
1. **Sam's wording:** a file per run, plus resume. Stale if code changed between the stop and the restart, and it duplicates the adopted record.
2. **Reframe:** the per-test stamped record, written as each test ends. A restart, a new chat or a handover runs only tests with no matching line.
3. **Faster runs:** split across processes. A smaller window, but a stop still loses everything.
4. **Learn first:** per-test times, plus a check that tests pass in any order (a resume runs a subset in a fresh process).

Chosen: 4 then 2.

## Proposal
**Learn (changes nothing, about 0.3% of a week).** Add to kit-tests-when's traced Step 0:
- Each test's seconds.
- One run in reverse order.

Bar: no test changes result between the two orders. Any that does is made independent first.

**Change 1 (own yes): write as each test ends.** This amends kit-tests-when Change 1.
- kittests.py appends and flushes one line per test the moment it ends: name, PASS, FAIL or crashed, seconds, and the stamp of the files it read.
- A kittest kills a run halfway and restarts it. Finished tests must be skipped, unfinished ones run, and a test whose file changed must re-run.

**Change 2 (own yes): nothing wiped, nothing silent.**
- `kittests-bg` stops truncating the log.
- The gate and the watcher read the record and name the tests that have no line for the current code. FAILs from a killed run are flagged.
- The time limit is set from the measured times, and a timeout writes a "stopped at" line.
- A kittest replays the 13:11 wipe and must keep the 13:03 greens.

**Numbers to beat** (handover-end.log and the record, at the end-of-film review):
- Full re-runs after a stop: 6 now, target 0.
- "No finished run" refusals: 4 now, target 0.
- Tests re-run after a restart: no more than the unfinished tests plus those whose files changed.

**Cost:** about 1% of a week once (unchecked), against 15% per film; saves a 19-minute re-run per stop.

**Sam would notice:** fewer "waiting for checks" hold-ups.

## Sam test
- Q1: Yes. Experts key results to the inputs per test (build-system practice), not to a whole-run log.
- Q2: Every chain's handover log, the archive and today's restart.
- Q3: Root cause checked; enforced in code; kittests replay real losses.
- Q4: Four approaches; only the reframe survives code changing mid-stop.
- Q5: Order-dependent tests could pass wrongly; the learn step rules that out first. Each change undoes in one commit.
- Q6: Sources named; unknowns unchecked.
- Q7: Not the cheap per-run file; reds and stamps kept.
- Q8: Permanent; reviewed against the film's numbers.

## Lost / Added
- Lost: restarting from test 1; wiping the last result at every start.
- Added: a record line per test; the reverse-order check; a measured time limit; two kittests.

## Unchecked
The 23 Nov cause; cost per lost run; PYTHONUNBUFFERED elsewhere; order dependence; build cost.
