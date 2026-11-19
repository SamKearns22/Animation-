# Helper B: cost-other

## Leak
The title and the "prototype split" fact give away the idea (split "other" inside the step-cost tool). Ignored.

## Results
- **The dollar estimate is right; the % is not.** Real app cost (get_session usage, read this chat) for 13 of 15 Milburn chats: $74.59; the ledger's transcript estimate for the same 13: $73.84 (within 1%). Two sessions (5c55685c, ce8f146c) were not found. So the ~47% gap to Sam's 22% sits in the week size (WEEK_USD 245, "PROVISIONAL", costwatch.py:26) or the meter window, not in the estimate. Other jobs ran on 17-18 Nov too (morning-report, proposal-route, cost-fixes ledgers), so Sam's 71→93% may not be Milburn alone.
- **Real split of those 13 chats** (app token counts x costwatch prices): re-reading 45%, writing new context 30%, output (Claude's words, thinking, code it writes) 25%. Output is 16-31% in every chat.
- **Start-up floor (estimate):** ~90k at step 1 (costwatch FRESH; 83k in this chat; step-1 size is not stored per chat) re-read over 1,176 steps ≈ $17.7, plus writing it once a chat ≈ $8: about a third of the film.
- **Rework is invisible.** Titles show at least 6 of 15 chats were note fixes (chats 4, 6, 9, 10, 11, 13), yet the ledger says "0 rounds, 0 notes, 0 repeated" (milburn.md). The record cannot say what fixes cost: a gap.
- Plan was 24% before work began; sets stage spent 16.7% against 1.8% planned (milburn.json stages).

## The real decision
Not "label the leftover" but: which block sets a film's cost (start-up floor, Claude's own output, or fix chats), measured for the whole film, so the next change hits the biggest. Fix chats and the floor outweigh searches (25%).

## Root cause
"Other" is a leftover by design: stepcost.py measure() charges only tool results and the output that asked for calls. It never names the start-up context re-read at every step, Claude's own messages re-read later, or calls kind_of() does not know (Edit, Write, python, git). The 13 Nov diagnosis found the same blocks; the 16 Nov start-up trim was never shown to work because step-1 size is not recorded.

## Approaches weighed
1. **Label:** stepcost names start-up floor, own output, edits/writes, runs.
2. **Reframe, learn-first:** one table of Milburn in real dollars by block and by chat purpose (new work, note fix, hand-over), from get_session and titles.
3. **Cut the floor now:** trim tool list and start-up text. Acts before knowing it is the biggest.
4. **Fix the yardstick:** settle the week size. Already in notes/proposals/estimates.md; not repeated.
Chosen: 2 first, then 1, then the purpose record, one at a time.

## Proposal
- **Learn (changes nothing; Sonnet; ~1% of a week):** finish the table above for all 15 chats: real $, step-1 context, output, and purpose. Result: each block's share of Milburn. It decides which lever comes next.
- **Change 1, naming the blocks:** stepcost splits "other" into start-up floor (step-1 context x every later read), Claude's own output, edits/writes, runs, and leftover; stores step-1 size. Enforced by the Stop hook (runs on every chat). Number to beat: leftover under 15% of each chat on the next film (was 58-87%); totals within 5% of get_session on three sampled chats. ~1.5% of a week, Opus medium.
- **Change 2, after Change 1 shows clean:** the ledger records each chat's purpose and notes count from its hand-over, so fix-chat cost is a number. Enforced by handover.py end refusing a row without a purpose. Number to beat: every chat of the next film has one; fix share known. ~1.5%.
- The cost-cutting change (floor, output or fixes) is proposed only after these, against its own measured share.
- Total ~4% of a week once, against 15% a film. Sam would notice one plain table "where Milburn's $80 went", then a cost line in each hand-over that names its blocks.

## Sam test
- Q1: an expert measures real dollars by block before cutting; done here.
- Q2: whole film, real app figures, all chats.
- Q3: root cause named; enforced by hooks, not chat choice; numbers to beat set.
- Q4: four different approaches; the leftover-label alone is rejected as too narrow.
- Q5: learning changes nothing; each change undoes alone; Sam trusts no untested cut.
- Q6: sources named; estimates marked.
- Q7: sized by the result (cost by block and purpose), not price; no cheap trap.
- Q8: changes are permanent, each reviewed at the next film's end.

## Lost / Added
Lost: nothing in the films. Added: one table, two record changes, ~4% once.

## Unchecked
Week size; Sam's meter window; the two missing sessions; whether "Chat 18" (named in chat 13's status) means chats missing from the ledger; step-1 size of each Milburn chat.
