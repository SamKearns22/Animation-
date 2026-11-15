## Leak
yes: mild. The problem frames the answer as "which chats, how many, which films", lists the kinds of work Protest Tiers chats differ by, and gives a per-chat reading cost. That points helpers toward "read a sample of chats by kind" rather than asking whether reading chats is the right method at all. It states no solution outright.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 4 | 4 | 4 | 19 |
| V2 | 2 | 2 | 2 | 2 | 4 | 12 |
| V3 | 4 | 3 | 3 | 3 | 4 | 17 |
## Sam test
Q1: Yes. An expert would measure real tokens at the source, weight each step by the history it re-reads, reconcile to the bill, and tie cost to its cause before choosing a fix. That is the pick.
Q2: All 32 Protest Tiers chats (made with today's tools, the ones to change) plus the 3 dearest of each older film. That is wider than two same-kind chats and better aimed than all three films in full.
Q3: The meter runs from the Stop hook in every chat. Bills must match the app's figure or they are marked unfit. Note numbers are cross-checked against the notes the chat ticked, so an empty field fails the handover. It is still weak if old transcripts lack token counts (F4).
Q4: Five methods were weighed: more call counts, a hand-picked spread, metering at the source, tracing by cause, and replays. Source metering plus cause tracing is the only pair that answers both "how" and "why".
Q5: It only reads and records. Undo is one function in the hook plus one handover field. No film change happens until Sam sees the ranked causes. The first 3 bills are shown against the app before the backfill.
Q6: The ledger stage figures were checked (moves 11.30, round-1 moves 14.04, plan extras 10.08, cast 5.96, sets 4.74, round 1 19.0) and are right. Costs and token availability are marked unchecked.
Q7: It is sized by coverage and accuracy. The cheap trap (2-3 more counted chats) is rejected. Honest cost is about 5-8.5% of a week.
Q8: The meter is permanent. The backfill is done once and in full. Everything is reviewed when Sam declares Protest Tiers complete.
## Pick
V1
## Why
V1 builds on the tool that already exists. `source/costbreak.py` already prices each step from real token counts, and `ledger.py auto` already runs in every chat but keeps only totals. Both are confirmed in the source. So the build is small and it hooks into what is already running. V3 names `ledger.py` as the closest tool and misses `costbreak`, so it would rebuild a meter that is already there. V3's "redone" flag also comes from notes fields that chats type in, which is the very fault that left every ledger row at 0. Its 5% gate may be impossible to meet, since costbreak's prices are only good to about 20%, and that could block every decision. V2 proposes a code-finding fix now, based on guessed call shares and an unchecked "10-15%" saving. That is the pattern Sam objected to at 19:11, and it is the cheap trap. From V3 I took three things: the model column read from the transcript (chats 27, 30 and 31 are titled Opus but logged as sonnet), the ranked one-page causes report with a film example per cause, and fixing the ledger disagreements as a first step.
## Faults in the pick
- F1 [fixed] V1's model column stayed wrong (sonnet for "Opus medium" chats 27/30/31). The meter now takes the model from each step in the transcript (from V3).
- F2 [fixed] Stage and note numbers were typed by the chat, so a chat could pass on paper. The handover check now matches them against the notes ticked in that chat's notes diff and fails on a mismatch.
- F3 [fixed] The ledgers disagree: headline 51.27% against the "After the film" line's 33.55%, and Blessed 62.21 against 80.02, Remakes 35.96 against 51.54. This is now step 0, done before any backfill.
- F4 [named] Unchecked: whether past chats' records (list_events) carry per-step token counts. If they do not, the backfill weights steps by history size and scales to the app figure. That is an estimate, and it will be labelled as one.
- F5 [named] costbreak's prices come from the cost watch, which ran 20-75% low. The ±10% match may fail at first. If it does, the prices are fixed before any bill is trusted.
- F6 [named] Backfill cost (0.1-0.2% per chat) is unchecked, and so is the build cost (about 1-1.5%).
- F7 [named] The "3 sources cover 80% of spend" target is a guess at what the answer will look like, not a fact.
## Final version
**Step 0 (fix the record).** Find why the three ledgers' headline totals disagree with their "After the film" lines. Correct `ledger.py` so that one figure is the real one.

**1. A permanent meter.** `ledger.py auto` (the Stop hook, already in every chat) runs `costbreak` on the chat's own record and its helpers' records. It stores the bill by kind of step, the start-up cost, the final history size, and the model per step, all from the transcript. It keeps doing this after the app figure arrives. A failed bill prints a "Checks:" line and never blocks the push.

**2. Cost by cause.** `handover.py end` records the stage and the note and fault numbers worked. They are cross-checked against the notes ticked in that chat, and the handover fails on a mismatch. Rework (a repeated note, a rebuilt stage) is then tied to its cost.

**3. Backfill, once and in full.** This covers all 32 Protest Tiers chats plus the 3 dearest app-visible chats of Blessed and of Remakes (38 in total). It uses real tokens where the record holds them. Otherwise it weights each step by the history size at that point, scales to the app figure, and labels the result an estimate. The first 3 bills are compared with the app before the rest run.

**Pass mark.** Every metered bill is within ±10% of the app's figure (`ledger.py app`). A bill outside that is marked unfit, and nothing is chosen from it.

**Output.** One ranked page: "where Protest Tiers' week went, and why". It lists the top causes, each with its share and a real film moment. Every later cost change must name the line it cuts. It is reviewed when Sam declares the film complete.

**Cost (unchecked).** Build about 1-1.5% of a week (Opus, high). Backfill about 4-7%. Together they are one tool job outside the film budget (rule 86).
## For Sam
### Option 1: Meter every chat, then trace the newest film in full
Every chat would record exactly where its cost went, automatically, without anyone remembering to do it. Each chat would also record which of your notes it was fixing. Then the whole of Protest Tiers, and the 3 dearest chats from each of the two older films, get measured the same way and checked against the app's real figures. You get one page: "this is where the week went, and why", with a real moment from the film for each cause. You would notice future cost fixes aimed at proven costs, not guesses.
Lost: nothing in the films. About 5-8.5% of a week for this one job.
Added: a permanent cost meter in every chat, a short notes check at each handover, and the one-page answer.
### Option 2: Meter every single step of all three films
This is the same idea, but it measures every chat of Blessed, Remakes and Protest Tiers. Each step's cost would have to match the app within 5%. It is wider, but the older films were made with older tools, and the strict match may never pass, which could hold up every decision. It also rebuilds a meter that already exists.
Lost: nothing in the films. About 8-10% of a week.
Added: a cost row for every step ever taken, and the same one-page answer once it passes.
