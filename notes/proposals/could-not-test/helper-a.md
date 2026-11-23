# Helper A: a check that "could not test" passes as a line

## Leak
None: the problem file states no fix. (The archive's chat 13 line, "a check that could not test stops the animatic", is a fix idea; not used as given.)

## Results
- Milburn: the clipping check printed COULD NOT TEST on every run; it went out with animatics 1, 2, 3 and the final (notes/archive/milburn.md, chats 12, 15, 18).
- Name card: Sam noted it twice (chat 13, chat 18); one of 4 repeat notes out of 33 (notes/proposals/milburn-review.md line 7). Chat 18's fix then put the card under the captions (milburn.md line 16): the fault was readability, not only passing-through.
- Third film in a row: Blessed's clipcheck tested nothing (rule 19, 13 Nov); on Protest Tiers it hid 56 teleports until chat 17 (notes/archive/proposal-route-handovers.md line 187).
- The rules already forbid this. Rule 19: "COULD NOT TEST stops the animatic like a fault"; rule 59: a check the film is not set up for "is a fault to fix before the first animatic, not a note to carry" (guides/film-quality-rules.md). handover.py counts it as a fault too.
- Why it still passed: pre-flight puts the line in with the ordinary faults (source/preflight.py ~488), and one flag, `--faults-named`, waves through every fault at once once they are "named" (source/film_engine.py ~90). It sat among 48-61 named lines (milburn.md lines 13, 20).
- Wider: of the recent films, only the template, Midterminal and Elder Swindon give `draw_order`; Milburn, Strictly Judges, Polanski, Netan-Yahoo, Hutt, Power Crime give no solids or layers at all (scan of source/*.py). So COULD NOT TEST is the normal state, not an accident.
- Cost: not measurable from the record. The ledger rows sum to 32.85% while Sam's app said 22% (notes/ledger/milburn.md vs milburn.md line 1): conflicting. The share spent on the two name-card rounds is not recorded.

## The real decision
Not "should one line stop the animatic" (the rules already say so), but: how does every film, across all its chats, actually get its picture checks run on it, so an un-run check can neither be waved through nor be the usual state? Bigger levers: the check's inputs made automatic, and a readability check (Hook Text's keep-clear list) extended to captions and hands.

## Root cause
1. Enforcement is wholesale: one "named" flag covers every fault, so "could not test" is treated like a known fault.
2. Set-up is by hand: each film must write solids or layers itself, and most don't; the template gives only `draw_order`.
3. The fault Sam saw was "the card can't be read". Even a running clip check might not flag a hand legitimately in front of a card, or a caption over it (unchecked). Chat 13's eye check used one still where the arm was away.
Earlier fixes (7 Nov touch check wording, 13 Nov rule 19) changed what is printed and written, not what the render tool refuses, so they failed.

## Approaches weighed
1. Gate: the render tool never accepts COULD NOT TEST under the blanket flag; only a per-check line in the film's Exceptions with Sam's Y.
2. Reframe (remove the cause): the engine builds `layers(t)` itself from what it draws each frame, so every film gets the clip and order checks with no set-up.
3. Reframe (the fault Sam saw): extend the Hook Text keep-clear list to captions and bodies: name cards, signs and faces listed at planning must stay readable.
4. Learn-first: replay Milburn's chat 13 code with layers supplied; see what clipcheck and a keep-clear check would each have caught.
Chosen: 4 first, then 1, then 2 or 3 as the replay decides.

## Proposal
- **Learn (changes nothing):** one Opus medium chat (~1.5% of a week). Replay Milburn at chat 13's and chat 18's code: (a) with layers added by hand, does clipcheck flag the card; (b) would a keep-clear box on the card flag hands and captions; (c) count COULD NOT TEST lines on the last four films' final code. Result decides change 2.
- **Change 1 (the gate):** the render and pre-flight refuse any COULD NOT TEST under `--faults-named`; it passes only with its own Exceptions line Sam said Y to. Enforced in the tool, not by reading. Number to beat: Milburn sent 4 renders with an un-run check; target 0 per film. Cost ~0.7% once.
- **Change 2 (one only, from the replay):** if (a) catches it, automatic `layers(t)` (2); if only (b), keep-clear for captions and bodies (3). Number to beat: Milburn's 2 faults that reached Sam with an un-run or missing check; target 0. Cost ~2-3% once, ~0 per film after (vs today's hand set-up).
- Total ~4-5% once, against Milburn's 22-33% film and the 15% aim; per film it removes hand set-up.
- Sam would notice: animatics never arrive with "could not test" in the Checks line; name cards and signs stay readable first time.

## Sam test
Q1: Yes; an expert enforces in the tool and removes the cause, not a rule.
Q2: Evidence spans Blessed, Protest Tiers, Milburn and six other film files.
Q3: Root cause found (wholesale flag, hand set-up); enforced in code; measured by counts.
Q4: Four different approaches weighed.
Q5: Change 1 can stop an animatic on a film without data; undone alone; change 2 waits for proof.
Q6: Sources named; costs unchecked where they conflict.
Q7: Not the cheap version: the gate alone would only stop films, so the cause is removed too.
Q8: Permanent changes, reviewed at the film's end; no trial.

## Lost / Added
Added: a hard stop when a check cannot run; one learning chat; then one tool. Lost: the blanket "named" pass for un-run checks; a few minutes' set-up on films until change 2 lands.

## Unchecked
Whether clipcheck would have caught the card; Milburn's true cost (22% vs 32.85%); cost of the two name-card rounds; whether Sam saw the clipcheck line in each animatic message.
