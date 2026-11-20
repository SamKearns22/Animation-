# Proposal: How to build big 2D body moves (a climb, a turn, a lean-out) and a check that every person in every frame is a human body

Status: adopted (2026-11-20)

## Problem
In Grand Theft Autism shot 4 (6.2 s), Jason climbs from the front passenger seat of a moving car, out through the
open side window, sits on the sill facing backwards, fires four pistol shots at a police car behind, and climbs back in
to the seated pose. Version 4 of the shot (chat 15) drew him as one stiff flat figure and Sam's frame-by-frame notes
(20 Nov) found: lower body and knees showing through the bonnet and door; the right arm "a gross sausage shape ...
dislocated from the shoulder"; "Limbs, neck, torso, all curled around each other and in the wrong place. Utterly
inhuman."; "his arms come out his back. Then the arms coming out his back pull out a pistol"; the gun firing to the
left, not at its target; "2D legs ... sticking inside the doorframe". Sam: "It really worries me that this wasn't caught
by anything we have so far implemented." And: "A 2D body can be animated to do 3D movements like this, though."
Two things are missing: (1) a way to build a big body move in the house's flat 2D style (climbs, turns past side-on,
leaning out of a window, getting in and out of cars, falls) that reads as a human body in every frame, with the right
parts hidden by the door, window frame and roof; (2) a check that would have caught every one of these faults before
Sam saw them: that each person in each frame is a human body (limbs joined, human lengths, arms on the correct side,
nothing tangled, nothing through solids), whatever the camera angle. It must work for every future film (the channel
is new satire each week; reuse the means, never the content), aim at high quality, fewer notes, and a film within about
15% of a week, and be judged on phone-size and full-size frames. Shot 4 is the first user; its build proposal goes to
Sam before any rebuilding (rule 8).

## Facts
- Shot 4's current build: source/gta_rehearse.py J4_KEYS (line ~961: 10 keys of hips, facing angle, lean, two ankles,
  in the car's frame in metres), jason4() (interpolates them), jason_layer() (line ~1015): Jason is views.standing()
  posed by putting his feet at the ankle points and solving his arms toward hand targets worked out in 3D, then drawn
  flat as one figure at one turn angle (views.py has five drawings: front, three-quarter, side, three-quarter back, back;
  a turn swaps drawings); afterwards whatever of the car lies in front of three sample points (neck, shins, feet) is
  rubbed out of him with masks (gta_cars.cover_masks), plus a hand-placed quad for the car's side on the sill.
- Chat 15 turned him to 160 degrees on the sill so the gun arm read past his shoulder; that fixed one frame and broke
  the climb on either side (case study section 7, cause A; lesson 12).
- The kit's limb solver (guides/figure-rig.md section 3): two-bone, the rig's lengths, a target out of reach is an error;
  figure.guard stops an arm >6% too long, <40%, or an elbow folded past 25 degrees; it measures arms only in 2D.
- The body check (source/viewchecks.py solid_faults, line ~427, chat 12): tests about 15 single joint points per person
  against listed solids (door, window pillar, roof, floor), feet against the pavement, and height for distance. It does
  not test that limbs join the body, that arms are on the correct side seen from behind, or tangling.
- handcheck.py (pose gallery, pre-flight): hands over/inside the body, off the arm, seams at the shoulder, a pose
  flipping sides through front-on or behind; runs on standing gallery poses, not on a film's moving shots.
- The pose gallery (guides/pose-gallery.md, source/posegallery.py): each pose drawn from five views on one sheet and
  hand-checked; no poses for climbing, sitting on a sill, or getting in or out of a car.
- source/lying.py: a 3D body from the person's own design for lying, falling, high cameras (catalogue row 70, 131).
- source/sitting.py: the sitting kit (seat and desk measured once, rising and sitting moves, its own audit).
- The fresh-eye critique (rule 89, source/critique.py) looks at pictures as a viewer would; it was not run on version 4.
- Sam (20 Nov): "A 2D body can be animated to do 3D movements like this, though." The case study's lesson 10 (draft):
  key poses drawn for each angle of the move, layered by hand, checked on a pose sheet before the shot is built.
- Rule 8 (new, Sam 20 Nov): a hardest shot gets a build proposal to Sam (key poses or method, reused, new, risks, how
  each is checked) before building. Rule 74 (new): acting notes for every shot, beat by beat.
