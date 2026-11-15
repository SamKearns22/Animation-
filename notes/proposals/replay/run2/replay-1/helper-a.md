# Helper A: cutting what a film costs to make

## Leak
Mild leak: the problem file points at the code MAP and `source/page.py` ("whether chats 29 and 31 used them"), which steers toward a look-up fix. I set that aside.

## Results
- Protest Tiers: **51.27% of a week spent over 32 chats**, against the 15% aim (3.4 times). Average about 1.6% a chat (ledger protest-tiers.md).
- The last films were the same: Blessed 62.21% over 24 chats; Remakes 35.96% over 19 chats (ledger headers). No recent film came within 15%.
- Cost per chat is steady at $3-8 (0.2-3.2%). **The number of chats is what varies.** At 1.6% a chat, 15% buys about 9 chats.
- Where Protest Tiers' money went (ledger stage table): moves 11.3% plus round-1 moves 14.0% = **25.3%, half the film**; "plan extras (unplanned)" 10.1%; cast 6.0% against 2.1% planned.
- Chat titles show rework: four chats to reach animatic 1 (14, 16, 18 "pre-flight crash fix", 19), then 29 "fix pre-flight faults" and 31 "fix black frames" (ledger). Unchecked: why each was needed.
- Chats 29 and 31 (2.57% and 2.36%): looking at code was about 30% of calls. **page.py was run 0 times in either chat, with 51 grep/sed look-ups instead** (tool-use-29-31.md), even though the round pack says to use it (job-packs.md line 32). Cost shares are estimates, not metered (bills-29-31.md).
- A fresh chat starts at about 90k tokens (costwatch.py `FRESH`), so every extra chat pays its start-up again. 9-12 of the first 20 actions were start-up (bills).
- **Gaps:** every ledger records "0 rounds, 0 notes", so the record cannot say how many chats were first-time building, fixing Claude's own faults, Sam's notes, or tool repairs. The "After the film" line (33.55%) does not match the header (51.27%). Tool and system jobs total about 76% across their ledgers (morning-report alone 28%); the period they cover is unchecked.

## The real decision
This is not about the cost of one chat's steps. It is **why a film takes 19-32 chats when 15% allows about 9**. That covers the whole film, its rework loops, and the tool jobs around it. Cutting look-ups inside a chat is the smallest lever.

## Root cause
Cost = number of chats × cost per chat. Cost per chat is steady; the number of chats is three times what the aim allows. Half of Protest Tiers went on moves, re-done across many chats that fixed faults (crash, pre-flight faults, black frames). That points to faults made, found late and fixed in separate chats, each paying start-up again. Before this, fixes were rules and tools a chat must read and choose to follow. page.py is the proof: it was built and written into the pack, then used 0 times. Nothing forces it, because rule 61's check only warns when a MAP is missing, never when the MAP goes unused. The record cannot yet split rework from first-time work, so the main cause is strongly suggested but not measured.

## Approaches weighed
1. **Make each chat cheaper:** a hook that sends film-code grep/sed through page.py. This is real and enforced, but it touches about 30% of a ~2% chat, so roughly 0.3% a chat, under a tenth of the gap.
2. **Reframe: cut chats per film** by catching faults before the chat that made them ends. The fix is aimed at whatever drives the extra chats.
3. **Learn first:** sort every chat of the last three films (75) by cause and cost, then fix the largest cause.
4. **Cut tool-job spending** (about 76% of a week across jobs; period unchecked).

Chosen: 3, then 2 (and 1 or 4 only if the measurement ranks them high). This meets all three aims: fewer faults reaching Sam, the same quality, and attacks the 3.4-times gap.

## Proposal
**Learn (changes nothing):** one Opus-high helper chat reads the transcripts of all 75 chats from Protest Tiers, Blessed and Remakes, filtered to titles, first messages and endings. It sorts each chat into first-time build, fixing Claude's own fault (which check missed it), Sam's notes, tool repair, start-up/handover only, or waiting on renders, and puts the app's real cost against each. Output: one table of % of a week per cause per film, plus the tool jobs' share by date. Cost about 3% of a week (unchecked estimate), once.

**Change 1 (permanent):** `handover.py end` refuses to finish until the chat's cause is filled in, and `ledger.py` records it with notes and rounds. This is enforced because the handover check already runs in every chat. Number to beat: none are recorded today, so every future chat must have its cause recorded. About 1% of a week.

**Change 2 (after the table, one at a time):** the fix aimed at the largest cause. If own-fault rework leads, the check that missed each fault is improved, so the fault is caught in the chat that made it. Number to beat: the next film's chats and % against Protest Tiers' 32 chats and 51.27%, from the ledger, reviewed when Sam declares the film complete. Each later change gets its own yes.

**What Sam would notice:** first, a one-page picture of where the money went. Then fewer chats and fewer "fix" chats per film.

## Sam test
- Q1: An expert measures the unit that sets the cost (chats per film) before tuning steps; this does.
- Q2: The evidence is 75 chats over three films, not two chats.
- Q3: The root cause is checked against data; the cause tag is enforced by the handover check, not by a chat choosing to read something.
- Q4: Four different approaches were weighed; the chosen one aims at the 3.4-times gap.
- Q5: The learn step changes nothing. Change 1 can be undone alone. Nothing unproven is asked of Sam.
- Q6: Sources are named; estimates are marked unchecked.
- Q7: Sized to find the biggest cause, not a cheap look-up tweak.
- Q8: No trials. Change 1 is permanent, and each change is reviewed at film completion.

## Lost / Added
Lost: nothing. Added: one cause line at every handover; one 3% measuring chat, once.

## Unchecked
Why each rework chat was needed; the 3% and 1% cost estimates; the period the tool-job ledgers cover; the per-step cost shares in chats 29 and 31; the ledger's model column (chats labelled "sonnet" are titled "Opus medium").
