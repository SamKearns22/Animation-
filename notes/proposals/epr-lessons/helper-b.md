# Helper B: Statement One lessons from building EPR

## Leak
None. The problem file gives no fix. It does call EPR "unusual", and I tested that instead of assuming it.

## Results
- Spent 101.29% of a week across 61 chats. The first plan was 21.5% (ledger .md; notes "First plan").
- **Length almost tripled after it was planned.** The plan was 4 s per tier, 16 s plus a 1.6 s sign-off (plan-r0 line 153). Round 1 asked for 4/6/8/10 s tiers and a new three-shot end scene (notes R2, R4). G1 and A2 added 2-3 s each. The final film is 43 s (notes line 12). At the planned rate per second, 43 s costs about 53%. The remaining overrun (roughly 48 points) is cost per second, not length (my arithmetic).
- **Two-thirds of the cost came after animatic 1.** Animatic 1 closed at 34.21%, so 67.1 of 101.29 (66%) came after it (ledger). Blessed shows the same pattern: animatic 1 at 21.02 of 62.21 (66%; ledger/blessed.md). Remakes does not: about 33.7 of 35.96 was spent before its animatic (ledger/remakes.md rows). So this is not unique to EPR.
- **Notes:** Round 1 had R1-R5 plus 6 answers. From round 2 on there were about 105 items: O1-O9, S0-S8, G1-G23, F1-F24, A0-A37 (my count of IDs in notes/protest-tiers.md). Round 2 cost 47.6% against 0.865% planned.
- **Design notes reached Sam only once the film moved.** Examples: France "camera too low" (F1) reversed framing lesson F2 ("low = the front line towers", plan-r0 line 64); Albania "perspective flattens" (A1); three Albania crowds re-staged (A4); timing changes (A7, F23); added length. The pencil roughs were stills and were sent (handovers line 48). They did not catch these.
- **Repeated notes (rule 30):** 6, namely G4, F15, F16, F18, F20 and A30 (notes).
- **The largest fault class was "everyone the same".** O4, F5, F9, F15, F16, F18, A17, A18 and G21 are 9 notes, 3 of them repeats. Next were contact and clipping (G3, G4, G14, G20, A25, F22: 6) and "pasted on" (A9, A19, A20, A27: 4). This is my reading of the note wording.
- **Gaps in the record:** every ledger row records 0 notes and 0 repeats. The "After the film" line says 33.55%, against 101.29% actually spent, so the end-of-film review would compare the wrong number. Cost per note cannot be measured yet.

## The real decision
The decision is not "what went wrong on an odd film". It is **where in the whole film a design choice gets made, and at what price.** In two of the last three films, two-thirds of the money went on decisions and faults found after the first moving picture. Two levers are bigger than "research" or "crowds":
1. Settling length, camera and gags before anything is built in code.
2. Stopping a known fault class before Sam sees it.

Per-chat overhead (history re-reading, code search) is already being handled by adopted proposals.

## Root cause
1. **Sam first sees the film's shape, its timing and its movement only in animatic 1.** By then cast, sets and moves are built in code, so every taste change becomes a rebuild spread across many chats. Round 2 ran on 16 Nov, about 24 chats at roughly 1.6-2.4% each, ending with 200-270k tokens of history (ledger).
2. **The research lessons were built without first being seen in motion.** F2 shows this: built at the low camera, then reversed in round 2.
3. **No automatic check covers sameness.** Fixes tuned single numbers (F9 changed only the rate, within 15%), so the notes came back again (F16, F18).
4. **The ledger cannot count notes,** so none of this was visible while the film was being made.

## Approaches weighed
- **A (reframe):** Settle the shape on a *timed rough* before the cast is built. These are pencil frames held to the beats at full length, with each shot's camera height and every gag. Sam's notes on length, framing and gags land there, at about 1% instead of 20-47%.
- **B (learn first):** Sort every note from EPR, Blessed and Remakes into design change, visible-fault class, or repeat. Give each note a cost (the "built chat N" tags times that chat's ledger cost). This shows which lever is largest.
- **C:** An automatic "sameness" check. Within each group, measure how much faces, skin, clothes, timing and pose vary, and refuse an animatic when they are too alike.
- **D:** Price every note batch before building it. This sits inside the open "estimates" proposal, and X1 put it on hold for EPR.

**Chosen: B first, then A and C, each as its own yes.**

## Proposal
1. **Learn (changes nothing; about 1.5% of a week; one Opus medium chat).** Build the note table for the three films: class, count, cost and rule-30 repeats. Also record why the "After the film" figure is wrong. Result: one sheet. It decides whether A or C comes first.
2. **Change 1, if design notes after animatic 1 are the largest cost class in at least 2 of 3 films.** Make the timed rough a stage, using the pencil kit that already exists (`pencil_cartoon`). It runs to final length, includes each research lesson as it will look, and is shown as a short clip. **Enforced:** the handover check refuses to open the cast stage until a "Y" on the timed rough is recorded in the notes. **Number to beat:** the share of film cost after animatic 1 falls from 66% to under 40%, and design notes after animatic 1 fall by half compared with EPR's count. **Cost:** about 1-2% per film. EPR's still roughs cost about 2.5% (ledger chats TWFKPUgZ and xQrZzs91). **Sam would notice:** a moving pencil film to note before any colour.
3. **Change 2, separately, if the sameness class leads the faults.** A sameness check in `check`, which refuses an animatic below a set spread. **Number to beat:** 9 sameness notes on EPR, down to 0 across the next two films. **Cost:** about 2% to build once.
4. **Change 3, separately:** the ledger records notes and repeats per round, and fixes the "After the film" figure. Its number: no film ends with 0 notes recorded.

Each change is permanent once adopted and is reviewed at the end of each film.

## Sam test
- Q1: An expert would fix *where* decisions get made, and measure first. That is what this does.
- Q2: The evidence covers three films, not only EPR, and the 66% pattern is checked in two of them.
- Q3: The changes are enforced by the handover check and by `check`, not left to a chat's reading. The root cause comes with evidence and each change has a number to beat.
- Q4: Four different approaches were weighed. The chosen one goes for the biggest share of the cost.
- Q5: The learning step changes nothing. Each change is a separate yes and can be undone alone.
- Q6: Sources are named for every fact. Classifications are marked as my reading.
- Q7: Sized by the result (cost after the animatic), not by price. The cost is stated.
- Q8: Nothing is a trial. Each change is made properly and reviewed when the film is declared complete.

## Lost / Added
- **Added:** one sorting chat (about 1.5%). If adopted: a timed-rough stage (about 1-2% per film), a sameness check, and note counts in the ledger.
- **Lost:** none of the joke or content. Building cannot start before the rough has its Y.

## Unchecked
- The note classification and per-note costs are approximate until step 1 is done.
- Whether a timed rough would have drawn F1 or A1 out of Sam earlier.
- The causes behind Blessed's post-animatic cost.
- Whether propose.py review has been run for EPR.
