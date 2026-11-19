## Leak
Yes: the title gives the remedy (measure a chat's start, set chat size from it), and the facts lead with a fit minimum near 138 steps.

## Results
- Milburn: 15 chats, 1,281 steps; 32.4% by estimate but 22.0% on Sam's app (milburn.json "final"; story/status.md); aim 15%. Estimates ran about 47% high, so fits built on them are scaled high.
- The bins (47 Opus chats, 4.13 to 2.68 per 100 steps): recomputed from notes/ledger/*.json, correct. All are estimates, from 6 ledgers.
- **A chat's start is already measured in real money:** app-costs.tsv near-empty chats cost $0.18-0.56 (Opus, 80-100k) and $0.13-0.46 (Sonnet), so 0.05-0.23% of a week, matching 0.15-0.3% on 11 Nov (chat-size-and-model.md). The fits' 0.58-0.86% "fixed term" is 3-10 times that, so it absorbs other differences between chats.
- **Gap:** the orientation a working chat does before its first edit or render is not counted. stepcost.py reads every step's context (line 150) but keeps only the end.
- **The larger fixed cost is paid every step:** 83k at step 1 (problem file). Derived: 83k × 1,281 steps × $0.18/M = $19, about 7.8% of a week per film, whatever the chat size. CLAUDE.md is about 4-5k tokens of it. tests/stepcost-transcript.jsonl (a real chat) began at 45k, so the base varies by about 40k.
- Derived sensitivity: history grows about 1.4k a step (Milburn: 14 steps→113k, 59→166k, 136→299k). With a start of $0.4-1.0, the best size is 55-90 steps. Chats of 60, 100 or 140 steps differ by 0.2-1.4% of a week per film. The current rule sits in that flat bottom.
- Stale fact: costwatch.py sets amber/red at 250k/370k (17 Nov), not 200k/300k.

## The real decision
The decision is how to cut what every step of a film carries (base × steps), not where a chat stops. Chat length is worth 1.4% at most, the base about 8%; Milburn ended 7 points over the aim.

## Root cause
The question returns because:
- The only numbers are fits on estimates that mix routine work, fixes and failed starts, with no marker for when real work begins. The curve is flat, so noise moves its minimum (42 chats gave 106 steps, 47 gave 138).
- The ledger saves end history, not step-1 context, so the load every step re-reads is never counted.

## Approaches weighed
1. As framed: measure the start, refit chat size. At most about 1.4%.
2. Reframe: shrink what every step carries (tool lists, attached connectors, CLAUDE.md, hook printouts). About 8%.
3. Reframe: fewer steps per film (tool search 6-26% of Milburn chats; learn/search-cost.md).
4. Learn first: record step-1 context and the cost up to the first real work, automatically, for every chat.
Chosen: 4, then 2, one change at a time; chat size unchanged.

## Proposal
**Learn (changes no film):** ledger.py auto (the end-of-chat hook) and stepcost.py add three columns to every chat's ledger row:
- (a) context at step 1;
- (b) steps and % of a week before the first edit, write or render;
- (c) base share: step-1 context × steps × re-read price, as % of the chat.
The hook runs on every chat, so no chat can skip it. Cost: 0.5-1% of a week once (Opus medium), then nothing. It is read at the next film's end review, checked against the app's figures.

**Change 1 (only if (c) is at least 5% of the film):** cut the largest step-1 item first. Beat: step-1 context down at least 25%, no chat blocked for a missing tool, measured by (a). One item per change, each undone alone.

**Change 2 (only if (b) is at least 0.5% a chat):** the figures go to startup-reading.md, which owns start-up reading; no second fix.

**Chat size:** one standing answer for Sam: the rule stays (about 100 steps, up to 150, none under 40). It is checked at each film's end against (a) and (b), and changed only if they put the best size outside 60-140.

Sam notices one end-review line per film.

## Sam test
Q1: An expert measures the mechanism, not a mixed fit.
Q2: Every chat of every film, real app figures as well as estimates.
Q3: Root cause shown; a hook records it, so no chat chooses; success is step-1 context falling.
Q4: Four approaches; the 8% lever beats the 1.4% one.
Q5: The learn step changes no film; each change is one item, undone alone.
Q6: Sources named; gaps listed.
Q7: Sized by the result (at least 25% off the base); refitting chat size is the cheap-but-worse route.
Q8: Permanent columns, no trial, reviewed at film end.

## Lost / Added
Lost: nothing. Added: three ledger columns; one standing chat-size answer.

## Unchecked
What makes up the 83k; the test transcript's date; whether sessions can open without unused connectors; 1.4k-a-step growth beyond Milburn.
