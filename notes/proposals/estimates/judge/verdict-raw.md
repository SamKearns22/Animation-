## Leak
yes: mild. The Facts section ends "What cost follows" with the cache-read correlations and "Estimate tables price the THING ... they do not price the number of chats, steps, fix rounds or history size", which points at "price chats / steps x history, not things". V1 (written before the helpers by the same chat) took that line straight; V2 and V3 weighed it and chose a reference class from real film totals instead, so the anchor was partly resisted.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 3 | 3 | 2 | 3 | 14 |
| V2 | 4 | 3 | 4 | 4 | 4 | 19 |
| V3 | 4 | 4 | 4 | 4 | 4 | 20 |
## Sam test
Q1: Yes, with the fixes: an expert would forecast from real past totals (reference class), price surprises the moment they appear, and keep every quote beside its actual so the method corrects itself. That is the pick.
Q2: Evidence is all three films' whole ledgers (checked: 35.96, 62.21, 66.63 now) plus the process ledgers, not one chat. Weakness fixed: the three films grew each time (36 -> 62 -> 67), so a plain average of past films would still have been low; the learning step now tests a size-scaled version too.
Q3: Root cause shown (things priced, chats and rounds not; rule 24 says "aim lower, no multipliers"; unplanned work enters at 0; no quote is ever checked). Enforced in ledger.py and handover.py, not by a chat choosing to read. Known to work when the next film lands inside its range. V3's task log had no check; fixed by V2's handover check.
Q4: Four approaches weighed (better unit prices, reference class, steps x history model, live counter); per-unit tuning and a counter alone rejected with reasons.
Q5: Learning changes nothing. Each change is its own Y and is undone alone (a rule line, one ledger field, one check). Nothing goes in on trust: change 1 only if the backtest passes. Honest risk: the first number Sam sees will read about 3-4x what he is used to.
Q6: Facts checked against the ledgers and code (totals, medians, row sources, rule 24 line 25, costwatch line 26, cost-diagnosis line 90, "chat 1 of 8"). One V3 claim corrected (the forecast already multiplies by the rate so far). Unchecked items listed in the final version.
Q7: Sized to make the number true, not cheapest; a counter alone and a unit-price tune were rejected as cheap-but-worse. Its own cost is given as a range and logged as the first entry.
Q8: Nothing temporary: the learning step is a measurement, not a trial; each change is permanent and reviewed when Sam declares the next film complete.
## Pick
V3
## Why
V3 finds the widest set of real causes and is the only one that fixes unplanned work entering at 0, which is why the budget stops and stage alarms fire late. It learns before changing and asks a separate Y per change. V2 is close and gives a clear pass mark and a check for task prices, but its own gate (outside view within 1.5x on every film) fails on its own figure for Blessed (1.7x), and it leaves unplanned rounds unpriced. V1 has the right instincts (dollars as the stored unit, ranges, unplanned work as its own quote) but bundles six changes into one yes and builds a steps x history model on 7 rows before any result shows it works.
Taken from V2: the pass mark for the backtest and for the next film, the handover check that flags any "% of a week" put to Sam with no logged row, and one meter reading to settle the week size. Taken from V1: store every price in dollars and show % at the current week size, so a week-size change restates open prices instead of breaking the comparison; and quotes given as typical-to-bad-case ranges. Added by the judge: reuse the existing last-three-films comparison (ledger.py compare_line, now used only after a film) as the before-the-film reference class.
## Faults in the pick
- F1 [fixed] V3 said the forecast "scales the same low base"; it already multiplies by the cost rate so far, so it corrects mid-film. The real fault is the starting number and unplanned work, not the forecast formula.
- F2 [fixed] A plain average of the last films would still have been low (films grew 36 -> 62 -> 67). The learning step tests three methods (plain reference class, scaled by film size, chats x cost per chat) and keeps the one with the smallest worst miss.
- F3 [fixed] V3's change 2 had ledger.py stage refuse pct 0, but unplanned stages are only added when marked done. Now an unplanned stage is opened and priced when work on it starts.
- F4 [fixed] V3's task-price log relied on a chat choosing to log. Now handover.py flags any "% of a week" given to Sam with no logged row (from V2).
- F5 [fixed] The week size is still provisional (245); one meter reading at the next reset settles it, and prices are stored in dollars (from V1).
- F6 [named] The honest first number for a film will read about 40-70% of a week, far above the 15% aim. That is the true cost today; cutting it is a separate job and is not done by lowering the estimate.
- F7 [named] Only three films make the reference class, and lost rows make past totals low; ranges will be wide until more films are in.
- F8 [named] The cost of this work is itself an estimate (range below); it is logged as the first entry so its miss is measured.
## Final version
**Learn first (changes nothing; one Opus medium chat; 2-4% of a week).** One table in dollars for Remakes, Blessed, Protest Tiers and the proposal-route runs: estimate vs actual, chats planned vs used, cost per chat, notes rounds, unplanned stages, app vs transcript figure where both exist, rows `ledger.py audit` lists as missing. Backtest three ways of making the first number, each using only films finished before: (a) last films' real totals as a range; (b) the same scaled by film size (new characters and places); (c) chats x cost per chat from past films. Keep the one with the smallest worst miss. Sam gives one meter reading at the next weekly reset to settle the week size. This chat's own cost is logged as the first quote.

