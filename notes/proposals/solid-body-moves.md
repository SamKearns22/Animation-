# Proposal: Learn to move a character in 3D for complex showstopper moves (Jason, shot 4 test space) without changing the art style

Status: open

## Problem
The project cannot make a cartoon person do a complex whole-body move (Jason climbing out of a moving car's window,
firing back, climbing back in) from a fixed camera without parts passing through each other or through the car, without
arms reading as tubes and hands as blobs, and without the drawing's look drifting. 14 attempts over 25 chats failed and
Sam stopped them (22 Nov). Sam's diagnosis: we tried to do too much at once without first learning the skill. Sam asks
for a separate test space (only Jason in his sitting pose and the car window), a skeleton that moves in 3D, the move done
with no clipping, the camera unchanged, the hand style unchanged, the house art style unchanged and blending into the
scene; the skill must serve all future complex human moves in showstopper shots. Sam is not an animator and asks for
research and a plan before anything is built. Separately, Jason's hand style changed (circle hands to fingered hands) in
chat 28 without Sam asking, which disturbed him.

## Facts
- Sam 22 Nov (notes/ledger/sam/3l2mwjz7.md): the request above, verbatim.
- 14 attempts, all FAILED: notes/shot4-case-study/shot4-case-study.md section 17 (table).
- Locked by Sam: shot 4's camera and beats, the script, shot order and lengths (CLAUDE.md "Fix the drawing, never the
  shot"; notes/grand-theft-autism.md Where things stand).
- House look: flat colour pieces with house outlines; people drawn by views.person with "circle hands" by default
  (guides/kit-catalogue.md "People" heading).
- Current shot 4 build (source/leanout.py MAP): key poses on a 3D skeleton (lying.Body), but drawn as separate flat 2D
  pieces (lying_flat.draw), then patched per part: hand3d_film (MakeHuman hand mesh), arm3d_film, head3d_film,
  gun3d_film, a hand-made "door-hiding map" (leanout._cover) to decide what the car hides. Faults found in the last four
  chats were mostly where pieces meet or overlap: seal showing through the arm, smears, stair-steps, elbow outside the
  door, window post through the mouth, a dark slab across the arm (notes/grand-theft-autism.md chat 30 section;
  chat 31 report in the case study section 17).
- The project already has MakeHuman's measured body (CC0): mesh, full skeleton with fingers, skinning weights
  (source/mhuman.py), a mesh-to-shape renderer (source/mesh_sdf.py), a body check (source/humancheck.py) and a strip
  check (leanout.py strip, 311 fault lines baseline).
- Hand style change: chat 26's own fault list wrote "F13 hands are discs or mittens (no fingers read)" and "F1 the hand
  on the door a blob" after Sam said only "so many problems with hands" (Sam 21 Nov 15:22, notes/ledger/sam). Chat 28
  built fingered hands (HAND3D in source/leanout.py, its comment credits "Sam 21 Nov ... 'the hand on the door a
  blob'", words that are chat 26's, not Sam's). No proposal or Sam question before the change (unchecked beyond
  notes/archive/grand-theft-autism-notes.md chat 28 section).
- Tools available in the container: Python 3.13; Blender 4.0.2 from the system package list; a bpy 5.3.0 wheel
  (Blender as a Python module) downloads. Neither installed or tested (installing was not allowed in this chat; untested
  whether it renders headless here: no graphics card).
