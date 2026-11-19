## Leak
Yes: the title gives the remedy ("measure what each new chat costs ... and set chat size from it"), and the facts lead with a fit whose minimum is about 138 steps.

## Results
- Milburn: 15 chats, 1,281 steps, 32.4% of a week by transcript estimate but 22.0% on Sam's app (milburn.json "final"; story/status.md). The aim is 15%. Estimates ran about 47% high on this film, so every fit built on them is scaled high too.
- The bins (47 Opus chats, 4.13 down to 2.68 per 100 steps) are right: I recomputed them from notes/ledger/*.json. All 47 are estimates, from 6 ledgers.
- **A chat's start is already measured, in real app money**: notes/ledger/app-costs.tsv has near-empty chats costing $0.18 (Opus, 80k history), $0.49 (Opus, 90k), $0.56 (Opus, 100k) and $0.13-0.46 (Sonnet). That is 0.05-0.23% of a week (WEEK_USD 245), matching the 0.15-0.3% measured on 11 Nov (chat-size-and-model.md). The fits' "fixed term" of 0.58-0.86% is 3-10 times that, so it is soaking up other differences between chats.
- **The gap**: nobody has counted the orientation a working chat does (reading the handover, the pack and the notes) before its first edit or render. stepcost.py already reads every step's context (line 150) but saves only the end history.
- **The bigger fixed cost is paid on every step, not once per chat**: 83k tokens at step 1 (problem file). Derived: 83k × 1,281 steps × $0.18/M = $19, about 7.8% of a week per film, whatever the chat size. CLAUDE.md is 12k characters (about 4-5k tokens) of that; the rest is app instructions, tool lists and hook output (split unchecked). tests/stepcost-transcript.jsonl, a real chat, started at 45k (30k re-read + 15k written), so the base varies by about 40k tokens.
- Derived chat-size sensitivity: history grows about 1.4k tokens a step (Milburn: 14 steps→113k, 59→166k, 92→256k, 136→299k). With a start of $0.4-1.0, the best size is 55-90 steps. At 1,281 steps, chats of 60, 100 or 140 steps differ by $0.4-3.5, which is 0.2-1.4% of a week. The current rule already sits in that flat bottom.
- Nothing in the record ties chat size to Sam's notes or to faults reaching him.
- The problem file is out of date: costwatch.py sets amber/red at 250k/370k (Sam's Y, 17 Nov), not 200k/300k.

## The real decision
The real question is how to cut the cost every step of a film carries (base context × steps), not where a chat should stop. Chat length is worth 1.4% of a week at most, the base about 8%, and Milburn finished 7 points over the aim. The judge on chat-size-and-model.md already called chat length "the smallest of the three levers".

## Root cause
The question keeps coming back for two reasons. First, the only numbers are fits on estimated costs that mix routine work, fixes and failed starts, with no marker for when real work begins. The curve is flat, so noise moves its minimum: 42 chats gave 106 steps, 47 chats gave 138. Second, the ledger records end history, not the context at step 1, so the fixed load that every step re-reads is never counted. Advice has swung because each answer came from a noisy fit, not from a measured mechanism.

## Approaches weighed
1. As framed: measure each chat's start, then refit chat size. The most it can gain is about 1.4%.
2. Reframe: shrink what every step carries (tool lists, attached connectors, CLAUDE.md, hook printouts). About 8% is at stake.
3. Reframe: fewer steps per film (tool search is 6-26% of Milburn chats). This overlaps learn/search-cost.md.
4. Learn first: the ledger records, for every chat automatically, its context at step 1 and its cost up to the first real work. Then decide.
Chosen: 4, then 2, one change at a time. The chat-size rule stays as it is.

## Proposal
**Learn (changes no film):** stepcost.py and ledger.py auto (the hook that runs when every chat stops) add three columns to each chat's ledger row:
- (a) context at step 1;
- (b) steps and % of a week before the first edit, write or render;
- (c) base share: step-1 context × steps × the re-read price, as % of the chat.
Because the hook runs on every chat, no chat has to choose to do it. It gets a test in `stepcost.py test`. Build cost: about 0.5-1% of a week, once, on Opus medium. After that it costs nothing per chat. The results are read at the next film's end review across all its chats, checked against the app's figures.

**Change 1 (only if (c) is at least 5% of the film):** cut the largest single item in the step-1 context first. The number to beat is step-1 context down at least 25%, with no chat blocked for a missing tool, measured by column (a). One item per change, and each can be undone on its own.

**Change 2 (only if (b) is at least 0.5% a chat):** hand the figures to startup-reading.md, which already owns start-up reading, rather than building a second fix.

**Chat size:** Sam gets one standing answer: the rule stays (about 100 steps, up to 150 to finish a stage, none under 40). At each film's end review it is checked against (a) and (b). It is changed only if they put the best size outside 60-140 steps.

What Sam would notice: nothing in the films; one line per film in the end review.

## Sam test
Q1: An expert measures the mechanism (the per-step load), not a fit on mixed chats.
Q2: Covers every chat of every film from now on, using real app figures as well as estimates.
Q3: Root cause shown; a hook records it, so no chat can skip it; success is step-1 context going down.
Q4: Four approaches weighed; the 8% lever beats the 1.4% one.
Q5: The learn step changes no film; each later change is one item and can be undone alone.
Q6: Sources named; derived figures marked; the rest listed under Unchecked.
Q7: Sized by the result (cut the base at least 25%), not by price; refitting chat size would be the cheap-but-worse route.
Q8: Permanent ledger columns; no trial; reviewed at film end.

## Lost / Added
Lost: nothing. Added: three ledger columns per chat, and one standing chat-size answer.

## Unchecked
What makes up the 83k (tool lists vs app text vs hooks); the date of the test transcript; whether a session can be opened without unused connectors; the 1.4k-tokens-a-step growth beyond Milburn.
