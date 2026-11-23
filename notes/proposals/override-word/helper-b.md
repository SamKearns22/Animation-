# Helper B: the word Override, and the "Locked by Sam" line

## Leak
The title and problem give a solution away: "one code word that skips any check, guard or step" and "drop the line". The film notes ("Chat 47") hold a draft wording too. I set both aside.

## Results
- **One known case:** chat 47 (2fec35f5, Sonnet, 56 steps, 0.42% of a week; ledger). It built animatic v5 and could not send it (notes "Chat 47").
- **Two guards stopped it, of different kinds:**
  1. **The send guard (humancheck.py send_faults) was right.** It wanted a body check record and a critique. Chat 47 had run neither, and had not done shot 4's full-size look or the cuts (its notes). CLAUDE.md line 87, Sam's own rule, says an override "never" skips the checks.
  2. **finish.py lines 209-213 are a false block.** They refuse every animatic while any proposal-route let-through is unsettled, from any chat. Today there are 4, all from chats 9c3f62f3 and e0605414, none from this film (unrouted.md, counted). Every film is blocked now, whatever Sam types.
- **The proposal Stop hook blocks once, then logs** (propose.py line 674), so it never held up a video.
- **The sound mix makes a new file with no body-check record.** `mix()` in grand_theft_autism.py has no humancheck call (checked).
- **Cost:** about one extra chat plus Sam's wait. The whole film is at 97.83% of a week over 52 chats, against 15% (ledger header).
- **Gap:** the send guard logs no refusals, so we can't count how often guards stood between Sam and an ask.
- **"Locked by Sam":** no code reads it, only the rule-proof list (rule_proofs.json). Chat 47 already left it out of messages to Sam.

## The real decision
When Sam wants something now and a guard is in the way, there are three kinds of guard:
- a wait for Sam (his Y, the route, cost-watch red): his word should end it;
- a quality check: skipping it sends unchecked work;
- a false block: fix it at the source.

One word for all three hides the false blocks and cuts quality. Bigger levers sit above the word: the false block, and checks that are not built into the render.

## Root cause
- Guards cannot hear Sam (only costwatch.py reads his prompt).
- finish.py ties every film to the route's unrelated backlog.
- The body check and critique are manual steps after the render, so a chat can end without them. The send guard is then the first place the gap shows.

## Approaches weighed
1. **Universal word:** every guard passes. It sends unchecked work as if checked, conflicts with Statement One and line 87, and masks false blocks.
2. **Reframe:** fix false blocks; make render, then mix, carry the record and prepare the critique, so nothing needs skipping.
3. **Typed Override, by kind:** it ends every wait-for-Sam gate. A quality gate lets the video through only labelled "Not checked yet", with the checks following; it never fakes a record.
4. **Learn first:** sort a week of refusals by kind, then size the changes.

**Chosen:** 4, then 2, then 3, each as a separate change.

## Proposal
**Learn first (changes nothing, about 0.4% of a week):**
- Read modelguard.log, unrouted.md, handover-end.log and a week of chats ("REFUSED").
- Sort each refusal: real fault, false block, or Sam waiting.
- Confirm whether the v5 silent render had a record.

**Then four separate changes, one yes each:**
1. **finish.py counts only this film's let-throughs** (about 0.4%).
   - Kittest: today's state lets GTA through and still refuses a film that has its own let-through.
   - Beat: 0 films refused because of another job (now every film is).
2. **The record survives the mix, and the animatic command prepares the critique pack** (about 0.6%; waits on the learn step).
   - Kittest: render, then mix, then the send guard finds the record.
   - Beat: 0 unchecked animatics handed over.
3. **Override** (about 1.2%).
   - The prompt hook logs Sam's typed word for one ask.
   - Wait gates pass.
   - The send guard passes only with a "Not checked yet: …" line, and the checks run next.
   - Never: fake records, locked shots, a final render without his yes, deleting.
   - handover.py lines 291-294 still catch an Override he never typed.
   - Kittest: replay chat 47.
   - Beat: 0 asks held after Override; 0 unlabelled unchecked sends.
4. **"Locked by Sam" stays in the notes and leaves Sam's messages** (about 0.2%).
   - Reword CLAUDE.md line 20.
   - The reply check flags the phrase; Sam's 10:54 words are its example.

**Total:** about 2.8% once, for all films. Each stuck chat costs 0.4-0.8% plus his wait.

**What Sam would notice:** no films blocked by unrelated jobs; Override gets him the video, marked unchecked; no Locked line in his messages.

**Question:**
1. On Override, may an unchecked animatic reach you, labelled as unchecked, with the checks following? This changes line 87. My pick: Y.

## Sam test
- **Q1:** an expert separates waits, checks and false blocks.
- **Q2:** one case so far; the learn step widens it to a week of refusals across every job.
- **Q3:** code and kittests enforce each change; a faked Override is still caught.
- **Q4:** four different approaches were weighed; this fixes the causes and keeps Sam's word.
- **Q5:** each change undoes alone; Override is logged; no fake records.
- **Q6:** sources are named; gaps are unchecked.
- **Q7:** the root fixes are included, not only the word.
- **Q8:** each change is permanent and reviewed at film end.

## Lost / Added
- **Lost:** the Locked line in messages; line 87's "never the checks" (only on Y to question 1); finish.py's cross-job stop.
- **Added:** an Override log; a "Not checked yet" line; the record through the mix; refusals counted.

## Unchecked
- Whether Sam typed Override in chat 47.
- Whether the v5 silent render had a record.
- Each change's cost.
