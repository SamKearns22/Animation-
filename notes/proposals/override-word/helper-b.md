# Helper B: Override, and "Locked by Sam"

## Leak
The title states the solution (one word skipping any guard; drop the line); the film notes hold a draft. Set aside.

## Results
- **One case:** chat 47 (2fec35f5, Sonnet, 0.42% of a week; ledger) built v5 and could not send it (notes "Chat 47").
- **The send guard (humancheck.py) was right.** It wanted a body check and a critique, and chat 47 had run neither (its notes). CLAUDE.md line 87, Sam's rule, says an override "never" skips the checks.
- **finish.py lines 209-213 are a false block.** They refuse every animatic while any route let-through is unsettled. The 4 open today all come from chats 9c3f62f3 and e0605414, not this film (unrouted.md, counted). Every film is blocked now.
- **The proposal Stop hook blocks once, then logs** (propose.py line 674), so it never held a video.
- **The sound mix drops the record.** `mix()` makes a new video with no body-check record (checked).
- **Cost:** about one extra chat plus Sam's wait. The film is at 97.83% of a week against 15% (ledger).
- **Gap:** the send guard logs no refusals.
- **"Locked by Sam":** no code reads it (only rule_proofs.json). Chat 47 already dropped it from Sam's messages.

## The real decision
There are three kinds of guard:
- waits for Sam (his Y, the route, cost red): his word should end them;
- quality checks: skipping one sends unchecked work;
- false blocks: fix them at the source.

One word for all three hides false blocks and cuts quality; the false block and render checks are bigger levers.

## Root cause
- Guards can't hear Sam; only costwatch.py reads his prompt.
- finish.py ties every film to the route's unrelated backlog.
- The body check and critique sit outside the render, so a chat can end without them.

## Approaches weighed
1. **Universal word:** sends unchecked work as if checked and masks false blocks (against Statement One and line 87).
2. **Reframe:** fix false blocks; render and mix carry the record and prepare the critique.
3. **Override by kind:** it ends every wait; quality gates pass only with "Not checked yet"; it never fakes a record.
4. **Learn first:** sort a week of refusals by kind.

**Chosen:** 4, then 2, then 3, each a separate change.

## Proposal
**Learn first (no change, about 0.4%):**
- Sort a week's refusals (modelguard.log, unrouted.md, handover-end.log, chats' "REFUSED") into real fault, false block, or Sam waiting.
- Confirm whether the v5 silent render had a record.

**Then four changes, one yes each:**
1. **finish.py counts only this film's let-throughs** (about 0.4%).
   - Kittest: GTA passes; a film with its own let-through is refused.
   - Beat: 0 films refused for another job.
2. **The record survives the mix; the animatic command prepares the critique pack** (about 0.6%; after learning).
   - Kittest: the send guard finds the record after the mix.
   - Beat: 0 unchecked animatics handed over.
3. **Override** (about 1.2%).
   - The prompt hook logs Sam's typed word for one ask.
   - Wait gates pass.
   - The send guard passes only with "Not checked yet: …", and the checks run next.
   - Never: fake records, locked shots, a final render without his yes, deleting.
   - handover.py lines 291-294 still catch an Override he never typed.
   - Kittest: replay chat 47.
   - Beat: 0 asks held after Override; 0 unlabelled sends.
4. **"Locked by Sam" stays in the notes, out of Sam's messages** (about 0.2%).
   - Reword CLAUDE.md line 20.
   - The reply check flags the phrase; Sam's 10:54 words are its example.

**Total:** about 2.8% once, for all films. Each stuck chat costs 0.4-0.8%.

**Sam notices:** no cross-job blocks; Override gets him the video, marked unchecked; no Locked line.

**Question:**
1. May Override send you an unchecked animatic, labelled, with the checks following? This changes line 87. My pick: Y.

## Sam test
- **Q1:** an expert separates waits, checks and false blocks.
- **Q2:** the learn step widens one case to a week, across every job.
- **Q3:** code and kittests enforce each change; a faked Override is caught.
- **Q4:** four different approaches were weighed; this fixes the causes.
- **Q5:** each change undoes alone; Override is logged.
- **Q6:** sources are named; gaps are unchecked.
- **Q7:** the root fixes are included, not only the word.
- **Q8:** permanent; reviewed at film end.

## Lost / Added
- **Lost:** the Locked line in messages; line 87's "never the checks" (only on Y); the cross-job stop.
- **Added:** an Override log; a "Not checked yet" line; the record through the mix.

## Unchecked
- Whether Sam typed Override in chat 47.
- The v5 render's record.
- The cost of each change.