- Shot 4's camera and beats: notes/grand-theft-autism.md "Beats for shot 4"; Sam wants the first clip's close, low
  camera beside Jason (version 1, commit 2668817c).
- Cost so far for this film: the film's ledger (notes/ledger/grand-theft-autism*); shot 4 has had four versions.

## Record
notes/shot4-case-study/shot4-case-study.md
notes/grand-theft-autism.md
source/gta_rehearse.py
source/gta_cars.py
source/views.py
source/viewchecks.py
source/handcheck.py
source/figure.py
source/posegallery.py
source/lying.py
source/sitting.py
source/critique.py
guides/figure-rig.md
guides/pose-gallery.md
guides/kit-catalogue.md
guides/film-quality-rules.md

## Verdict (the judge, word for word)
<!-- verdict-hash: dbd715b238077563 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V1 (helper A). Critiqued: 8 found, 4 fixed, 4 named.

## Leak
yes: the facts quote lesson 10's remedy ("key poses drawn for each angle of the move, layered by hand, checked on a pose sheet") and Sam's line that a 2D body can do it, and the problem lists the check's contents (limbs joined, human lengths, arms on the correct side, nothing tangled, nothing through solids). V3 follows the leak closely; V1 and V2 weigh it and move past it.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 4 | 3 | 4 | 4 | 4 | 19 |
| V3 | 3 | 3 | 3 | 2 | 3 | 14 |
## Sam test
Q1: Yes once patched: an expert measures the failed frames first, puts the check where no file can skip it (the drawing and the clip writer), and reuses the 3D skeleton the kit already draws in the house style rather than hand-built layer tables per film.
Q2: The evidence is version 4's real frames (8 of 16 notes share cause A) widened by V2's 11 past body-placement notes (critique checklist P7, 9 films). Wide enough for the check; the look of the 3D route is shown to Sam before it is built.
Q3: Root cause found with evidence: the shot was drawn in a practice file that runs no pre-flight, no pose check and no critique (checked: none called), and clips (`--span`) skip the pre-flight lock (checked, film_engine). Enforced at the drawing and the writer, not by a chat choosing to run it; numbers to beat are set.
Q4: Four different approaches weighed (hand-drawn keys per angle, a 3D skeleton route, a send gate, measure first); measure-then-gate-then-route is the strongest.
Q5: The first step changes nothing; each change is its own Y and undoes alone; the 3D look is shown on a sheet before any build. Risk named: the check sits in drawing code every film uses, so it must show 0 false flags on past films first.
Q6: Mostly checked; patched: the film's spend is now 28.82% (both helpers quoted 27.71%), and the 3D body now draws through the flat house pieces (`lying_flat`), nearer pieces over farther, not per-pixel; all costs and render speed marked unchecked.
Q7: Sized to the result (a kit for every film's big moves plus an unskippable check), about 6% of a week once, built only as the replay shows which parts matter. No cheap patch to shot 4 alone.
Q8: Nothing provisional: each change is permanent when made and reviewed at film end.
## Pick
V1
## Why
V1 and V2 share the right shape (measure first, then a 3D skeleton route and a human-body check, each its own Y). V1 wins on the root cause: it puts the check where every person is drawn and makes the clip writer refuse an unnamed fault, so a practice file or a quick clip cannot slip past it. V2's gates live in pre-flight and finishing, and the record shows shot 4 was built in a file that runs neither, and quick clips skip pre-flight's lock: the same bypass would recur. V3 builds a new part-layer drawing in the shared drawing code when `lying_flat` already lays the flat rig's pieces along a 3D skeleton, needs a hand-written layer table for every key of every film, has no learn step, and bundles drawing, check and gallery into one yes.
Taken from V2: the cold critique of version 4 in the learn step; drawing the skeleton with the flat house pieces (`lying_flat`) at full and phone size; the 11 past P7 notes as wider evidence; "0 false flags on the pose gallery"; each change its own Y. Taken from V3: the check's extra tests (each drawn piece joined to its parent, the person's picture one joined shape, knees and elbows within human bend, samples along every bone not only joints); keys posed in the body's own frame (hands placed from the chest); passing poses (car climb, lean-out, aim from a window) added to the pose gallery; passing shot 3 as a no-false-flag test. From the record: the screenplay says Jason "leans out", whole to the hips; versions 3-4 made a bigger sill-sitting climb.
## Faults in the pick
- F1 [fixed] V1 described the 3D body's look as its own fills with per-pixel depth; it now draws through `lying_flat` (house pieces, nearer over farther). The final version says so and shows that look first.
- F2 [fixed] V1's learn step had no cold critique of version 4; added from V2, so the picture-only faults are counted too.
- F3 [fixed] Stale spend figure (27.71%); the ledger now reads 28.82%.
- F4 [fixed] V1 left the three changes' Ys implicit; each is now its own Y.
- F5 [named] The check sits in drawing code every film uses: a slower render or false flags on old films are possible; it must pass the pose gallery, shot 3 and two past films with 0 false flags before it can refuse anything. Its speed is unchecked.
- F6 [named] Whether Sam accepts the flat-pieces-on-a-skeleton look upright, and whether the car gives depth for every piece, is unknown until the look sheet.
- F7 [named] All costs (about 1% + 1.5% + 3-4%) are unchecked estimates.
- F8 [named] The move itself: the screenplay says "leans out" (whole to the hips through the window); the sill-sitting climb is bigger than written. Shot 4's build proposal (rule 8) should put the written move to Sam first.
## Final version
**Learn (changes nothing; about 1% of a week, unchecked; Opus).** Replay version 4 (5edd1c1d) every frame. (a) A fresh helper critiques it cold: how many of the 8 cause-A notes (2, 3, 4, 6, 7, 8, 11, 15) it names. (b) Turn Jason's poses into the 3D skeleton (`lying.from_views`); run `body_faults`, `check_arm3` and the skeleton's collision shapes against the 3D car; count which notes each catches. (c) One sheet for Sam: 6 moments of version 4 beside the same skeleton drawn with the flat house pieces (`lying_flat`), at full and phone size, plus Jason from five views. (d) List what is missing upright.

