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

## Verdict (the judge, word for word)
<!-- verdict-hash: 7e0ec44ef242c2cd -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = chat, V3 = helper B. Picked: V2 (chat). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the name ("-3d"), the outside "skeleton first, then wrap volume" suggestion and Facts weighted to the GTA bench all point at measured 3D legs; and the problem's wording "hand-written 2D outlines" is wrong (views.py _limb3 already samples 3D tube rings and projects them; R7_END_ON, R7_FAR pick the hiding), which steers helpers to the wrong root cause.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 4 | 4 | 4 | 5 | 20 |
| V2 | 4 | 4 | 4 | 4 | 5 | 21 |
| V3 | 3 | 3 | 2 | 2 | 4 | 14 |
## Sam test
Q1: Yes with the fixes below: measure before building, on the one body method Sam has praised, and the stop that failed (27% spent against a 6% estimate, ledger r7 shows 0 chats) becomes a check, not a habit. An expert would also make the learn chat log its own cost; added.
Q2: The scope is the right unit (how the kit draws every seated person, every film), the evidence is wide: all three judge rounds (results-r7, r7c3, r7c4), Sam's v4 marks, the GTA record (checked: Jason's legs "never seen", GTA notes 291-293), both ledgers. Covers women, men, trousers and a skirt.
Q3: Root cause named and checked (guessed tube shapes plus faked hiding; no enforced stop; the solid body not in the catalogue). Known to work by numbers set before drawing (every view 4+, nothing below chat 4, right woman/man 3 of 3, bum still reads) and then Sam's Y on the sheet. Enforced by the switch kittest, the seated checks and the handover check, not by a chat choosing to read something.
Q4: Five approaches, two of them reframes (whole solid person; a process stop); two methods measured side by side rather than argued.
Q5: Learning changes nothing; each change its own yes; posted and locked films stay pixel-identical behind people.BEFORE_SEATED. Sam is not asked to trust unseen legs: he sees the sheet first. Weak spot named: judges are not Sam (F4).
Q6: Checked: Sam's words and 27% (ledger/sam), judge scores, leg_cover switch (views.r7_on), BEFORE_SEATED, seated_r7_switch, seated_look, no_bottom, rule 87 "by hand", catalogue gap, bench costs as estimates. Unchecked and marked: the 27% against the app, the arm "sausage" cause, the skirt surface, the body at kit scale.
Q7: Sized by the result (judges' 4 in every view, then Sam's Y), not a price; the cheap trap (chat 5's six outline patches) refused. Honest cost 10-12% of a week, once for every later film.
Q8: The sheet is a finding, not a trial; changes are made fully or not at all and reviewed at the end of the first film that uses them.
## Pick
V2
## Why
V2 rests on the widest, best-checked evidence: it alone found that Sam has never seen the solid body's legs (true: in GTA they stay hidden in the car), so "It looks very good" is not evidence for legs; that the solid body is missing from the catalogue (true); and that the stop rules are kept by hand (true, rule 87). It measures the per-part join (the route the arm "sausage" came from, cause unchecked) against a whole solid person instead of assuming, includes a skirt (the job demands skirts; V1 defers them, falling short), and makes the stop rule a check tested on R7's own chats.
Taken from V1: the correct root cause (R7 already projects 3D tubes; the faults are guessed shapes and flat hiding rules), the switch and kittests that keep posted films identical, a tighter learn cap. Taken from V3: the per-person build and clothing from each spec, the chair in the same depth pass, and crossings counted.
V3 loses on risk and cost: one yes for the whole build before any measurement, a 6% cap that is the same estimate R7 overran fourfold, and a stated cause for the arm "sausage" that is unchecked.
## Faults in the pick
- F1 [fixed] V2's root cause said each view's outline guesses again; corrected to V1's checked reading (guessed tube radii and bumps, hiding by cut-off numbers and shading).
- F2 [fixed] V2's change 1 "kit test redraws the sheet against the threshold" cannot run blind judges; replaced by the switch kittest, the seated checks passing on the new sheet and still catching Sam's v4 frames; the judges gate the learning step only.
- F3 [fixed] The learn chat's 4% cap was kept by hand, the exact R7 failure; it now logs itself in the r7 ledger at each handover and the handover check stops at 4%.
- F4 [named] Blind judges are not Sam: a 4 is necessary, not sufficient; Sam's Y on the sheet, beside reference photos, is the gate.
- F5 [named] If the whole solid person wins, its torso would differ from the standing flat one at a sit or stand; that goes to Sam as its own question with its Lost line, never built by default.
- F6 [named] Unchecked: the skirt surface in the body's data (if absent, said plainly, not faked), the 27%, the bench costs, the arm "sausage" cause, the body at the kit's scale.
## Final version
**Root cause.** R7 already places hip, knee and ankle correctly and projects 3D tubes, but the tubes are guessed (set radii, hand bumps) and hiding is faked by cut-off numbers and shading, so each patch moves another view. Nothing stopped the job: estimate 6%, Sam's figure 27%, ledger empty.

**Learn (changes nothing; one Opus-high chat, cap 4%, logged in the r7 ledger each handover).**
1. Generalise the bench drawing out of Jason/car code: any kit person's build from their spec, posed on sitting.realize's joints, kit camera and units, house colours and ink, the chair in the same depth pass.
2. Draw sheet v4's four views (May, Kemi, Blair) two ways: (a) solid legs under the flat torso, joined at the hem; (b) the whole seated person solid with house head and hands. Trousers as a shell about 14-15 cm across at the knee; one skirt from the body's skirt surface if it exists.
3. Measure: fresh blind judges (judge_r7.py), no_bottom, seated_look, body-chair and leg-leg crossings 0, each clothing part one piece.
4. Pass: every view 4+ from all three judges, nothing below chat 4, the right woman/man 3 of 3, the bum reads. Else stop and tell Sam what must be learned.
5. Sam sees the winner beside v4 and reference photos: one numbered question.

**Change 1 (own yes, after pass and Sam's Y).** The winner replaces seated_lower for new films behind BEFORE_SEATED; kittest seated_r7_switch keeps posted films pixel-identical; seated_look still catches Sam's v4 frames; a catalogue line. About 6-8%.

**Change 2 (own yes).** The handover check stops a kit job after two judged rounds rising less than a point, and kit jobs' costs go in the ledger; must flag R7 chat 3 from results-r7/r7c3. About 1%.

Cost: 10-12% of a week. Lost: R7's drawn legs for new films; chat 5's planned patches.
## For Sam
### Option 1: Test real measured legs first, then build, with an automatic stop
Problem: Seated legs were drawn from guessed shapes, so fixing one view broke another, and nothing stopped the work when it kept failing, so it cost 27% of a week.
1. One chat (at most 4% of a week, its cost recorded as it goes) draws May, Kemi and Blair seated, from all four angles, using the measured human body that drew Jason in the car film: once as real legs under our flat top half, once as the whole person.
2. Trousers and one skirt are tried; fresh helpers who don't know which is which score every angle.
3. If every angle scores 4 out of 5 or better, beats today's legs, and reads as the right woman or man, you see that one sheet beside your marked sheet and real photos, and answer one numbered question.
4. Only on your yes do these legs become every new film's seated legs; finished films stay exactly as they are.
5. Separately, on its own yes: any kit job that improves less than a point over two tries stops itself and comes to you.
Why: you have never seen those measured legs (in the car film they stayed hidden), so they are tested before you are asked to trust them.
You'd notice: one sheet, then seated people whose legs hold from every angle.
Other option: Option 2, cheaper, trousers only, no automatic stop yet.
Lost: the drawn legs for new films; the six small patches planned next.
Added: about 10-12% of a week once, for all later films; a stop on runaway kit jobs.
### Option 2: Quick test of measured legs in trousers only
Problem: Seated legs were drawn from guessed shapes, so fixing one view broke another, at 27% of a week.
1. One chat (about 2.5% of a week) draws May, Kemi and Blair seated, from all four angles, with the measured body's legs under our flat top half, in trousers.
2. Fresh helpers score it; at 4 out of 5 everywhere, you see the sheet.
3. On your yes, these legs become new films' seated legs; finished films stay as they are.
4. Skirts and an automatic stop for failing jobs each wait for a later proposal.
Why: the smallest test of the method that worked on Jason.
You'd notice: a sheet sooner; skirted people still on the old legs.
Other option: Option 1.
Lost: the drawn legs for new films; skirts stay on the old drawing for now.
Added: about 7% of a week; nothing stops the next runaway job yet.
