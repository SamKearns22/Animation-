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
