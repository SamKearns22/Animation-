# Helper A: fast-climb

## Leak
Set aside: "a bar that says whether a move this fast reads" and "count sudden jumps instead?".

## Results
- No timing can pass the bar. 3 cm a frame at 24 fps is 0.72 m/s, which is slower than walking (unchecked). Even at a perfectly even speed the climb needs 3.4 cm a frame: 41 cm in 12 frames (learn-step.md L303). A "pop" (jumps(), bench_move.py L1465) means the speed changes by more than 3 cm a frame, which is about 1.8 g.
- Some flags are impossible at any speed. The head goes from still to 24 cm in one drawing (about 14 g). The gun wrist changes speed by 34 cm (about 20 g) (problem file). The goal path is smooth (`_herm`). But a goal missing from one key snaps across at the halfway point (`_lerp_goal`), and each frame is solved from scratch.
- Nobody knows how many of the 624 flags are real jumps. This is the main gap.
- Films are delivered at 1.1x speed (rule 70), so the climb plays in 0.45 s. Nobody has judged it at that speed.
- The biggest numbers belong to the legs, which the film camera never shows. Which joints are on screen: unchecked.
- Sam's notes were about impossible bodies, not speed (pass list 18-20). He has not replied on the grey clip.
- Shot 4 has cost about 39% of a week. The film has spent 89.2% against an estimate of 53.2% (ledger).

## The real decision
What the move check should measure in every film. It should treat jumps (never allowed) apart from speed. Speed should be judged on screen, from the film camera at delivered speed, against how fast real people move.

## Root cause
One number per joint in world space covers two different faults: a jump, which is a break, and speed, which comes from Sam's locked timing. It is applied to joints nobody sees, and it has no real-human reference. So all 624 flags get named, and a real 14 g head pop hides among them.

## Approaches weighed
1. Raise the number. It still mixes the two faults and has no source.
2. Ask Sam whether the move reads. That makes him the check, and the timing is already his.
3. Reframe: split the check into "jumps = 0" and "speed on screen against measured people". (chosen)
4. Learn first: measure the flags, what is visible and human speeds. (step 0)
5. Fix the drawing alone: spread and overlap the climb. Kept, as the fix that comes after.

## Proposal
**Learn first. This changes nothing; about 1.5% of a week; Opus high.**
- L-a. Sort every flag in the 198 stored frames. It is a jump if the solved joint leaves its goal's smooth path by more than 1 cm, or the goal snaps. Otherwise it is speed.
- L-b. Through CAM4, record which joints are visible and their speed on screen at 1.1x.
- L-c. Measure real people's peak speed and change of speed per joint, from CMU quick get-ups, kneels and climbs (coverage unchecked) and from the L3 clips.

**Then one change at a time, each on Sam's Y:**
1. jumps() gets two tests. (a) Jumps: none allowed on any joint, and none can be named and passed. (b) Speed: visible joints only, measured against L-c at 1.1x. The new check must first catch the old elbow pop, the knee flip and the 14 g head. A guard refuses any grey clip with a jump. Target: 624 named flags → 0.
2. Fix the drawing: spread the climb over the whole of 0.5-1.0 s, with the head leading. Cameras and beats are untouched. Target: no notes from Sam on the climb.
3. Only if (b) still fails: a separate question to Sam about how the house style draws fast moves.

Cost: about 5% of a week, one-off. Honest overspend on a film at 89%; reused by later films. Sam would see a get-up that eases out of the seat.

## Sam test
- Q1: faults told apart before any number.
- Q2: every frame, film camera, delivered speed.
- Q3: root cause found; guard enforces; proven on old faults.
- Q4: five approaches.
- Q5: learning changes nothing; each change undone alone.
- Q6: sources named; unknowns marked.
- Q7: not "raise the number".
- Q8: permanent, reviewed at film end.

## Lost / Added
Lost: the 3 cm-a-frame bar Sam approved.
Added: a test that allows no jumps, an on-screen speed test, and a table of real human speeds.

## Unchecked
Walking and limb speeds, and the g figures (general knowledge). Chat 41's "9-17 cm" (no source given). What CMU covers. Which joints are visible. How many flags are real jumps.
