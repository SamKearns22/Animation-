## Leak
None; no solution stated. Two facts disagree with the ledgers (Unchecked).

## Root cause
1. **A meter exists but nothing runs it.** `source/costbreak.py` (11 Nov) prices each step from real token counts. It reads only the running chat's own transcript, by hand. `ledger.py auto` (the Stop hook) stores only totals. When a chat ends, its step data is gone. So the bills for 29 and 31 fell back to keyword call counts ("Call-count weighted guesses, not metered", bills-29-31.md).
2. **Counting calls misprices.** Every step re-pays the whole history, and chat 29 ended at 252k tokens (bills). A large output is paid again by every later step. "35% looks at code" cannot guide a change.
3. **The sample is one kind.** Both chats were late fix-and-animatic chats (2.57%, 2.36%). Per the ledger's stage table, spend went to moves 11.30 + round-1 moves 14.04 (25.3 of 51.27), unplanned plan 10.08, cast 5.96, sets 4.74.
4. **Why a chat existed goes unrecorded.** Notes, rounds and repeats are 0 in every row of all three ledgers, yet round 1 cost 19.0% (34.21 to 53.21). Rework cannot be tied to its cause.

## Approaches weighed
- A. Read more chats, count calls: same flaw.
- B. Read a hand-picked spread (cheapest and dearest per kind, three films). Better scope; still counts, done once.
- C. **Meter at the source, permanently:** the hook that already runs in every chat writes each chat's priced bill.
- D. **Measure by cause:** each row records the stage, the note numbers fixed and the fault the checks missed.
- E. Controlled reruns of a task. Trials (Q8), and every film is new.

Chosen: C plus D. C shows how cost is spent, D shows why, and a change needs both.

## Proposal
**What.** (1) `ledger.py auto` runs costbreak on its own transcript and helpers'. It stores the bill by kind, the start-up cost and the final history size, including after the app figure is in. (2) `handover.py end` requires the stage and the note or fault numbers. (3) A backfill, done once in full: all 32 Protest Tiers chats (the newest tools, which are the ones to be changed) plus the 3 dearest of Blessed and Remakes. Steps are weighted by the history size at that point, use costbreak's kinds, and are scaled to each chat's app figure.
**Enforced** by the Stop hook and the handover check; no chat chooses. A failed bill prints a "Checks:" line and never blocks the push.
**Number to beat.** Every bill within ±10% of the app's figure, checked by `ledger.py app` (costwatch ran 20-75% low). The backfill names the 3 sources covering at least 80% of Protest Tiers' spend. Each later change cites the bill line it cuts and is reviewed when the film is declared complete.
**Cost (unchecked).** Build about 1-1.5% of a week (Opus). Backfill of 38 chats about 4-7% (0.1-0.2% per chat). A tool job outside the film budget (rule 86).
**Sam notices:** one table, "where Protest Tiers' week went, and why"; nothing in film chats.

## Sam test
- Q1: Experts meter at the source, weighted by position and by cause.
- Q2: The whole newest film plus older outliers; two same-kind chats were too narrow.
- Q3: Runs in every chat by hook; bills must reconcile with the app, so half-efforts fail.
- Q4: Five approaches weighed; C+D covers how and why.
- Q5: Hook crash guarded; undo is one function; first 3 bills shown against the app first.
- Q6: Sources named; estimates marked unchecked.
- Q7: Sized by coverage and accuracy; the cheap trap (2-3 more chats) rejected.
- Q8: Permanent meter; backfill done once in full; reviewed at film complete.

## Lost / Added
- Lost: nothing.
- Added: a bill per ledger row, a stage and notes field at handover, the backfill (4-7%).

## Unchecked
- Whether `list_events` has token counts.
- The cost per chat read.
- Blessed ~80% and Remakes ~51% match a stale "After the film" line (80.02, 51.54); the ledger headers read 62.21% and 35.96%.
- Protest Tiers reads 51.27% against 33.55% in that line, and has 32 chats, not 29.
- Reconcile these first.
