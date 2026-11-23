# Proposal: Jason's get-up and sit-down in shot 4 move faster than the approved 3 cm bar allows

Status: open

## Problem
Shot 4's locked acting rows give Jason 0.5 s (12 drawings, K1 0.5 s -> K2 1.0 s) to get from sitting to kneeling on
the seat, and about 0.35 s (C3 7.45 s -> K1 7.8 s) to sit back down. Climbing onto a seat on your knees inside a car
takes a real person longer. To fit, his joints move 15-54 cm a drawing and change speed by up to 49 cm in one
drawing. The bar Sam approved for stage 1 (proposal solid-body-moves) says no joint jumps over 3 cm a frame, so the
grey test body can never pass it at the locked timing: the check prints 283 "pops" and 341 "steps over 3 cm" on
every run, all named, which teaches nobody anything and could hide a real pop. Sam's earlier notes on this shot were
about bodies that looked impossible (limbs through each other, arms from the back, horror on the way back). The
locked camera, beats and times must not move (CLAUDE.md "Fix the drawing, never the shot"). What is missing: a way
to tell, and a bar that says, whether a move this fast reads as believable to a viewer from THIS camera, and a way
to draw it so it does.

## Facts
- Locked (notes/grand-theft-autism.md, Where things stand chat 41): shot 4's camera and acting-row times K1 0.5,
  K2 1.0, K3 1.4 ... K2 7.4, K1 7.8; house art style; circle hands.
- The bar: notes/proposals/solid-body-moves.md line 105 ("no joint jumps over 3 cm a frame"), Sam's "Y 1".
  The check: source/bench_move.py jumps() (steps over 3 cm a frame; pops = a step more than 3 cm off the smooth
  path through its neighbours, i.e. speed change over 3 cm a frame).
- Already flagged as the open question: notes/bench/learn-step.md line 95 (chat 34): "the 3 cm a frame bar cannot
  hold at the locked timing ... count sudden jumps instead?"; chat 41 section: "real quick limbs change speed 9-17
  cm a frame at 24 fps" (source of that figure: unchecked).
- Measured chat 42 (current move, solve per frame), get-up 0.33-1.33 s, largest step / largest speed change a
  drawing: head 23.8 / 23.8 cm (at 0.54 s: from rest to 24 cm in one drawing), left shoulder 25.9 / 25.9, gun
  wrist 27.9 / 33.8 (0.88 s, K1 hold -> K2 hold), left elbow 38.9 / 43.1, pelvis 10.4 / 12.0, knees 34.7-42.7 /
  28-39, ankles 28-37 / 27-39. Sit-down 7.0-8.08 s: head 15.3 / 15.3, gun wrist 27.2 / 35.9, pelvis 14.1 / 17.1,
  right ankle 54.1 / 48.8.
- What the film camera sees (source/gta_rehearse.py CAM4): 0-0.45 s shot 3's exact windscreen frame; 0.45-1.10 s it
  swings round the front corner to his window; legs below the door top are never in the film camera (critique spec
  v8: "His legs are never seen (he kneels on the seat)"). Over 7.0-8.2 it swings back to the windscreen frame. Which
  joints are on screen at each drawing: unchecked.
- Everything else in the grey clip is clean (chat 42): 0 body-car, 0 pistol, 0 joint range over 198 drawings; one-
  point joint creases and 1-2.5 cm slides named. Clip: animations/drafts/grey-lean-out-whole.mp4 (sent to Sam 23
  Nov). Watched at phone size by Claude: reads as one move (not a viewer's test).
- Fresh critique r42-grey-p1 (source/data/critique/grand-theft-autism/r42-grey-p1/result.md): no fault about speed;
  it said the frames were too far apart to judge rhythm (CAN'T TELL).
- Next after the grey body: stage 2, the dressed look in the house style, then back into the film (proposal
  solid-body-moves). The 3 cm bar is also on the pass list as item 23 (learn-step.md L1).

## Record
notes/bench/learn-step.md
notes/proposals/solid-body-moves.md
notes/grand-theft-autism.md
source/bench_move.py
source/gta_rehearse.py
source/leanout.py
guides/film-quality-rules.md
animations/drafts/grey-lean-out-whole.mp4
notes/bench/l3-reference.jpg
