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