**Change 1 (own Y; only if the kept method lands within 1.5x on both Blessed and Protest Tiers backtests).** A film's estimate is that method's range (typical to bad case), stored in dollars, shown in % at the current week size, with a chat count. The thing table only splits it into stages. Rule 24's "always aim lower", "no multipliers" and starting units are replaced. `ledger.py estimate` refuses a total with no chat count, or below the range's low end without a written reason. Pass mark: the next film lands inside its range (now 2.5-3.3x out), checked when Sam declares it complete.

**Change 2 (own Y).** An unplanned stage or round is opened and priced from past rounds the moment work starts; the film's estimate rises and Sam sees the new figure in the next message. `ledger.py stage` refuses to close an unpriced unplanned stage. Pass mark: no unplanned stage at 0 on the next film.

**Change 3 (own Y).** Every price put to Sam for a task, stage or proposal is a logged quote; the actual fills itself in at the chat's end. `handover.py end` flags any "% of a week" in a message to Sam with no logged quote. Pass mark: after the next film, half the logged quotes within 1.5x.

Cost: 2-4% to learn, 1-3% per change, about 0.2% per film after, against misses of 20-45% now. Unchecked: whether 245 is the true week; how far transcript figures miss the app's; Protest Tiers' final total (still open).
## For Sam
### Option 1: Learn, then honest ranges and priced surprises
First one chat measures every past estimate against what was really spent and tests three ways of giving you a number, without changing anything. Then, each with its own yes: a film's price becomes a range taken from what past films really cost (the price rule's "always aim lower" goes); any extra round is priced the moment it starts and the film's total goes up; and every price I give you is written down with what it really cost beside it.
You would notice: a much higher first number for a film (about 40-70% of a week, as films really cost now), a new figure when an extra round starts, and "said X, came to Y" after jobs.
Lost: the low, single first number you are used to, and "always aim lower" in the price rule.
Added: a range from real films, prices for surprises, a written record of every price against its real cost; about 2-4% of a week to measure, 1-3% per change.
### Option 2: Learn, then a range and a price record (no surprise pricing)
The same measuring chat, then two changes: the film price becomes a range from past films' real totals, and every price I give you is written down and checked against its real cost. Extra rounds stay unpriced until the end of the film, so the budget stop still fires late when one appears.
Lost: the low single number and "always aim lower"; the warning when an extra round starts.
Added: a range from real films and a record of every price against what it cost; slightly cheaper to build.