- Free motion data: CMU motion capture database, 2500+ moves, free for any use (mocap.cs.cmu.edu; cgspeed BVH release).
- Industry practice for a 2D look from 3D (web, 22 Nov): Guilty Gear Xrd (GDC 2015, Motomura): 3D models cel-shaded,
  hand-edited shading, animation held on twos/threes and hand-keyed, per-shot pose tweaks to read like drawings; Blender's
  toon shading plus Line Art (outlines from the 3D model's silhouette and part borders) used for 2D-look animation.

## Record
notes/shot4-case-study/shot4-case-study.md
notes/grand-theft-autism.md
notes/archive/grand-theft-autism-notes.md
notes/archive/grand-theft-autism-handovers.md
notes/ledger/sam/
notes/proposals/big-body-moves.md
source/leanout.py
source/mhuman.py
source/mesh_sdf.py
source/humancheck.py
source/lying.py
source/lying_flat.py
source/hand3d_film.py
guides/kit-catalogue.md
guides/film-quality-rules.md
CLAUDE.md

## Verdict (the judge, word for word)
<!-- verdict-hash: e931d0f24992b5e8 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = chat, V3 = helper B. Picked: V2 (chat). Critiqued: 8 found, 5 fixed, 3 named.

## Leak
yes: the title ("move a character in 3D") and the facts (Blender, the bpy wheel, CMU motion capture, Guilty Gear and Line Art, "faults mostly where pieces meet") point at a remedy: one 3D body drawn in a toon style. Much of it is Sam's own ask (a 3D skeleton), so the anchor is partly his; the tool choice (Blender against the project's own renderer) and the order of the work are what it anchors.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 5 | 4 | 4 | 4 | 4 | 21 |
| V3 | 4 | 3 | 2 | 2 | 3 | 14 |
## Sam test
Q1: Yes, as patched: an expert blocks the move first (grey figure, planted contacts, from acted reference), then renders it in the look from one 3D scene so the depth decides what hides what; both are learned on a bench before the film. What they would add, taken in: tool picked by a side-by-side frame, not by speed.
Q2: Evidence is the whole shot 4 record (14 attempts, 25 chats, every Sam note since v4) and shot 4 is costed chat by chat in L1. The decision is the method for every future showstopper, not this shot only; the bench is built for that.
Q3: Root cause found with evidence: hiding guessed by a hand-made map (faults at every join, chats 30-31), four drawing methods joined by fades, and motion invented without reference (chat 30: the shoulder slid over the planted hand). Bars are measured by a script that prints into the handover and by a pass list made from every past note, which the bench's checks must catch on the old failed frames before they are trusted. Not left to a chat choosing to read.
Q4: Five approaches weighed (Blender, in-house single pass, motion first, a permanent bench, hand-drawn keys); the pick combines the three that each remove a cause.
Q5: Nothing enters shot 4 until Sam's Y on two clips; each stage undoes alone; shot 4 and the film stay as they are. Sam is asked to trust only things he has seen (a still, then a grey clip, then a drawn clip). Residual risk: the house look from a 3D body is untested (L2 tests it first).
Q6: Facts checked against the record (below); shot 4's cost share, Blender headless, render speed, a closed 3D car shape and suitable reference are marked unchecked and are what L1-L3 measure.
Q7: Sized by the result (zero crossings, zero strip faults, Sam's eye), not by price; about 14.5% of a week, honest, against an unmeasured but large spend on patches. No cheap trap left once the tool is chosen by the frame.
Q8: The bench, the single-pass drawing and the reference step become permanent kit; nothing is a trial. Reviewed against results when Sam declares the film complete.
## Pick
V2
## Why
V2 has the truest root cause. V1 says "the poses were never at fault" and rejects reference-led motion, but that rests on one measurement of version 4 (case study section 10); the last failures were motion faults (chat 30: the shoulder slides over the planted hand, leaving only impossible elbow bends), so V1 would draw a broken move beautifully. V1 also quotes 62.62% over 32 chats where the ledger says 61.7% over 31. V2 alone asks Sam which hand style he means instead of assuming it, and keeps the look lock as its own proposal, not bundled. V3 has the right core (one solid body, IK contacts, self-collision, acted reference) but no cost, no learn step, a six-step ladder built before any result, no Sam Y between steps, and it puts the circle hands back without asking him.
Taken from V1: the pass list built from every Sam note and the chats 28-31 faults, with the checks proven on the old frames; a no-movement still beside the approved Jason at phone size in the learn step. Taken from V3: body-against-itself and body-against-gun crossings, IK goals on the car (hand on the door top, knee on the seat), CMU motion as a reference source.
## Faults in the pick
- F1 [fixed] V2 chose Blender "only if the in-house way is too slow": the tool is now picked by the look and correctness of one frame side by side, speed second.
- F2 [fixed] Hiding in L2 was "checked by eye": now measured by the crossing script as well.
- F3 [fixed] Only body-car crossings were tested: body against itself and against the gun added.
- F4 [fixed] No pass list from past notes: added, and every bench check must catch those notes on the failed frames.
- F5 [fixed] The look was unseen until stage 2: a still in the look comes in the learn step.
- F6 [named] Shot 4's cost share is an estimate (40-50%); L1 measures it.
- F7 [named] Whether the project has a closed 3D shape of the car's door and window is unchecked; if not, it is built in stage 1.
- F8 [named] Whether a 3D body can be drawn to pass as the house look is unproven; the still in L2 is the first proof, and if it fails Sam is told before any move is made.
## Final version
**Learn first (changes nothing; about 2.5% of a week; one Opus high chat):**
- L1. Sort every Sam note and every fault since version 4 by cause (hiding and joins, look, motion). Turn them into one numbered pass list with pictures. Cost shot 4 chat by chat.
- L2. Install Blender; one frame from shot 4's locked camera of seated Jason, drawn both ways: Blender (toon fills, Line Art outlines) and the project's own single pass (MakeHuman body posed by its skin weights, car and gun in one picture keeping each dot's depth and part, house colours, house outlines on silhouettes and part borders, house face). Side by side with the approved Jason at phone and full size; crossings measured; seconds per frame. Pick the tool by the picture.
- L3. 3-5 reference clips (or a CMU motion) of a person leaning out of a car window and back; key poses and the planted contacts marked.

**Then one change at a time, each on Sam's Y:**
1. Test space: only Jason seated and the window, shot 4's camera. The L3 move as a grey figure, key poses set by IK goals on the car. Bar: 0 crossings (body-car, body-self, body-gun) at every 1/24 s; no joint jumps over 3 cm a frame; contacts held; the pass list's motion items clear. Every check first proven to catch the old failed frames. A script prints the results into the handover. About 5%.
2. The same move in the house look. Bar: 0 strip faults (from 311), pass list clear, side-by-side with the approved seated Jason, the stranger test at phone and full size. About 7%.
3. Only after Sam's Y: into shot 4, camera and beats untouched; written into the kit catalogue for every showstopper.
4. Separate proposal: a house-look lock (a hand-style change needs Sam's words quoted).

Total about 14.5%, one-off. Sam sees a still, a grey clip, a drawn clip.
Question: 1. The test space uses the circle hands, as before chat 28 (Y/N).
## For Sam
### Option 1: Move first, then the look
I learn the move on a test bench, away from the film. First one still picture of Jason drawn the new way next to the Jason you approved, so you can see the style holds. Then the move as a plain grey figure copied from real footage of someone leaning out of a car window, checked by the computer so nothing passes through anything. Then the same move in our style. You see a still, a grey clip and a drawn clip; nothing goes into shot 4 until you say yes. About 14.5% of a week.
Lost: the patched-together drawing of Jason's arm, hands and head used in shot 4 so far, and the fingered hands, once you approve.
Added: a test bench for every future big move, a way of drawing a 3D body in our style, real reference for moves.
### Option 2: Look first, then the move
The same bench, but the style comes first: Jason drawn as one solid body inside a solid car so nothing can overlap, judged against your approved Jason, then the move made in our style straight away, without footage to copy. First a lock so no chat can change the hand style again without your words. About 11.5% of a week.
Lost: the patched drawing tools for shot 4, once the new way passes.
Added: a test bench, a style lock, a list of every past note to pass.
