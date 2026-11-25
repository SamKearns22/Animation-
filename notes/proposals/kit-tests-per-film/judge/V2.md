## Leak
Yes: the title and Sam's quote give the answer (film start and end).

## Results
- Per-test stamps went live 25 Nov 13:07 and were finished at 17:23. Sam asked at 17:57. Nearly all he saw came before them (git log).
- 25 Nov kit refusals: 10 rows. 5 came after 13:07, in 2 chats: 2 "still running", 2 crashes of `people_from_a_description`, 1 "no run" (handover-end.log).
- That test has crashed on every fresh machine since 22 Nov (next-jobs.md).
- Stamp grain (kittest-stamps.tsv): `ink.py` is read by 81 of 147 tests (14.7 of 15.9 min), `body.py` by 78 (10 commits since 18 Nov), `kitstamps.py` itself by 85. A core drawing fix reruns nearly everything.
- Regression: c87022ef (17:49) put the handover's stale run inside the Override branch. Without Override, a chat's final code goes untested (handover.py 580–600).
- Open Wounds: 18 chats, 41.97% of a week (ledger). The ledger has no kit-test step kind, so the usage cost Sam names is unmeasured: a gap.
- body_check_back_view was red in 4 chats in a row (kittest-reds.log). Whether reds would reach an animatic under start/end-only: unchecked.

## The real decision
Per film and across parallel chains: where must the tests stand between a broken shared tool and Sam's eyes, at the least cost? Not "how often per chat". Bigger levers: the crashing test, coarse grain, the regression, 18 chats per film.

## Root cause
Chats are blocked on things they did not make: a busy start-up run, a test crashing since 22 Nov, others' reds. Coarse grain adds reruns. Stamps had not yet helped.

## Approaches weighed
1. **Sam's draft:** full set in the first chat and before the final. A chat "suggests" a run after a major change. Relies on judging "major"; animatics reach Sam on untested shared code.
2. **Reframe:** test where Sam's eyes meet the work: film start, and every animatic and final (finish.py's stale-only gate, already built). No run or wait in other chats. Kit changes are caught at the next animatic.
3. **Repair-first:** fix crash, grain and regression, keep the per-chat gate. Against Sam's word.
4. **Off-chat runner per push:** feasibility unchecked.
5. **Learn-first:** measure cost and animatic risk first.

Chosen: 2, with 5 as Step 0 and 3's repairs as separate fixes.

## Proposal
**Step 0, learn (changes nothing, about 0.3% of a week).** From 3 days of transcripts:
- (a) % of a week spent on kit tests (waits, refusals, retries, fixing others' reds)
- (b) per past red: the chat that caused it, and any animatic made before it was caught
- (c) whether handover.py can tell a film's first chat

**Change 1 (Sam's Y).**
- setup.sh runs the tests only in a film's first chat, and `handover.py end` gates only there.
- A kittest proves a mid-film chat neither runs nor waits.
- To beat: mid-film refusals 10 a day → 0; waits → 0 min.
- Safe while finish.py's gate stays.

**Change 2 (own question; differs from Sam's draft).** Keep the stale-only run before every animatic.
- That is where Sam first sees a fault; film-only chats wait a median 0.4 min.
- It replaces "suggest a run" with a check, not a chat's judgment.
- To beat: animatics on untested shared code → 0.
- Asked with Step 0's (b) count. On N, only the final is gated.

**Fixes (one commit and one kittest each):**
- F1: undo c87022ef
- F2: make `people_from_a_description` run on a fresh machine
- F3: drop `kitstamps.py` from 85 tests' reads

**Cost.** About 1% of a week each, once (unchecked). Per film: minutes of runs in Sonnet finish chats. Open Wounds' overrun of 15% is chat count, not kit tests.

**Sam would notice:** no handover stalls; finals always green.

## Sam test
- Q1: Experts test the build before it ships, not every worker's step.
- Q2: Whole film and every chain; logs plus Step 0.
- Q3: Root cause checked; enforced in code; two numbers.
- Q4: Five approaches weighed.
- Q5: Each undoes in one commit. A late mid-film red is stopped by finish.py before Sam sees it.
- Q6: Sources named; gaps unchecked.
- Q7: Keeps the animatic gate, the cheap version's trap.
- Q8: Permanent. Step 0 is a measurement. Reviewed at film end.

## Lost / Added
- Lost: the start-up run and handover gate in mid-film chats; the early catch of others' reds (now caught at the next animatic); the "suggest a run" line.
- Added: a first-chat marker; one kittest per change and per fix.

## Unchecked
- kit-test usage cost per chat
- whether reds reached animatics
- whether handover.py can tell a film's first chat
- why `kitstamps.py` is read by 85 tests
- the build costs
- whether an off-chat runner is feasible
