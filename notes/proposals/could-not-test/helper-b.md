# Helper B: "could not test" passing as a line

## Leak
None as a solution. The title frames it as "a line instead of a stop", which steers toward a stop; weighed below, not assumed.

## Results
- The fault reached Sam twice: the name cards (chat 13, note c), then Milburn's own card (chat 18), a repeat note (notes/archive/milburn.md lines 11, 14).
- A third near-miss shipped in the final: "at 1.5 s the caption's top edge still touches the card's bottom edge" (milburn.md line 16). Captions are added later by finish.py, after the film's picture is drawn (milburn.py line 18).
- The stop already exists on paper. Rule 19 (since 13 Nov) says COULD NOT TEST stops the animatic like a fault (film-quality-rules.md line 65). In the code, pre-flight only stops on COULD NOT TEST lines from its gate warnings (preflight.py ~457). Clipcheck's COULD NOT TEST is added to the ordinary fault list (~488), and that list can be named and waved through (finish.py `--faults-named`). Milburn printed it at every round (notes/ledger/milburn/round-0.txt lines 40, 103).
- handover.py (~382) counts it as a fault, but a fault can be named, so this did not stop it either.
- Cover is thin across films: a rough search finds solids/layers in only 3 of 43 film files, and satire_template has only draw_order(t), which runs just the flip check (source/*.py; the search is crude).
- It needs a build: chat 15 called the 48 lines "each needs a build, not a quick edit" (milburn.md line 20). The drawing data does exist: Milburn already paints in back/mid/front/over layers, with the card on "over" (milburn.py lines 266, 293).
- Cost: Milburn came to 22% of a week (app figure, milburn.md line 1). The ledger table reads 32.85% (an estimate). I could not find what the two card rounds cost on their own.

## The real decision
This is not "should COULD NOT TEST stop?" (Sam already said yes on 13 Nov). The decision is: how does every film reach its first animatic with the clipping check actually seeing everything that is drawn, including what finish.py adds on top? It has to be cheap enough that no chat is tempted to name the line instead. A stop on its own just moves the cost to a chat that has no budget for the build.

## Root cause
1. One rule, two paths in the code. The gate's version stops; clipcheck's version is an ordinary fault, and ordinary faults can be named.
2. Each film has to build its own layers or solids. No stage owns that build and no estimate includes it, so naming the line was the only cheap path. The layers Milburn paints in are never handed to the check.
3. The check has a blind spot. Even running, clipcheck sees only picture(t). Captions and the Hook Text come later, so the caption cut would still have got through.
4. The eye check was done on one still frame where the arm was out of the way (line 14). A hand moving over the card has to be checked frame by frame, not on one picture.

## Approaches weighed
1. **Enforce:** make clipcheck's COULD NOT TEST a real stop that cannot be named. Small, but without cover it turns every film into a forced build or a stall.
2. **Reframe, cover by default:** the shared painter, the drawing tool every film uses to paint its layers, hands those layers to clipcheck automatically. COULD NOT TEST then becomes rare, and the stop costs nothing.
3. **Picture-based "stays readable" check:** a film names what must stay readable (cards, faces). The check measures how much of each one is visible in the finished frame, captions included. It does not depend on 3D data.
4. **Learn first:** replay the checks on Milburn's saved code from chats 12, 13 and 18. This shows which approach would have caught each card note and the 1.5 s caption touch.

Chosen: 4 first, then 1, 2 and 3 as separate changes. 1 alone falls short (root cause 2), and 2 alone misses captions (root cause 3).

## Proposal
**Learn (changes nothing, about 1% of a week):** replay Milburn at chat 12, 13 and 18 code. Record three things: whether clipcheck with the painter's layers catches the hand over the card at the noted times; whether anything catches the caption; and how many other films carried COULD NOT TEST, and what faults hid behind it (ledger round files).

**Change 1, the stop (about 0.5%):** clipcheck's COULD NOT TEST joins pre-flight's stop list, and finish.py refuses `--faults-named` while it stands. It is enforced in code, so no chat can choose to skip it. Number to beat: Milburn replayed at animatic 1 must refuse.

**Change 2, cover by default (about 2–3%, only if the learning step shows it catches the hand):** the shared painter provides the film's layers to clipcheck, and satire_template uses it. Number to beat: the chat 12 replay flags the card under the hand at the times Sam noted, and the chat 18 replay comes back clean.

**Change 3, stays readable (about 1.5%, waits on the learning step):** finish.py's overlays (captions, Hook Text) are checked against a "keep readable" list on the finished frames. Number to beat: it catches the 1.5 s caption touch, and it gives no false alarms on the last two films.

Total about 5–6% of a week, once, set against a 15% film. Each later film needs no build. Sam would notice: the card-type notes stop coming, and each "Checks:" line has one less old line in it.

## Sam test
- Q1: Yes. An expert fixes the code path and the coverage, not just the rule's wording.
- Q2: Yes. The scope is every film and the template, tested by replay on real notes.
- Q3: Yes. It is enforced in code, the root cause is found with evidence, and each change has a replay number to beat.
- Q4: Yes. Four different approaches were weighed, and the choice combines them in order, each on its evidence.
- Q5: Yes. Each change can be undone on its own. Changes 2 and 3 wait for the replay results.
- Q6: Yes. Sources are named; the weak ones are under Unchecked.
- Q7: Yes. The stop alone is the cheap trap, and it is not proposed alone.
- Q8: Yes. These are permanent changes, reviewed at the film's end; there is no trial.

## Lost / Added
- Lost: being able to name this line and render the animatic anyway. A film without cover stops until the cover exists.
- Added: a learning replay; a stop that cannot be named; layers from the painter; a readable check on finished frames.

## Unchecked
- Whether clipcheck's drawing-order check would actually flag the hand over the card (this is the learning step's job).
- The cost figures; the 3-of-43 count (rough search); what the card rounds cost; the gap between 22% and 32.85% in the ledger.
