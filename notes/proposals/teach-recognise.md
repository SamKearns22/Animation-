# Proposal: How to teach Claude to recognise a broken drawing (GTA v7 note 10)

Status: open

## Problem
Sam, 21 Nov, on a frame of GTA shot 4 version 7 (picture notes/shot4-case-study/sam-v7/ultimately-door-arm.jpg):
"Ultimately there's so much wrong in this image, I don't know how to teach you to recognise it." Every check passed
that frame and the fresh-eye critique did not flag it. Sam sees in one glance faults our checks and our critique keep
missing: shot 4 has had seven versions, and three of version 7's ten notes repeat notes from version 4 (Lucia's
crossed grip, the sausage arm, the cop who does not react to being shot). Sam does not want to keep pointing at
faults one by one; he wants a way for us to see a broken drawing the way a viewer does before he sees it.

## Facts
- Chat 22's reading of the picture (film notes, v7 note 10): the arm grows out of his back with no shoulder; the
  forearm folds back into an L of flesh with a thumb-stub, no elbow, thicker than his head; the hand neither grips
  nor rests, it floats over the door; the car's side breaks into loose red slabs, the tyre sits on the door with no
  wheel arch; black bars (pillar, rail) cut across his vest with nothing to say what they are; white stair-step
  streaks at the right; the vest is a flat white shape with no back, neck or form.
- Checks that passed it: the body check (source/humancheck.py) tests joints, drawing order, pieces apart, a gun's aim,
  a neck showing; the car check (leanout.car_faults) tests bone lines against the car's solid shape; the depth-order
  and solid checks (viewchecks). None tests how the drawn shapes read (thickness against length, a shoulder joining,
  a hand touching what it rests on, what a black bar is).
- The fresh-eye critique (rule 89, source/critique.py) saw this frame only inside a wide panel at phone size.
- Chat 23 measured why two repeats came back: Lucia's crossed grip: hands set by the car's left and right, but the
  kit's 'L' arm is the arm on the picture's left when a person faces us (their right): the first fix moved the grip
  points, never which arm went to them (a new body-check test, "crossed", now catches it). The sausage arm: the 3D
  skeleton rebuild fixed where the joints are; the flat arm is still drawn at the body-middle size, so an arm 20-30%
  nearer the lens lands 1.2-1.4x its length at the same thickness (measured 1.26-1.37x in v7's firing frames).
- Chat 22's draft lesson 22 (case study section 15): a view where the flat drawing breaks (close, from behind, arm
  toward the lens) is a camera fault before it is a drawing fault.
- Sam's pictures: notes/shot4-case-study/ (sam-frame-*.jpg from version 4, sam-v7/*.jpg from version 7), each with
  his words in the case study; about 25 labelled pictures of real faults so far.
- The film is at 42.8% of its 15% budget with a forecast of 93% (handover cost line): shot 4 alone has taken about
  12 chats.

## Record
notes/shot4-case-study/shot4-case-study.md
notes/shot4-case-study/sam-v7/
notes/grand-theft-autism.md
source/humancheck.py
source/critique.py
source/leanout.py
guides/film-quality-rules.md
notes/proposals/big-body-moves.md

## Verdict (the judge, word for word)
<!-- verdict-hash: c7d480a0b749841c -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V2 (helper B). Critiqued: 7 found, 4 fixed, 3 named.

