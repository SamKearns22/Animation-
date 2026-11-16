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
