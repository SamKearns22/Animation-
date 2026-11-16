# Helper B: EPR build lessons

## Leak
None.

## Results
- **Total:** 101.29% of a week over 61 chats, against a first plan of 21.5% (ledger; notes "First plan").
- **Length:** planned at 16 s (plan-r0 line 153); round 1 added 4/6/8/10 s tiers and a new end scene (R2, R4); the final film is 43 s (notes line 12). At the plan's rate per second, 43 s ≈ 53%, so about half the overrun is length.
- **After animatic 1:** 66% of the cost (34.21 of 101.29 spent before it). Blessed is the same, 66% (21.02 of 62.21). Remakes is not (~94% spent before). So this is general.
- **Notes:** about 105 from round 2 on (O, S, G, F, A items; my count). Round 2 cost 47.6% against 0.865% planned.
- **Design notes came only once the film moved:** F1 reversed research lesson F2 (plan-r0 line 64); also A1, A4, A7, F23. The still pencil roughs (handovers line 48) missed them.
- **Repeats (rule 30):** 6 (G4, F15, F16, F18, F20, A30).
- **Fault classes (my reading):** "all the same" 9 (O4, F5, F9, F15, F16, F18, A17, A18, G21); clipping 6; "pasted on" 4.
- **Gaps:** the ledger shows 0 notes and 0 repeats for every chat, and "After the film" reads 33.55%, not 101.29%. Cost per note cannot be measured yet.

## The real decision
Where in a whole film design choices get made, and at what price. In 2 of the last 3 films, two-thirds of the money went after the first moving picture. Two levers are bigger than "research" or "crowds": settling length, framing and gags before anything is built in code, and stopping the largest fault class before Sam sees it. Per-chat overhead is already covered by adopted proposals.

## Root cause
1. Sam first sees timing and movement at animatic 1, after everything is built in code. Each taste note becomes a rebuild across many chats (about 24 on 16 Nov, at 200-270k history each).
2. Research lessons were built without being seen moving (F2, then F1).
3. No check covers sameness. Fixes tuned one number (F9: rate only), so the notes returned (F16, F18).
4. The ledger cannot count notes.

## Approaches weighed
- **A (reframe):** settle the film's shape on a *timed rough* before the cast is built: pencil frames held to the beats at full length, with each shot's camera and every gag.
- **B (learn first):** sort and cost every note from EPR, Blessed and Remakes ("built chat N" tag × that chat's ledger cost).
- **C:** an automatic sameness check in `check`.
- **D:** price each note batch before building (the open estimates proposal).

Chosen: B, then A and C, each as its own yes.

## Proposal
1. **Learn** (changes nothing; ~1.5%; one Opus medium chat): one note table (class, count, cost, repeats) for three films, plus why "After the film" is wrong. It decides which change comes first.
2. **Change 1** (if design notes after animatic 1 are the largest cost class in at least 2 of 3 films): a timed-rough stage using the existing pencil kit, sent as a clip.
   - **Enforced:** the handover check won't open cast without Sam's recorded Y on the rough.
   - **Beat:** cost after animatic 1 under 40% (now 66%); design notes after it halved against EPR.
   - **Cost:** ~1-2% per film.
3. **Change 2** (separately, if sameness leads the faults): `check` refuses an animatic when a group's faces, clothes and timing vary too little.
   - **Beat:** 9 such notes to 0 over the next two films.
   - **Cost:** ~2% once.
4. **Change 3** (separately): the ledger counts notes and repeats per round, and "After the film" is fixed.
   - **Beat:** no film ends with 0 notes recorded.

**Sam notices:** a moving pencil film before any colour.

## Sam test
- **Q1:** moves decisions earlier and measures first.
- **Q2:** three films checked, not one.
- **Q3:** enforced by the handover check and `check`; each change has a number to beat.
- **Q4:** four different approaches weighed.
- **Q5:** learning changes nothing; each change can be undone alone.
- **Q6:** sources named; my readings marked as mine.
- **Q7:** sized by the cost after the animatic, not by price.
- **Q8:** no trials; reviewed when the film is declared complete.

## Lost / Added
- **Added:** a sorting chat; if adopted, a rough stage (~1-2% per film), a sameness check, note counts in the ledger.
- **Lost:** no content. Building waits for the rough's Y.

## Unchecked
- Note classes and costs, until step 1 is done.
- Whether a timed rough would have surfaced F1 or A1 earlier.
- What drove Blessed's cost after its animatic.
- Whether propose.py review has been run for EPR.
