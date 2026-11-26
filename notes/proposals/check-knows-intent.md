# Proposal: Checks that understand what the scene is trying to do

Status: adopted, option 1 (Sam, 26 Nov, R8 chat: "1"); step 5 (the three resting-hand faults) discarded: Sam: "I don't see anything wrong their resting hands, discard."

## Problem
The picture checks (hands, overlaps, rests, pop-ins) judge shapes only. They cannot tell something the scene intends (a crowd running past each other, guests through a doorway, hands behind a runner's body) from a real drawing mistake. They flag the intended, and each "this is fine" answer is tied to one person, second and exact wording, so when the drawing changes the same intended thing comes back as a new fault. Sam (26 Nov, chat 36): "The checks can't be stupid. They need to understand when something is intentional in the image. They need to be able to ask the image and the screenplay, when they are unsure, 'is this normal in the context of what we are trying to achieve'". Checks must also never lock out requested work (rule 93).

## Facts
- Chat 36 animatic: 9 picture-check faults; 3 matched an old answered row (source/waivers.py split, matching by exact or wildcard wording), 6 did not (3 'hand over another body' on crowd figures at 11.08, 26.42, 29.33 s; 3 RESTS). Looked at the first three frames: ordinary crowd overlap, except a guest half hidden behind Blair's neck at 29.33 s whose bent arm reads oddly. RESTS not looked at.
- Answered rows (notes/brexit-is-done.md '## Exceptions', rows 116-135) are matched by person and wording, with 'looked at' text; none states the scene's purpose in a form a check can read.
- The film already holds intent: the brief and screenplay (story/ and notes brief checklist), the acting list (source/acting.py, story/brexit-is-done-moves.txt), background action lists (brexit_is_done_action.py site_actors, room_actors). The picture checks (preflight.picture_faults) read none of these.
- A check cannot look at a picture and decide by itself; a Claude helper can look at a still and read a text (critique.py, rule 89, does this for pictures).
- Earlier animatics: chat 17 (25 Nov) held by 16 faults, chat 22 and 26 sent; whether picture checks ran in 22 and 26 is unchecked.

## Record
notes/brexit-is-done.md
notes/archive/brexit-is-done-handovers.md
source/waivers.py
source/preflight.py
source/critique.py
source/brexit_is_done_action.py
guides/film-quality-rules.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 0df0d5bcb02a95b5 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the Facts line "a Claude helper can look at a still and read a text (critique.py, rule 89, does this for pictures)" points at one remedy (a picture judge), and Sam's quoted words ("ask the image and the screenplay") point the same way. V2 and V3 named it and weighed it; V1 did not.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 2 | 3 | 5 | 14 |
| V2 | 4 | 4 | 3 | 4 | 4 | 19 |
| V3 | 5 | 4 | 4 | 4 | 4 | 21 |
## Sam test
Q1: Yes. An expert puts the meaning where the action is drawn (the drawing code already says it with its "allow" marks, checked: brexit_is_done_action.py 404 and 896), not in lists typed after the fault; a picture judge only for what that leaves unclear.
Q2: Yes, after the fix: the learn step sorts every picture-check flag of the whole film (chat 17's 16, chat 20's 3, chat 36's 9), not one chat. V3 wrongly counted chat 19's 34 pre-flight depth lines as picture-check flags; corrected.
Q3: Root cause shown with evidence (HANDS_OK covers only 'no hand' and '*workers 2', checked in handcheck._allowed and brexit_is_done.py 129; the faults name workers 3, 4, 5 and 'over' kinds). Runs in code on every frame; a test proves it both ways (quiet on meant, loud on real). Weak spot: a chat could still mark a real fault "meant" at the source; hence the never-excusable list and the "meant:" line still printed.
Q4: Yes: intent at source, picture judge, better depth test, fix the drawing, learn first, all weighed.
Q5: Each change has its own yes and comes out alone; nothing is trusted until it passes the saved examples. Risk left: intent marks could hide a real fault; met by printing them as "meant: …" and never excusing sinking, hovering or passing through.
Q6: Facts checked against the record (the 9 lines, the HANDS_OK rows, the allow marks, the 55.84% spent). Costs are estimates, marked unchecked.
Q7: Sized by the result (meant flags to 0, real flags missed 0), not by price; the cheap trap (a typed purpose line per scene, V1) is rejected.
Q8: Permanent shared change with its test, reviewed when Sam declares the film complete; no trial.
## Pick
V3
## Why
V3 finds the real root cause: the meaning is already written where the action is drawn, but the checks cannot read it, so it is copied by hand into rows keyed to one name and wording that break on every redraw. It also sees that the 3 RESTS flags are real drawing faults (sinking 3-4 cm), the same kind as Sam's note 19, so no amount of "understanding intent" may excuse them. V2 is sound and careful but its first lever (depth in metres) rests on an unchecked fact (whether plan positions reach the hand check) and does nothing for doorway or pop-in meaning; V1 is the hand-written list again and cannot judge. Taken from V2: every change gets its own yes, explicitly; a "meant" flag still prints as "meant: …", never hidden; the picture judge saves nothing and judges afresh each animatic; the depth test kept as the fallback for 'over' flags with no intent mark.
## Faults in the pick
- F1 [fixed] V3 counted chat 20's "34 answered" as picture-check flags; they were pre-flight depth-order lines (handovers, chat 17 and 19). The sort now covers picture-check flags only: chat 17's 16, chat 20's 3, chat 36's 9.
- F2 [fixed] Changes were not explicitly separate yeses; now each is its own yes.
- F3 [fixed] Intent marks could silence a flag completely; now a meant flag still prints as one short "meant: …" line.
- F4 [named] Sam asked for checks that "ask the image and the screenplay" when unsure; the picture judge comes only if the sort shows unclear flags left after change 1. If none are left, it is not built.
- F5 [named] Costs are estimates from earlier build chats, unchecked; the film already stands at 55.84% of a week against 15%.
- F6 [named] Whether the 29.33 s arm is a real fault is unknown until the sort looks at it full size.
## Final version
Learn (changes nothing, Sonnet): look at the first still of every picture-check flag this film has had (chat 17's 16, chat 20's 3, chat 36's 9) at full size; mark each meant, real or unclear, naming what in the brief, screenplay or action list makes it meant. Save them as examples. This gives the number to beat. About 1.5% of a week (unchecked).

Change 1 (own yes): the shared actions that hide or overlap limbs on purpose (side-on run, crowd pass, doorway entry) mark each person in each frame with what is meant (person, limb, kind, cause), building on the existing allow marks. The hand, overlap and pop-in checks read these marks; a flag that fits prints as one "meant: …" line, never as a fault and never hidden. Never excusable: through a body, sinking, hovering (added to the shared never-allowed list). A mark made in one film's code only needs an Exceptions row and a "move to shared" line. Test: quiet on every "meant" example, still flags every "real" one (note 19, chat 36's three RESTS, May's finger, 29.33 s if real). Beat: meant faults on chat 36's animatic 0, real faults silenced 0. The old HANDS_OK and pop-in rows for these actions are removed once the test passes. About 2.5% (unchecked).

Change 2 (own yes, only if the sort shows unclear flags left): a fresh picture judge gets each remaining flag's circled still, the screenplay line and the action, answers meant / fault / can't tell; it saves nothing and judges afresh every animatic; its answer is advice on the Checks line. Trusted only when it agrees with the sort and calls no real example meant. About 2% once, 0.2% per film (unchecked). Fallback for 'over another body' flags with no mark: the depth test from the plan, if plan positions reach the check.

The three RESTS faults are fixed in the drawing (shared acting kit) whatever happens.

Reviewed against the film's results when Sam declares it complete.
## For Sam
### Option 1: the meaning travels with the drawing
Problem: The picture checks only see shapes, so they flag things you meant (runners' hands behind bodies, guests in a doorway), and each "this is fine" answer is tied to one person and one second, so it breaks every time the drawing changes.
1. First, one look through every flag this film has had, each picture full size, sorted into meant, real or unclear. Nothing changes yet.
2. On your yes: each shared movement (running side on, a crowd passing, guests through a door) carries a note of what is meant, and the checks read it. A meant flag shows as one short "meant" line, never hidden.
3. Sinking into a seat, hovering and passing through a body can never be excused.
4. Only if step 1 finds flags still unclear, and on a separate yes: a helper looks at the picture and reads the screenplay line and says "meant" or "fault".
5. The three resting-hand faults (May's hand into her lap, Blair's wrists into the armrest) are fixed in the drawing either way.
Why: The drawing already knows what it means; the checks just can't read it, so we keep copying it by hand and it keeps breaking.
You'd notice: Shorter check lists that are nearly all real faults, and meant staging no longer coming back after a redraw.
Other option: Teach the hand check how far apart people really stand, so side-by-side runners stop counting as touching.
Lost: The hand-typed "this is fine" lists for crowd movements.
Added: A meaning note on each shared movement, a test that proves it, and possibly a picture helper. About 4% of a week once (estimate), then very little per film.
### Option 2: measure distance first
Problem: The same: the checks flag meant overlaps and the answers break when the drawing changes.
1. First, the same full-size sort of every flag this film has had. Nothing changes yet.
2. On your yes: the hand check uses how far apart people really stand, so a hand only counts as touching when it would really meet the other body.
3. On a separate yes, only if meant flags remain: each movement carries a plain "what is meant" line the checks read.
4. On a separate yes, only for what is still unclear: a helper looks at the picture and the screenplay line and gives advice.
Why: Fix the measuring first, so fewer flags need judging at all.
You'd notice: Fewer crowd "hand over another body" flags; doorway and pop-in flags stay until step 3.
Other option: Option 1, putting the meaning with the drawing first.
Lost: The hand-typed "this is fine" lists for hands, once step 3 covers them.
Added: A distance-based touch test, a meaning line on movements, a judge pass on each animatic. About 3.3% of a week once (estimate).
