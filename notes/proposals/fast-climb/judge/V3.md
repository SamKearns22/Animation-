# Helper B: fast-climb

## Leak
Mild: "what is missing" leans to a camera-based "believable" bar, and the facts carry chat 34's "count sudden jumps instead?". Set aside.

## Results
- Sam's shot 4 notes: all impossible bodies, none speed (grep: case study, archive notes, ledger/sam). His view of the grey clip (sent 23 Nov): not in the record.
- jumps() (source/bench_move.py L1455) counts STEPS (over 3 cm a drawing: speed) and POPS (second difference over 3 cm: speed change) for 15 joints, legs included, ignoring the camera. 283 / 341 a run: problem file (chat 39: 142 / 411, notes/bench/proof.txt).
- Locked windows: get-up K1 0.5 -> K2 1.0 (12 drawings); sit-down K2 7.4 -> K1 7.8 (about 10) (notes/grand-theft-autism.md, chat 41).
- The drawing uses part of them: climb keys C1 0.56 ... C3 0.89, sit-down C3 7.45 ... C1 7.70 (learn-step.md, chat 41); the gun hand holds K1 until about 0.83, then crosses in 3-4 drawings at 22-28 cm each (learn-step L303); the head goes from rest to 24 cm in one drawing (problem file).
- Physics floor (my arithmetic): D rest to rest in N drawings needs speed at least D/N, speed change at least 4D/N² (smooth ease 4.9D/N²). Gun hand, 0.8 m (learn-step L96) in 12: speed at least 6.7 cm, so the step bar can never pass; speed change only 2.2-2.7 cm, so the pop bar CAN. Measured 33.8: about 13 times the floor.
- Camera still to 0.45 s, swings round 0.45-1.10; legs never on screen (gta_rehearse CAM4 L638-646). Joints on screen per drawing: unchecked.
- Nobody judges rhythm: critique r42 CAN'T TELL.

## The real decision
For every fast locked move: how does a check tell speed the beats force (no fault) from jerks the drawing adds (a fault)? The bigger lever is the spacing inside the locked windows.

## Root cause
One number was set for two things. Speed is fixed by Sam's times, so the step bar is unreachable noise that trains chats to name, not look. The pop bar is mostly right: pops run 10-15 times what the times need, because the climb is crammed into 0.33 s of a 0.5 s window; joints wait, then whip, with no ease or overlap. Chat 39's "breakdowns passed with speed" (learn-step L153, L230) smoothed paths but kept the crammed timing.

## Approaches weighed
1. Reframe: judge each joint against the least its locked window allows, and fix the spacing to reach it.
2. Viewer-first: a screen-space test on the film camera; a step wider than the limb's own on-screen width reads as two drawings (strobing).
3. Learn-first from reference: measure a real fast sit-to-kneel (no footage shows knees on a seat, learn-step L71).
4. Sam's eye alone: a check must catch it first (Seeing like Sam 2).

Chosen: 1; 2 only if the learning shows strobing; 3 lacks footage.

## Proposal
Learn first (changes nothing; about 0.5% of a week, Opus high, next stage-1 chat): per joint and window, print travel, floor speed, floor speed change, measured, on screen yes/no (through CAM4), and on-screen step against limb width.

Then one change at a time:
- C1, the pop bar: a pop is a speed change over 3 cm or over the smooth-ease value its window allows, whichever is larger. Proven first on old faults (81 cm knee flip, chat 41; 33 cm elbow snap, L149; 22.3 cm elbow pop, L212): all still caught. Beat: 283 pops -> 0, except joints whose floor exceeds 3 cm, each printed with it. Enforced in jumps(), which the send guard reads. About 0.3%.
- C2, the drawing, judged by C1: re-space get-up and sit-down over the whole windows, eased, overlapping (gun hand starts with the hips at 0.5). Camera, beats, times untouched. About 2.5%.
- C3, only if on-screen steps exceed limb width: the step bar becomes that strobing test; otherwise it goes. About 0.5%.

Total about 3.8%; the film is already at 89.23% against a 53.2% estimate (ledger). Sam would notice a grey climb starting smoothly at 0.5 s, no snaps, his timing kept.

## Sam test
Q1: splits speed from jerk, spacing first.
Q2: every fast locked move, not one shot.
Q3: bars computed, nothing to excuse; proof: pops at floor, no speed note.
Q4: four kinds weighed.
Q5: never above physics; old faults caught; each undoes alone.
Q6: sourced or marked.
Q7: sized by the floor reached.
Q8: permanent, reviewed at film end.

## Lost / Added
Lost: the flat 3 cm speed bar (C3, on Sam's Y). Added: a floor-referenced pop bar, a strobing test if needed, a re-spaced climb.

## Unchecked
Joint travel except the gun hand; joints on screen; the 283/341 counts; "9-17 cm a frame"; pose tracking; Sam's view of the grey clip.
