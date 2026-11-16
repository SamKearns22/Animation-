# Proposal: Why the % of a week cost estimates are rarely right

Status: open

## Problem
Sam, 16 Nov (session d675UK2u): "your estimates in terms of week costs (for example, this task will cost 3% of a week)
are rarely correct." Chats tell Sam what a film, a stage or a small task will cost as a share of his weekly allowance,
and he decides go / stop / which version on that number. The numbers usually land far from what was spent, almost
always low, so his decisions are made on a figure he cannot trust, and the budget stops and alarms built on the same
figures fire late or after the money is gone. The job is to find why the estimates miss and what would make the number
Sam is given one he can rely on, whole films and single tasks alike.

## Facts
Measured by chat 1 of this round (16 Nov) from notes/ledger/*.json, notes/ledger/app-costs.tsv, the film notes'
estimate tables and .claude/hooks/costwatch.py history. "% of a week" = list dollars / WEEK_USD x 100.

Whole films, estimate vs spent:
- Remakes: estimate 14.5% (notes/remakes.md "Plan extras", made 10 Nov). Ledger now 35.96% (19 rows, all app
  figures); the film notes and the Blessed post-mortem say ~45%. 2.5x to 3.1x.
- Blessed: estimate 19% ("FULL" version, notes/archive/blessed-handovers.md). Ledger now 62.21% (24 rows, 18 app,
  6 estimated); the compare line says 80.02% (at the old week size, see below). 3.3x or more.
- Protest Tiers: first plan 21.5% (notes/archive/protest-tiers-plan-r0.md); at the round 1 re-plan 34.2% was already
  spent. Re-plan (chat 20, 15 Nov): 29.3% more, landing at 63.5%. Ledger now 61.99% with round 2 and the final still
  open, so it will pass 63.5%. Against the first plan: 2.9x+.
- Framing research: estimate 1.4%, ledger has no cost rows at all (stages marked done with spent 0).

Per stage (Protest Tiers ledger stages, cumulative "spent" differenced; estimate = the stage's priced share):
- plan 0.70 -> 0.00 (rows missing); plan extras (unplanned) 0 -> 10.08; cast 2.09 -> 5.96 (2.9x); sets 3.70 -> 4.74
  (1.3x); moves 3.07 -> 11.30 (3.7x); animatic1 1.40 -> 2.13 (1.5x); round1 cast 2.31 -> 3.66 (1.6x); round1 sets
  0.32 -> 1.30 (4.1x); round1 moves 4.45 -> 14.04 (3.2x); round1 plan and animatic2 0 spent (rows filed elsewhere).
- Round 2: priced 2.7% in the re-plan table, stored in the ledger as 0.865 (the re-plan scaled new stages by 0.3204 so
  shares add up); 5 chats since animatic 2 on 15 Nov total 9.42% (ledger rows), 8.78% by the cumulative figure; the
  task brief quotes 9.18%. About 3.3-3.5x the price, round still open.
- Blessed stages were marked done out of order (plan marked last, at 50.92%; sets at 0 then an unplanned sets 5.24),
  so its per-stage actuals cannot be read reliably: animatic1 2.0 -> 9.83, round1 2.5 -> 10.01, unplanned
  walliams-face 0 -> 11.58, unplanned plan time 1.0 -> 8.31.
- Remakes priced "one notes round" inside a 3.0% line for critique + sheet + animatic + round + final; it went to
  animatic 3 and further rounds (notes/remakes.md).
- Unplanned work is never priced: stages flagged "unplanned" carry pct 0 (Protest Tiers plan extras 10.08; Blessed
  sets, cast, walliams-face 17.35 together). The film's total estimate is not raised when one appears.

Small tasks and process work:
- The proposal route was priced "~1.3% of a week per route run" (notes/proposals/install-route verdict). The 15
  proposal-route ledger rows are 0.25 to 8.33% a chat (mean 2.57%), and one route run spans several chats plus helpers.
- Other process prices given to Sam ("about 5-6% of a week once", "~1-2% saved per film", "About 2% (unchecked)") are
  in notes/proposals/*.md; none has an actual written beside it. No ledger field holds a task's estimate, only
  film-level `estimate` and stage `pct`.
- One chat (533f1450) appears in both the proposal-route (3.01) and protest-tiers (2.78) ledgers: double billing,
  fixed 16 Nov (chat 5: a chat whose task is under notes/proposals/ bills to proposal-route only).

What cost follows:
- notes/ledger/app-costs.tsv (65 chats with the app's real figures): the chat's dollar cost correlates with cache
  reads (the whole history re-read each step) at 0.90 (Opus, 53 chats) and 0.98 (Sonnet, 12); with the history size at
  the end at 0.87 / 0.98. Cache reads are roughly steps x average history.
- Only 7 ledger rows (proposal-route, cost-diagnosis, job-e-measurements, 16 Nov on) carry `steps` and `hist_k`
  (stepcost.py, run by ledger.py auto). On those 7: cost vs steps 0.87, vs steps x history 0.86 (too few to separate).
  Example: a19b01a1 100 steps, 194k history, 2.96%; 67b38f9d 15 steps, 116k, 0.25%.
- Estimate tables price the THING (a character 1.9, a Glimpse 1.3, a second of action 0.6, a painting 0.6), measured
  from earlier films' stage totals; they do not price the number of chats, steps, fix rounds or history size, and
  each new film's things are new (rule: every film is new), so the per-thing units are averages over unlike things.

Where the numbers come from:
- Row sources across all 24 ledger files: 67 'app' (the app's own dollar figure, read with get_session), 71
  'estimate' (worked out from the chat's transcript), 13 with no source. Films are mostly app (Protest Tiers 29 of 37);
  process ledgers are all estimates (morning-report 17, proposal-route 15, overnight-run 9). (The brief said "most rows
  are est, few app": true for process work, not for films.)
- The weekly limit is not published. WEEK_USD in costwatch.py: 290 (9 Nov), 171 (13 Nov, so Blessed read 80% as Sam
  saw it), 245 (15 Nov, "PROVISIONAL", from Sam's meter showing 17% after the 14 Nov reset). Ledger % figures were
  rewritten at 245 (usd/cost = 2.45 on every app row), but estimates made on 9-13 Nov were written against 290 or 171
  and are compared today with spend at 245: the unit itself moved by -41% then +43%. costwatch.py says both price and
  week size are "good to about +-20%".
- Ledger rows were lost: 7 of 9 checked chats had no cost row (startup-reading, change 1); framing-research has none.
  So past spent totals are low, which makes the real misses larger than shown above.

Outside help Sam showed (unchecked):
- A Reddit post on ccusage: a counter that reads the local chat logs and prices tokens in API dollars.
- /compact: summarise the chat so far and carry on in the same chat with a short history.

## Record
notes/ledger/
notes/ledger/app-costs.tsv
notes/protest-tiers.md
notes/remakes.md
notes/archive/blessed-handovers.md
notes/archive/protest-tiers-plan-r0.md
notes/budget-job.md
notes/cost-diagnosis.md
notes/proposals/
.claude/hooks/costwatch.py
source/ledger.py
source/stepcost.py
source/costbreak.py
guides/film-quality-rules.md
guides/job-packs.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 0b1ec24ca9bc789f -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper B, V3 = helper A. Picked: V3 (helper A). Critiqued: 8 found, 5 fixed, 3 named.

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
