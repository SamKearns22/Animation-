# Model body for every character? (Sam, 25 Nov, R7 chat 7, session_01U3pKQyzgm44MCDdyHMoACP)
Sam: "Should we be building *all* our characters in the way Jason was built? Is that the answer to a large amount of
our problems?" ... "Our solution needs to take into account dynamic movement: a future film may require any action from
an actor. Standing, moving around." Scheduled by Sam for 22:20 (UK) 25 Nov: "Schedule this full investigation".
Facts already checked (chat 7): Islamocommunism: El-Sayed sat behind the desk and STOOD (shot 4); AOC walked in.
GTA shot 4 (Jason, the model body): about 39% of a week (notes/bench/learn-step.md L1); Sam's notes on the model body
itself: poses and movement good, faults were cut-off and passing through the door. R7 approved plan part (b) (whole
seated person solid, house head and hands) is unbuilt. Chat 7 wrongly guessed twice (a 4-view set; "computer look"):
every claim about a past film comes from opening it, saying where.
## The investigation (proposal route: facts first, two helpers, blind judge, top two for Sam)
Requirement 1 (first test of every option): any action, one body, no visible change of drawing at any moment.
1. Count (cheap model for reading; cap 2.5%): every Sam note on every film (notes, archive, sam-notes, ledger notes):
   which a model body would have prevented, which not (likeness, timing, script...), which it might cause. A number.
   STOP after 1 and tell Sam if under about a third of body/pose/contact notes would be prevented.
2. One moving test (cap 6%): a real shot from a past film with people moving (sit, stand, walk), redone with model
   bodies and house heads and hands, at its real angle; beside the original. Clip, not a full render.
3. Blind judges score both; the proposal route's top two to Sam with Lost/Added and the cost impact (one-off switch,
   per film after), from the ledger, no padding.
