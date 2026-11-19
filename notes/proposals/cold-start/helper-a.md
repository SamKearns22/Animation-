# Helper A: cold start

## Leak
The title gives away the answer ("measure ... and set chat size from it"). I set that aside. Two of its facts are out of date: Sam said Y on 17 Nov to the chat-size rule (notes/proposals/chat-size-and-model/sam.md), and the cost warnings are 250k/370k, not 200k/300k (.claude/hooks/costwatch.py line 28).

## Results
- Milburn: 15 chats, 1,281 steps, 32.4% by estimate, 22.0% on Sam's app (milburn.json, rechecked). 11 Opus chats cost 29.15%; 4 Sonnet chats (14, 40, 117, 28 steps) cost 3.25%. The estimate runs 1.47 times Sam's meter, so every % figure here may be about a third too high.
- 47 Opus chats: the cost per 100 steps and the fits in the problem file match my recount. From 70 to 130+ steps the curve is flat: 2.82 to 2.68, within 5%. Running every Milburn Opus chat at the lowest point would save about 0.14 per 100 steps x ~1,000 steps = ~1.4% of a week a film. The under-40 group is mostly tool and proposal jobs, not film chats (cost-fixes, proposal-route, cost-diagnosis rows).
- A real start, measured directly (tests/stepcost-transcript.jsonl, Opus, a usage figure on every step): 78k tokens in context after 2 calls, $0.41 = 0.17% of a week; 0.24% by step 8. About 30k of the very first step was already cached, so not all of the start is paid fresh. That is a third to a quarter of the fits' fixed term (0.58-0.86%). x15 chats = ~2.5-3.6% of a film, before re-reading film files.
- Not in the record: how many steps and how much cost a film chat spends re-learning what the last chat already knew (its film code, notes, pictures). That is the part of a cold start the size decision turns on, and it is a gap.
- Faults or notes caused by handovers: the ledger's "notes" field is 0 on every Milburn row (unchecked whether that is true).

## The real decision
Not "how long is a chat" (Sam settled that on 17 Nov, and the curve is flat), but what a handover really costs a whole film: the fixed start (measured, ~0.2%) plus the re-learning (unmeasured). Two bigger levers sit outside this problem: how many steps a film takes (1,281), and how much history each step adds (tool search alone is 6-26% of Milburn chats' cost).

## Root cause
The size rule came from curve fits on chat totals. Totals mix the start with the kind of work, so the fixed term is confounded (the problem file says so). stepcost.py already reads every step's usage, but ledger.py keeps only the steps, the history at the end and the kind shares, so the start is never stored. And nothing marks "first real work", so the re-learning cannot be told apart from the work itself.

## Approaches weighed
1. **Learn first (chosen).** stepcost measures each chat's start automatically at its end. Nothing changes until a film's figures are in.
2. **Reframe: a warm handover.** The handover names the exact files, line ranges and pictures the next stage needs, so the next chat reads them once instead of searching. This makes a start cheaper rather than rarer.
3. **Handover by sum, not steps.** The cost watch says "hand over" once the extra re-reading still to come is more than a measured fresh start. Needs a guess of steps left; it replaces Sam's rule.
4. **Leave chat size alone.** Spend the effort on steps per film and history added per step (finder-use, rework). This is already the bigger lever and has its own proposals.

## Proposal
**Learn (changes nothing).** Add four fields to stepcost/ledger.py auto, written on every chat's row by the Stop hook (the step that runs when a chat ends), so no chat has to choose to do it: context at step 1; steps and % of a week until first real work (the first edit or write outside notes, or the first render); the cost of reading files the film's previous chat also read; and the cost of the whole start. The existing test fixture checks it. Build ~0.5-1% of a week once; 0% per film after that. The result goes into the end-of-film review.

**Change, only if the numbers call for it, one at a time:**
1. If re-learning plus the start averages over 0.5% a chat (over ~7% of a 15-chat film), make the warm handover (approach 2) a refusal in handover.py end: no handover without its read list. Number to beat: start cost per chat down by half, Sam's notes and repeat faults no higher than on the last two films. ~1% of a week.
2. Only if the measured start shows the fitted lowest point outside 70-150 steps does chat size go back to Sam, through the route. Otherwise the 17 Nov rule stands and the question is closed. That matters, because Sam has had mixed answers before.

What Sam would notice: nothing, until the film-end review line "a new chat's start cost X% of the film".

## Sam test
Q1: An expert measures the start on each step's usage before tuning on fitted totals; done here.
Q2: Every chat of the next film, measured automatically. Better than old fits; Milburn transcripts are gone.
Q3: A hook writes it, so no chat can skip it. Root cause shown (start not stored, no "real work" marker).
Q4: Four different approaches weighed; the bigger levers are named and left to their own proposals.
Q5: Learning changes nothing; each later change can be undone alone, and the 17 Nov rule is kept.
Q6: Figures rechecked against milburn.json, the ledgers and the test transcript; gaps marked.
Q7: Sized to the decision; no cheap one-off guess at the start cost.
Q8: Permanent fields in the ledger; each change reviewed when Sam calls the film complete.

## Lost / Added
Lost: nothing.
Added: four start-up figures on every ledger row (~0.5-1% once); possibly later a required read list in handovers.

## Unchecked
Whether the 30k first-step cache hit happens in every session; why the estimate is 1.47 times the app; whether one tool-job transcript stands for film chats; the ledger's zero notes per chat.
