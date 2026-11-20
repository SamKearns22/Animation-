# Proposal: How to build big 2D body moves (a climb, a turn, a lean-out) and a check that every person in every frame is a human body

Status: open

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
