# Helper A: why the % of a week estimates miss

## Leak
None. The problem file states facts only.

## Results
- Films, estimate vs ledger (sum of chat `cost`, notes/ledger/*.json): Remakes 14.5 vs 35.96 (19 chats); Blessed 19 vs 62.21 (24 chats); Protest Tiers 21.5 first plan vs 66.63 now (39 rows, open; problem file's 61.99 is stale). Every miss is low, 2.5x to 3.3x.
- Cost per chat is steady: median 2.02 / 2.19 / 1.83% (same ledgers). So a film costs roughly chats x 2%.
- The plans got the chat count wrong: cost-diagnosis.md line 90, "a film at 10-15% is about 5-7 such chats"; Protest Tiers titled "chat 1 of 8"; real: 19, 24, 39.
- Rule 24 (rulebook line 25) builds in the low bias: "always aim lower", "no multipliers", "a notes round 2.7"; real rounds ran 10-14% (problem file).
- Unplanned work enters at pct 0 and never raises the estimate (problem file: 10.08, 17.35).
- The unit moved: WEEK_USD 290, then 171, then 245 "PROVISIONAL" (costwatch.py line 26), "+-20%" (line 15).
- Task prices are never compared with an actual: no ledger field holds one (problem file). Process ledgers are all transcript estimates (proposal-route: 16 of 16, checked).
- Gap: no record of how far transcript estimates miss the app figure.

## The real decision
What number, for the whole film and all its chats, Sam gets before go, and how it stays true as the film runs. Bigger levers than unit prices: the chat count, unplanned rounds, a fixed unit.

## Root cause
Estimates price the things on screen; spend is set by how many chats run, which fix rounds, repeat notes and unplanned stages drive, and the method prices none of them. Nothing closes the loop: the forecast (ledger.py line 613) scales the same low base; task prices are never checked. The earlier fix (rule 24: rounds priced from real rounds) failed: its 2.7 starting unit was never replaced by the measured 10-14.

## Approaches weighed
1. Better unit prices: wrong driver; every film is new, so units average unlike things.
2. Reframe: price by chats. Reference class from the last three films (chats used x cost per chat), quoted as a range; the thing table only says where the chats go.
3. Learn first: rebuild every past estimate vs actual in dollars, with chats, rounds and unplanned stages, before any change.
4. Live counter (ccusage-style) only: shows spend, gives no go/stop number.
Chosen: 3, then 2, then two follow-ons.

## Proposal
**Learn first (changes nothing, ~1.5% of a week, one Opus medium chat):** one table, in dollars, for Remakes, Blessed, Protest Tiers and the proposal-route runs: chats planned vs used, cost per chat, rounds, unplanned stages; and app vs transcript figure where both exist. Output: the reference class.

**Change 1 (on Sam's Y, after the table):** a film estimate is chats x measured cost per chat, from the last three films, given as a range in dollars and %. `ledger.py estimate` refuses a total with no chat count, or below the reference low end without a named reason; rule 24's "aim lower / no multipliers / starting units" is replaced. Beat: the next film lands inside its range (now 2.5-3.3x out), checked when Sam declares it complete.

**Change 2 (separate Y):** an unplanned stage is priced the moment it appears and raises the film's estimate; Sam sees the new figure. `ledger.py stage` refuses pct 0. Beat: zero unplanned rows at 0.

**Change 3 (separate Y):** every price put to Sam for a task is stored with its job and the actual written beside it at the end. Beat: after three tasks, median miss under 1.5x.

Cost: ~1.5% to learn, ~1% per change; ~0.2% per film after, against 20-40% surprises now. Sam would notice: a higher first number, as a range; a new number when an unplanned round starts; "was X, came to Y" after tasks.

## Sam test
Q1: yes; reference-class forecasting is the standard fix for one-sided misses.
Q2: all three films plus process work, not one chat.
Q3: enforced in ledger.py, not by a chat choosing to read; judged on each film's real total.
Q4: four different approaches weighed; per-unit tuning rejected with reason.
Q5: learning changes nothing; each change undone alone.
Q6: sources named; gaps below.
Q7: sized to make the number true, not cheapest; a counter alone was rejected as cheap-but-worse.
Q8: each change is permanent, reviewed at film complete; no trials.

## Lost / Added
Lost: the low "aim lower" first number; rule 24's starting units. Added: a chat count and range on every estimate; re-priced unplanned work; task actuals.

## Unchecked
Whether WEEK_USD 245 matches Sam's meter; how far transcript estimates miss; Protest Tiers' final total (open); the 10 "auto" rows' content.
