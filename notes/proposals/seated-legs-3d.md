# Proposal: Seated legs that read in every view, after four failed chats of hand-drawn leg outlines

Status: open

## Problem
Seated people in the kit do not have believable legs. On Sam's sheet v4 (25 Nov: May, Kemi and Blair seated, seen
from the front, three-quarter, side and with legs crossed) Sam wrote: "Though they finally managed to give characters a
bum, the legs look awful." From the front the lap is a flat grey blob with a scalloped hem over two straight posts; from
three-quarter the near thigh nearly vanishes and the legs look like a standing person's behind a chair; from the side
the thigh-to-knee step is lumpy; crossed, the top shin leaves the knee at a strange angle, the foot floats and the top
leg does not read as resting on the under leg. The bum and seat were accepted and must keep reading.
Sam also wrote: "Building body kits is costing huge unacceptable expenditure and producing awful results. This cannot
continue." and "The approach to building these kits is wrong if it takes 27% of a week to fail to build normal seated
legs on a simple model." He passed on an outside suggestion: build a stick skeleton with explicit joints first, then
wrap volume and clothing around the bones, because raw hand-written outlines cannot manage foreshortening (front view)
or overlap (crossed legs).
The job: seated legs, waist to feet, that a stranger believes without effort in all four views for every kit person
(women and men, trousers, skirts, different builds), at a cost Sam accepts, without another round of the same failure.

## Facts
- Sam's words and his three marked pictures of sheet v4: notes/learn/seated/handover-sam-25nov.md;
  notes/learn/seated/examples/sam-25nov-v4-legs-awful-1..3.jpg. The first R7 note (24 Nov, "No bum/circular knees"; "you
  do not *know* how to draw this part of the body as you couldn't do it on blessed either"):
  notes/learn/seated/no-bum-circular-knees-sam.jpg; notes/next-jobs.md R7.
- Cost so far: Sam's figure 27% of a week over R7 chats 1-4 (24-25 Nov). The film budget is 15% of a week per film
  (CLAUDE.md Statement One). The r7 ledger (notes/ledger/r7.md) shows no chats imported (unchecked against the app).
- How the legs are made today: the skeleton is already solved in 3D (source/sitting.py realize(): hip, knee, ankle per
  side for each seated pose spec). Thighs and calves are then drawn as hand-written 2D outlines in source/views.py
  (the leg drawing and the R7_ constants: thigh arch, calf, knee step, lap shading, far-leg shade), patched view by view
  across chats 1-4 (notes/next-jobs.md R7 "where things stand"; notes/archive/r7-handovers.md). Each patch fixed one
  view and broke or missed another (handover-sam-25nov.md "What I found"). Rule 30: a note given twice means the
  method, not the picture, is wrong.
- Blind judges (notes/learn/seated/judge_r7.py, results-r7*.md) scored chat 4's legs 2-3 out of 5.
- The project has a measured human body: MakeHuman (CC0) mesh, full skeleton and skin weights (source/mhuman.py); a
  build is set by six numbers (gender, age, muscle, weight, height, proportions).
- GTA (22-23 Nov): after 14 failed attempts at shot 4 with flat pieces, proposal solid-body-moves (notes/proposals/
  solid-body-moves.md, adopted) built a test bench: the MakeHuman body posed on a house skeleton by its skin weights as
  ONE closed body (source/bench_pose.py), drawn in one pass where depth decides what hides what, house flat colours by
  clothing part, house ink on silhouettes and part borders (source/bench_draw.py), with the house head, neck column and
  circle hands (source/bench_move.py dressed_draw); used in the film by source/jason3d_film.py. Jason sits in a car seat
  in shorts. Sam on the redrawn dressed clip (23 Nov): "It looks very good. Well done." and "We have added a new skill
  to our toolkit." (notes/archive/grand-theft-autism-notes.md, "Sam (23 Nov, on the redrawn dressed clip)").
- Sam's notes on that 3D Jason along the way: lost bulk ("he's a muscled guy", fixed by BULK); the neck join jagged; the
  vest strap an island; nobody had judged the dressed body beside the approved flat Jason
  (notes/archive/grand-theft-autism-notes.md chat 46; notes/bench/learn-step.md; notes/bench/sam-notes/).
- Separately, the earlier per-part 3D arm (source/arm3d_film.py, a MakeHuman arm joined to the flat body by fades)
  drew Sam's "gross distended sausage" note four times (notes/archive/grand-theft-autism-notes.md lines 216, 462, 598,
  628). Unchecked whether that was the arm itself or its join to the flat body.
- The bench is Jason's build and Jason's clothes (vest, shorts) only; part_at labels clothing on his rest body. Trousers,
  skirts, women's builds and the kit's own camera and pixel units (sitting.py: FLOOR 928 px) were never tried with it.
- Speed: a dressed still went 105 s -> 17 s after the bench speed-up (commit 25c58ee9).
- Bench chats cost about 2-2.6% of a week each (notes/ledger/grand-theft-autism.md lines 62-63, estimates).
- The sheet Sam saw: notes/learn/seated/sheet_r7.py (front, three-quarter, side, crossed; May, Kemi, Blair; from
  source/castsheet.py setup for brexit-is-done).

## Record
notes/learn/seated/
notes/next-jobs.md
notes/archive/r7-handovers.md
notes/proposals/solid-body-moves.md
notes/archive/grand-theft-autism-notes.md
notes/bench/learn-step.md
notes/bench/sam-notes/
notes/ledger/grand-theft-autism.md
notes/ledger/sam/
source/sitting.py
source/views.py
source/castsheet.py
source/mhuman.py
source/bench_pose.py
source/bench_draw.py
source/bench_move.py
source/jason3d_film.py
source/arm3d_film.py
guides/kit-catalogue.md
guides/figure-rig.md
guides/film-quality-rules.md
CLAUDE.md