## Leak
yes: the problem file says the critique "saw this frame only inside a wide panel at phone size" (points at full-size crops) and quotes draft lesson 22 (points at a camera fix). The film notes' v7 note 10, on the record list, goes further and spells out chat 22's planned answer (Sam's pictures as examples, crops of every joint and contact, ban views where the flat drawing breaks): V3 is that plan almost word for word.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 5 | 4 | 4 | 4 | 4 | 21 |
| V3 | 3 | 3 | 2 | 2 | 3 | 13 |
## Sam test
Q1: Yes. An expert would first ask whether the existing picture critic was ever shown the fault at a size it could read. The record shows it was not, and that it asked for the crop three times. Enforcing that look and measuring it comes before teaching a new eye.
Q2: The evidence is wide enough: all ~25 of Sam's pictured faults from two versions, plus clean frames to count false alarms, run against both critic models. That beats one frame or this film alone. Two older bench cases (Blessed, Remakes) back the crop result.
Q3: The root cause is shown from the record. Close-ups were off in all six of the film's critique specs (34 panels). The critic's requests for a crop were never answered. Its FAULTs on the very panel Sam flagged were named as "taste" and the clip was sent, because the send gate only asks that some critique exists. The fix is in code (the pack, the send gate), not left for a chat to remember. Success is counted on the bench and in Sam's body notes for each clip.
Q4: Five different approaches were weighed (examples, enforcing the full-size look, a camera test, shape measures, learning first). The pick puts first the one the record shows broke, and builds the others only where the bench shows a gap.
Q5: Learning changes nothing Sam sees. Change 1 restores Sam's own 14 Nov rule and adds a code lock. It is several pieces of one mechanism under one Y (named, F4). Each later change is its own Y. All can be switched back. One real risk: crops made the Opus critic worse on Blessed (5 to 2 of 12). The bench decides which model judges the crops before the change goes in.
Q6: Facts were checked against specs, code, ledger and bench (see Faults). Costs and "12 chats" are marked unchecked.
Q7: It is sized by catching Sam's faults, not by price. The bench is kept for good. The deeper builds (shape measures, camera test) wait for the bench to show they are needed, so nothing is built cheap or blind.
Q8: Permanent: the bench stays and the locks stay. Reviewed against the film's results when Sam declares it complete. Nothing is a trial.
## Pick
V2
## Why
V2 and V1 share the right diagnosis: the eye exists, was starved and was never obeyed. V2 is stronger on evidence. Its bench is all of Sam's pictures plus clean frames, kept for good, and it already tests V3's labelled-example idea as one arm. It also sets a number Sam would feel: body notes per clip below shot 4's (8, then 4).
From V1: the "every contact moment" arm of the learn step. V1's handling of CAN'T TELL ("can't tell": the critic says it cannot judge from the picture it was given) is kept, so Sam's 11 Nov rule (a can't-tell never blocks the film) stands. V1's conditional camera-angle change is kept too; V2 had quietly dropped it.
New in the pick (missed by all three): the record shows the critic did FAULT Jason in panel 4 of round 22 ("large and cut off… seen from the side or behind"; "arm up with a ball hand and no gun shape"). The chat named those as taste ("his raised gun is hard to see at 3.75 s"). The clip then went with hunt 1's eight items open and no hunt 2, and the send gate allowed it. Enforcing the crop alone leaves that door open.
V3 has no measuring step and bundles four builds. Part of its item 3 (crossed forearms, sausage thickness, a hand on the door) was already built by chat 23. It ignores that close-ups already exist and were switched off.
## Faults in the pick
- F1 [fixed] V2 says "all eight specs". There are six; the 34-panel count is right.
- F2 [fixed] V2 said "pre-flight refuses a send until answered or named", which would change Sam's 11 Nov rule without saying so. Now: the crop is built and re-asked automatically; anything still unclear goes on the Checks line; the film is never held by a can't-tell.
- F3 [fixed] V2 missed that FAULTs on a person were named as taste and sent, and that the send gate checks only that a critique exists. Added to Change 1.
- F4 [named] Change 1 is four code pieces under one Y. They are one mechanism (the critic gets its full-size look and is obeyed), and each can be switched back alone.
- F5 [fixed] V2's change 2 dropped the camera-angle fix weighed in approach 3. It is restored as change 3, built only if the bench ties misses to the view.
- F6 [named] Crops lowered the Opus critic's score on Blessed (5 to 2). The learn step must pick the critic model for crops; Change 1's target comes from that run.
- F7 [named] Costs (about 2% learn, about 1% change 1, about 0.5% a film after) and "shot 4 about 12 chats" are unchecked estimates.
## Final version
**Learn (changes nothing Sam sees; about 2% of a week, unchecked; Opus medium plus three Sonnet helpers).** Add Sam's ~25 pictured faults from shot 4 versions 4 and 7 to the critic bench for good. Each goes in as its full frame, with a clean frame of the same shot and his words as the answer key. Run the Sonnet and Opus critics four ways: as packed this film (close-ups off); with close-ups; with close-ups plus a full-size crop of every place a hand or body touches the car; with close-ups plus three of Sam's labelled pictures. Count catches, false alarms and misses for each kind of fault. Then sort the misses: a miss even at full size; a miss on a view where the flat drawing breaks; a miss on a kind no checklist line covers (car side breaking apart, unexplained black bars, stair-step streaks).

**Change 1 (its own Y; about 1%): the critic gets its full-size look, and is obeyed.**
1. The critique pack refuses to switch close-ups off on any panel with a person in it. A panel made from a saved picture must give boxes for each person, or the pack is refused.
2. A CAN'T TELL on a person line that names a crop builds that crop and asks one fresh helper again. Anything still unclear goes on the Checks line. The film is never held by a can't-tell (Sam, 11 Nov).
3. A FAULT on a person cannot be named as taste until its full-size crop has had that fresh look.
4. The send gate accepts only a critique that had close-ups and whose person faults are each fixed or re-looked at and named.
To beat: the bench's close-up score, measured on the critic model the bench picks. On the next film: Sam's body notes per clip below shot 4's (8, then 4), and no repeated body note.

**Change 2 (its own Y; only for a kind the bench shows full size still misses):** the labelled pictures in every pack, or a shape measure in the body check (limb thickness against length, a shoulder joining, a dark bar crossing a body). Whichever the bench shows closes the gap, each with its own bench number.

**Change 3 (its own Y; only if the misses cluster on certain views):** a camera test before animating refuses views where the flat drawing breaks (a limb drawn more than 1.2 times its length, a body seen close from behind).

Each change is judged at film end against Sam's notes.
## For Sam
### Option 1: Make the checker look closely, and test it on your pictures first
The checker that looks at our pictures before you do never got a close-up of that frame. Close-ups had been switched off for this whole film. It asked three times for a closer look and was ignored, and the problems it did spot on that frame were waved off as "taste". First we test it on all ~25 of your marked-up pictures, to see what it catches when it can see properly. Then we lock it so close-ups can't be switched off, its questions get an answer, and its warnings about bodies can't be waved off. Bigger fixes (teaching it with your pictures, new shape measures, banning bad camera angles) come only where the test shows it still misses things. Each is a separate yes.
Lost: a chat's freedom to skip close-ups or wave off a body warning without a closer look.
Added: a permanent test set made from your pictures, bigger checking sheets, and fewer broken bodies reaching you.
### Option 2: Build all four teaching tools at once
Your pictures go to the checker as examples every time, with close-ups of every joint and contact in every frame. New measures look for sausage arms, floating hands and stray bars. A camera test bans views where the drawing breaks. All four are built now, without testing first which ones actually catch your faults.
Lost: about a fifth of a week of building before we know what works, and some of it repeats checks added this week.
Added: four new tools under one yes, which are harder to undo or tell apart if notes still come back.