**Change 1, the human-body check (own Y; about 1.5%).** Recorded where people are drawn (`views.person`, `lying.draw`), so no file bypasses it. Every person, every frame: bones at rig length in 3D (within 6%), elbows and knees in human range, each arm on its own side as drawn, each drawn piece joined to its parent and the person's picture one joined shape, no limb through another, samples along every bone outside every listed solid, a held gun within 10 degrees of its target while firing. The clip and animatic writer (including `--span` clips) refuses a render with an unnamed fault or without a critique record for that render (rule 89). Beat: catches every skeleton-held fault of version 4; 0 false flags on the pose gallery, shot 3 and two past films.

**Change 2, big moves on the 3D skeleton (own Y, only if Sam passes the look sheet; about 3-4%).** Climbs, turns past side-on, leaning out, car doors and falls are posed as 3D key poses in the body's own frame, drawn with the flat house pieces, hidden by the 3D car piece by piece; key poses shown on a five-view pose sheet in the rule 8 build proposal before building; passing poses go into the pose gallery. Pre-flight refuses a big move built on the flat standing figure. Beat: shot 4's next clip has 0 of the 8 cause-A notes; the next film's big move gets 0 repeated body notes.

Total about 6% of a week once (unchecked); later films reuse it. Shot 4's build proposal puts the screenplay's "leans out" move to Sam.
## For Sam
### Option 1: Measure, then a check nothing can skip, then a proper 3D skeleton
First, at no risk, we replay the bad version and measure which of your 8 body notes our existing tools and a fresh critic would have caught, and show you one sheet: the bad frames beside Jason drawn on a 3D skeleton (a hidden stick-figure that knows where each limb is in space) dressed in our usual flat pieces. Then, each on its own yes: a check that looks at every person in every frame as a body (joined arms, right lengths, right sides, nothing through the car, gun aimed right), placed where people are drawn so no shortcut skips it, and nothing reaches you with a fault unnamed; and big moves built on that skeleton. You would notice: no more twisted bodies reaching you, and a look sheet before any rebuild.
Lost: the old flat figure for big moves (kept for normal poses); a quick clip can no longer be sent before the critique runs.
Added: one look sheet for you; a check that can stop a clip; climb, lean and aim poses kept for future films.
### Option 2: The same, with the check at the usual pre-send checks
The same measuring and the same skeleton, but the body check and a "critic must have looked" rule run at the usual pre-send checks and when finishing, not where people are drawn. Simpler to add, but shot 4 was built in a practice file that runs none of those checks, and quick clips skip them, so the same slip could happen again.
Lost: the old flat figure for big moves; sending without a critique when finishing.
Added: one look sheet; the skeleton route; the body check; a critique rule at finishing.