Dressing (Sam asked what must be learned, chat 7): Jason's clothes were PAINTED on the skin (bench_pose.part_at) and
the trousers a pushed-out skin; loose clothes (open jackets, lapels, skirts, coats, robes, hi-vis) need real garments.
Step 2 checks first, before building: MakeHuman's own garment library (on disk? licence?). Blender: Sam said Y to it
(22 Nov, GTA chat 31; apt install blender, not in setup.sh, so install it first); it drew Jason (L2) but its cloth
simulation was never tried, then dresses the test in a suit jacket that hangs open; checks: cloth never through body or
chair, each garment one piece. Name what could not be learned.
Sam (chat 7): "Do we need to go as far as building 3d clothing models?" Default for step 2: NO garment models or
cloth simulation first. Our style is flat, so only each garment's outline and seam lines must be right. Clothes as
SHELLS from the body (already working: Jason's painted vest cut, chat 6/7 trouser shell hanging straight below the knee,
chat 6 skirt from the body's own skirt surface): a jacket = the trunk pushed out, cut open at the front, its hem hanging
straight and resting on the lap; lapels and ties painted on. Garment library / Blender cloth only if the shell fails a
named test (say which). Robes and coats swinging while walking: a lag rule, tested in the clip.
## Statement One questions the judge must answer (Sam, chat 7: "What aren't we considering? Aligning with statement one")
a. Paying for it: the switch is one-off kit cost outside films; when does it pay back (films to break even at a per-film
   saving from step 1's count)? Every film after must still be top quality within 15%.
b. Sets: people as model bodies against flat-drawn furniture and rooms is today's seam one level up (contact, depth).
   How do chairs, desks, doors, cars meet the body (Jason's car and R7's chair were in the same depth pass)?
c. Heads and hands: hand-drawn heads turning with a freely moving body (angles between our head views; the back of the
   head: Jason's "brown blob"); circle hands vs real hands holding things.
d. Moves: who poses a body for any action? Reuse the acting lists and pose kit; free motion-capture libraries as reference.
e. Checks: the rulebook's checks are built for flat bodies; which carry over, which must be rebuilt and re-proven
   (no rule without a working check) - a hidden cost.
f. The look: posted films vs new ones on the channel; a stranger test on the clip at phone size.
g. Open Wounds (live) stays on the flat kit; the switch only between films.
h. Success measure: the next films' cost and number of Sam's notes vs the last three; a stop rule if worse.
Push notification at the end of each step, pass or stop. Total cap 8.5% of a week; at the cap, stop and tell Sam.

## Step 1 result (investigation chat 1, 25 Nov, session_01U3pKQyLPecZFf57adRJxjG; Opus high; 1.8% of a week)
Where I looked: every film notes file in notes/ and notes/archive/ (28 films; handover, plan, acting, estimate and
work-log sections left out), 1682 lines (count/items.json, each with its file:line). Six Sonnet helpers sorted them
(count/instructions.md, out1-6.txt); a seventh sorted a random 200 again blind (out_sample.txt: agreed on 164 of 200);
then every "prevented" call on a body note checked by hand (count/hand-check.md). Tally: count/tally.py.
- Sam notes: 1058. Places/props 204, moves and timing 202, text/sound 131, camera 104, faces 96, BODY 90, script 86,
  CONTACT 68, other 41, clothes 26, HANDS 10. Body/pose/contact/hands together: 168 (16% of all notes).
- Of the 168: a model body prevents 50 outright (30%); 97 more only partly (87% together), nearly all of them a body
  meeting a flat chair, car, door, desk, table or prop: those need the furniture solid too (question b). 21 not at all.
  All 10 hand notes: not helped. 34 notes (body 15, face 8, clothes 7, hands 4) could be made worse by it.
- Body notes repeat about twice as often as the rest (20% read as repeats vs 11%): they are the costly ones.
- Stop rule: 30% sits right on "about a third", so step 1 stopped and asked Sam (Q1) rather than deciding alone.
Statement One, what step 1 already says (the rest is for step 3's judge):
 a. At most 16% of Sam's notes are about bodies; outright, 5% of all notes. Payback must come from the costly repeats
    (GTA shot 4 alone was about 39% of a week, notes/bench/learn-step.md L1), not from the note count.
 b. 63 of the 68 contact notes are only partly fixed by a solid body alone: sets would have to join the same depth
    pass (Jason's car did: learn-step.md L1 row 1). This is the bigger cost and is unmeasured.
 c. Hands: no hand note is fixed by it. Heads: 8 face notes could get worse (head views on a freely turning body).
 d-h. Not answerable from the count; step 2's clip and step 3's judge.
Open rule requests: none found in this investigation's notes.

## Step 2 result (investigation chat 2, 25 Nov, session_01U3pKQzuMaJ3B7QYkkK55xe; Opus high)
Built: source/model_body.py (shared: any kit film's people as model bodies; the film's own people code runs, its
flat-person calls are caught and that skeleton poses the measured body) and source/islamocommunism_model_body.py (only what is
Islamocommunism's own: flutes and handset as solids, the desk's kneehole, the door leaf, the wall round the door).
Clip: notes/proposals/model-body-all/islamocommunism-shots3-5-side-by-side.mp4 (posted | model body, 12.17-27.84 s).
What the model body found that the flat film hid (each fixed in the drawing, never the shot):
- The flat seated pose put his hips 15 cm BELOW the chair's cushion and his desk forearm 13 cm INSIDE the desk; once
  risen, he stood INSIDE his own chair (the set's chair never moved). Fixes: the measured body's own lengths (the
  kit's legs are short: standing hips 0.74 m vs a real 1.78 m man's 0.96 m), the bottom resting on the cushion, a hand
  the film laid on a surface resting on its top, and (Added) his chair rolls back 0.4 m as he stands.
- Kit drift (not this test's fault): Islamocommunism rebuilt today draws both people BALD with no beard (the film
  hooks its heads into traitors_cast.HEADS; the kit now draws heads from body.HEADS), and `islamocommunism.py stills`
  at drawing scale 1 frames the room wrongly (burnham and body each keep their own scale). The posted film is
  untouched. move to shared: hook old films' heads into body.HEADS too (islamocommunism_model_body._heads does it for this test).
Checks on the clip (188 frames, 4.6 min to render, 12 frames a second): nothing through the desk, the door leaf,
the door wall or the chair once he stands; 6 frames (15.0-15.5 s, seated) his bottom presses into the rigid cushion
box (named); his desk hand rests at the desk's front edge, 0.2-0.28 m short of where the flat pose put it (inside the
desk). Fixed on my own before sending (3 faults, each fixed once; the third found by the body check: both heads sat on the
collar, no neck, because the head was set 14 cm over the neck instead of the kit's height): empty hanging arms bowed out like hands on hips
(now they keep the kit's direction from the shoulder); the turned door leaf was tested as a box round it (false hits).
Cost of step 2: about 1% of a week (chat at 2.1% with its start).
Not done here (named): clothes are painted on a pushed-out skin (jacket 1.6 cm off the body, trouser shell from
solid_seat); no garment hangs or swings. The chair cushion is a rigid box: a seated bottom presses up to a few cm in.

## Where things stand (investigation chat 2)
Sam (25 Nov, on the step 2 work): "The 3D looks much worse." That is step 3's question answered by Sam himself.
Rules that bite next: Statement Two (say plainly it is worse), 85 (cost: chat 2 at about 3.1%), the proposal route.
Done: step 2 built and rendered (model_body.py, the side-by-side clip); 3 faults fixed after the fresh-eye look.
Why it looks worse (Claude's own look): a painted mannequin, not a drawing: lumpy stiff limbs, a jacket that is skin
with no shape or folds, small drawn heads on big real bodies, real proportions making him look hunched at the desk,
forearms and shoes shortened when they point at the lens.
Next: stop the switch (Claude's pick), asked of Sam as Q1. Keep what was learned: the depth check showed the flat
poses sit 15 cm inside the chair and lay the forearm inside the desk; that check could guard flat films (a proposal,
not asked). If Sam says go on instead: real hanging clothes, a body drawn in the house's clean curves, poses made
for 3D; each must be learned first (weeks, not a chat).
Needs Sam: Q1 (stop, Y/N).
Read: this file only.
Open rule requests: none.
For Claude: islamocommunism_model_body.py clip 12.17 27.84 OUT; _heads() is a 'move to shared' (body.HEADS hook for old films).
Locked by Sam: Islamocommunism's cameras, times and beats as posted; no posted film is changed; Open Wounds stays flat.

## Exceptions
| warning | - | why | looked at | chosen or real | owner |
|---|---|---|---|---|---|
| `BODY: side.mp4 12.79 s: Alexandria Ocasio-Cortez: L forearm drawn 0.3x its length (end-on to the lens: reads as a stub) (17 drawings)` | - | model bodies draw a forearm aimed at the lens shortened, as it really is; the film's flat poses (two glasses held out in front, the handover) aim it there freely. A finding for step 3: model-body poses must keep forearms off the lens line | the clip at full size, those frames | real | step 3 / the model-body plan |
| `BODY: side.mp4 15.04 s: Abdul El-Sayed: no neck shows (1.9 cm; at least 2): the head sits on the shoulders (Ad-Vanced 57: lift the head off them) (6 drawings)` | - | the head lifted to the kit's height this chat (was the fault in every frame); in these 6 frames (a nod, the lean) 2 mm short of the 2 cm bar. Not fixed again to save a render | the clip at full size, those frames | real | the model-body plan |
| `BODY: side.mp4 15.04 s: elsayed: body points inside the desk chair (133 points) (6 drawings)` | - | the cushion is a rigid box in the test; his seated bottom presses up to a few cm in, as into a soft seat; hidden behind him from this camera | the clip at full size, 15.0-15.5 s | real | the model-body plan (soft seats) |
| `BODY: side.mp4 22.13 s: Alexandria Ocasio-Cortez: L forearm drawn 0.2x its length (end-on to the lens: reads as a stub) (1 drawing)` | - | model bodies draw a forearm aimed at the lens shortened, as it really is; the film's flat poses (two glasses held out in front, the handover) aim it there freely. A finding for step 3: model-body poses must keep forearms off the lens line | the clip at full size, those frames | real | step 3 / the model-body plan |
| `BODY: side.mp4 25.38 s: Alexandria Ocasio-Cortez: no neck shows (1.8 cm; at least 2): the head sits on the shoulders (Ad-Vanced 57: lift the head off them) (6 drawings)` | - | the head lifted to the kit's height this chat (was the fault in every frame); in these 6 frames (a nod, the lean) 2 mm short of the 2 cm bar. Not fixed again to save a render | the clip at full size, those frames | real | the model-body plan |
| `BODY: side.mp4 27.46 s: Alexandria Ocasio-Cortez: R forearm drawn 0.3x its length (end-on to the lens: reads as a stub) (5 drawings)` | - | model bodies draw a forearm aimed at the lens shortened, as it really is; the film's flat poses (two glasses held out in front, the handover) aim it there freely. A finding for step 3: model-body poses must keep forearms off the lens line | the clip at full size, those frames | real | step 3 / the model-body plan |
| `BODY: side.mp4 27.71 s: Abdul El-Sayed: R forearm drawn 0.3x its length (end-on to the lens: reads as a stub) (1 drawing)` | - | model bodies draw a forearm aimed at the lens shortened, as it really is; the film's flat poses (two glasses held out in front, the handover) aim it there freely. A finding for step 3: model-body poses must keep forearms off the lens line | the clip at full size, those frames | real | step 3 / the model-body plan |
| `BODY: side.mp4 27.80 s: Abdul El-Sayed: R forearm drawn 0.2x its length (end-on to the lens: reads as a stub) (1 drawing)` | - | model bodies draw a forearm aimed at the lens shortened, as it really is; the film's flat poses (two glasses held out in front, the handover) aim it there freely. A finding for step 3: model-body poses must keep forearms off the lens line | the clip at full size, those frames | real | step 3 / the model-body plan |
