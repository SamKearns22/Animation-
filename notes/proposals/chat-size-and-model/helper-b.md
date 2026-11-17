# Helper B: chat size and model switching

## Leak
None as a solution; the problem file's "one definitive rule" title already narrows the answer to a rule about chat size.

## Results
- Opus chats with a step count: **32, not 42** (my count over notes/ledger/*.json). The bucket figures match the problem file exactly (6/11/10/3/2 chats; 4.3, 3.44, 2.69, 2.43, 2.96 % of a week per 100 steps). Linear fit 0.49 + 0.0226 a step (I got 0.49, the file says 0.42); a quadratic fit has its minimum near 11 steps, so "minimum near 106" depends on the fit and only 5 chats run past 80 steps.
- 16 Nov, Protest Tiers: 24 chats, 1,479 steps, 39.3% of a week (checked, ledger). The whole film so far: 61 ledger rows, **101.3% of a week** against an estimate of 63.5% and an aim of 15% (ledger).
- Moving from chats under 40 steps (4.3 per 100 steps) to chats of 60-100 steps (about 2.6) saves about 40% on those chats. Across 16 Nov, where 10 of 24 chats ran under 60 steps, the saving is about 10-15% of the day: about 4-6% of a week. Real, but the film overspent by about 85% of a week.
- Wrong model: chats 7 and 8 on 16 Nov ran on Opus for look, check, clip and sound (problem file, get_session; unchecked by me). How much of the 39.3% this cost is **not recorded**. That is a gap. Sonnet at 64 steps cost 0.8 against about 1.7 for Opus at 60-80 steps (ledger), so routine work on Opus costs about twice as much.
- Model labels in the ledger are doubtful: Sonnet-labelled chats of 72-79 steps cost 2.2-2.6, about Opus prices (ledger; protest-tiers-costs.md).
- The contradictory advice is real: "a fresh chat for every round and every cost warning" (CLAUDE.md) pushes chats to be short; "too many chats" (budget-job.md) and the 200k split (cost-diagnosis.md) pull the other way.

## The real decision
How a whole film's steps are cut into chats, and which model runs each step. Two bigger levers sit above it: how many steps a film takes (1,479 in one day), and keeping each step on the cheapest model that can do it well. Chat size is the smallest of the three.

## Root cause
1. **Sizing:** three rules each set where a chat ends ("fresh chat per round", amber at 200k, "one stage per chat"), and none of them names a target. So every chat ends at whichever rule it hits first, and short chats pay the start-up cost again and again. The amber line (200k) already falls in the cheapest band (60-80 steps, about 215k history), so the cost watch is right and the "every round" rule is the one that cuts chats short.
2. **Model:** the model check reads words in the next-chat line and matches a fixed list. "Check", "look", "sound" and "clip" are not on it. CLAUDE.md itself puts clips on Opus ("deciding, fixing, clips") and does not name sound at all. So chats 7 and 8 passed the check, and partly followed the written rule. The check guesses from the wording and never looks at the model the chat actually ran on.

## Approaches weighed
1. **One sizing rule:** a chat runs to amber or to the end of its stage. It ends early only for a model change or a question for Sam. "Fresh chat every round" is removed.
2. **Reframe, fewer steps:** attack the 1,479 steps (repeated fix rounds, hand searches through the code) rather than how they are cut into chats. This is the biggest lever and belongs to other proposals.
3. **The model is fixed by the stage:** a table of stage to model in the tool that opens the next chat, plus a check at each chat's start that compares the model it was served (from get_session) with the table.
4. **Learn first:** sort the last two films' chats by job and by the model each was served, then price the wrong-model cost and the short-chat cost before changing anything.

Chosen: 4, then 3, then 1, each on its own. 2 is named, not bundled.

## Proposal
**Learn first (changes nothing):** one Sonnet chat reads get_session for every Protest Tiers and Blessed chat it can open. For each chat it records the model it was served, its job, its steps and its history. Results: the % of a week lost to the wrong model, the true model labels, and the measured cost per step against history size. About 1% of a week.

**Change 1, the model (only if the learning shows over 2% of a week a film lost to the wrong model):**
- CLAUDE.md gets one table, job to model: checks, looks, clips, sound, renders and sending go on Sonnet; fixing and building go on Opus.
- handover.py start reads the chat's own served model and refuses to work on a mismatch. It opens the right chat instead.
- Number to beat: under 1% of a week a film on the wrong model, read from the ledger's served models.
- Cost: about 1% of a week.

**Change 2, the size (after change 1, on the measured curve):**
- One line replaces "a fresh chat for every round": "A chat runs to amber or the end of its stage. It ends sooner only for a model change, a question for Sam or red."
- The handover check flags any chat that ended under 40 steps without one of those reasons.
- Number to beat: under 15% of a film's chats under 40 steps, and cost per 100 steps under 2.8.
- Cost: about 0.5% of a week.

What Sam would notice: one answer about chats that does not change, fewer and fuller chats, and routine work visibly on Sonnet.

## Sam test
- Q1: Yes. An expert would measure the model actually served, not guess from the wording.
- Q2: Two films, every readable chat, rather than one day.
- Q3: Enforced in code at each chat's start, so it does not depend on a chat choosing to follow it. Root causes found with evidence. Each change has a number to beat.
- Q4: Four approaches weighed. The larger lever (steps) is named honestly.
- Q5: The learning step changes nothing. Each change can be undone on its own.
- Q6: Sources named. The 42/32 discrepancy and the minimum point are corrected.
- Q7: Sized to the result. It does not claim chat size alone gets the film to 15%.
- Q8: Permanent once made. Reviewed at the end of the film.

## Lost / Added
- Lost: "a fresh chat for every round" (CLAUDE.md).
- Added: the job-to-model table, a check at chat start against the model actually served, and a flag for short chats.

## Unchecked
- The models served to 16 Nov chats 7 and 8.
- The fit with 42 chats (I found 32).
- 13 Nov $27.73 and $5.80 figures.
- Whether get_session can read chats on the other account.
