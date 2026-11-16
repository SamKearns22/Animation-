# Helper B: why the % of a week estimates miss

## Leak
None (the cache-read facts lean toward pricing steps x history; weighed, not assumed).

## Results
- Films, first estimate vs ledger now (notes/ledger/*.json, summed `cost`): Remakes 14.5 -> 35.96 (2.5x, 19 chats); Blessed 19.0 -> 62.21 (3.3x, 24 chats); Protest Tiers 21.45 (notes/archive/protest-tiers-plan-r0.md) -> 66.63, still open (3.1x, 39 chats). Always low, by a steady 2.5-3.3x.
- Cost per chat is steady, chat count is not: 1.89, 2.59, 1.71% a chat. Protest Tiers was planned as "chat 1 of 8" (ledger titles); notes/cost-diagnosis.md line 90: "a film at 10-15% is about 5-7 such chats". Films took 19-39.
- An outside view would have done far better: before Blessed the finished film cost ~36 (1.7x low); before Protest Tiers the two averaged ~49 (1.36x low), against 3.3x and 3.1x bottom-up.
- Rule 24 (guides/film-quality-rules.md line 25) says "always aim lower", "no padding, no multipliers", and anchors at "about 15% ... 26%"; all three estimates sit in that band.
- Process: proposal-route priced ~1.3% a run; ledger 16 rows, 40.2% in all, all `estimate` rows. No task estimate has an actual beside it; source/ledger.py has no field for one.
- The unit moved: WEEK_USD 290 -> 171 -> 245, still "PROVISIONAL" (.claude/hooks/costwatch.py lines 14-26).
- Gap: lost rows make actuals low; the record cannot say by how much.

## The real decision
Not "price things better" but: what is Sam's number built from, and is it ever checked? The unit is the whole film (all chats and rounds) and every task priced to Sam. Bigger levers than unit prices: chat and round count, rule 24's anchor, the missing feedback loop.

## Root cause
1. Estimates price THINGS; cost follows CHATS (~1.7-2.6% each). Rounds, fixes, research and handovers multiply chats and are never priced (unplanned stages carry 0).
2. Rule 24 forbids the steady ~3x correction the record shows and says "aim lower" toward 15%: the estimate is anchored to the hope.
3. No loop: task estimates are never written down, so nothing learns.
4. A moving unit and lost rows blur every comparison. The 0.3204 re-plan kept the bottom-up frame, so the miss returned (round 2: 2.7 priced, ~9.2 spent).

## Approaches weighed
- A. Refit per-thing units. Same frame; things are new each film; chats unpriced. Rejected.
- B. (Reframe) Outside view: Sam's number comes from past films' real totals and chats x cost per chat, as a range; the thing table only splits it into stages.
- C. Model the driver: chats x steps x history (stepcost.py). Right physics; only 6-7 rows carry steps. Not yet.
- D. (Learn-first) Backtest B and C on the record; log every estimate Sam gets with its actual.
- Chosen: D, then B, then the log, one at a time.

## Proposal
Learn first (changes nothing; one Sonnet chat, ~1%): recompute what B and bottom-up would have said for the 3 films against actuals, with rows `ledger.py audit` lists as missing; ask Sam for one meter reading at the next reset to fix WEEK_USD. Results go in this proposal's notes.

Change 1, only if B lands within 1.5x on every film: the film estimate is the outside-view range (low = cheapest past film, middle = median, high = dearest); rule 24's "aim lower / no multipliers" replaced. Enforced: `ledger.py estimate` refuses a total below the low end without a written reason. Number to beat: next film within 1.25x of the middle (now 2.5-3.3x). ~1.5% once.

Change 2, its own Y: every % put to Sam (task, stage, proposal) gets a logged row; the actual fills itself at close. Enforced: `handover.py end` flags a "% of a week" with no row. Number to beat: half of logged tasks within 1.5x after one film. ~1.5% once.

Sam would notice: larger, honest ranges, and "estimate X, spent Y" after each film.

## Sam test
- Q1: reference-class forecasting plus a calibration log is the expert fix.
- Q2: all three films and process ledgers, not one chat.
- Q3: root cause shown; enforced by ledger.py and handover.py, not by reading; measured each film.
- Q4: four different approaches weighed; the reframe wins.
- Q5: learning changes nothing; each change undoable alone; nothing on trust.
- Q6: sources named; the rest under Unchecked.
- Q7: sized to reach 1.25x; cost stated.
- Q8: no trial; each change permanent, reviewed when Sam declares the film complete.

## Lost / Added
Lost: the low single number; "aim lower" in rule 24. Added: a range from real films, an estimate log, two checks, ~4% of a week once.

## Unchecked
Cache-read correlations; "7 of 9 chats had no row"; Remakes "~45%"; Blessed and Remakes planned chat counts; ccusage, /compact; whether 245 is the true week.
