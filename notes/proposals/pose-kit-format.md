# Proposal: A build format for new pose kits, from what worked in R7

Status: open

## Problem
Sam, 26 Nov (after R7 chat 11): "Please codify what succeeded in this build into a build format that can
successfully create kits for other poses. This was an arduous and expensive process and we should learn what worked
so that we don't repeat the mistakes of this process."
R7 (a natural seated lower body for May) took 11 chats and about 9.8% of a week against a 6% estimate (25 Nov Sam:
"Building body kits is costing huge unacceptable expenditure ... This cannot continue"). Most of Sam's notes were
faults he saw at a glance that no check had looked for. The next pose kits (other seated poses, other characters,
standing or moving poses) have no written order of work to follow, so they could repeat the same rounds.

## Facts
- Sam, 26 Nov (on chat 11's first draft of this job): "I'm not sure you have understood the crux of our improvement
  which was implementing the full body model and then layering clothes separately. Please check all R7 chats for
  what worked and then update the job." Chat 11's first facts and idea centred on checks and placement: wrong crux.
- Chats 1-5 (notes/archive/r7-handovers.md): the legs drawn as hand-made flat outlines and guessed 3D tubes
  (views.seated_lower, _r7_outline: arch, calf, cloth widths, shade tricks); each patch moved another view; blind
  judges stayed at 2-3 of 5 for four rounds (results-r7.md .. r7c4.md); Sam: "the legs look awful" (sheet v4).
  Chat 5's judged proposal (notes/proposals/seated-legs-3d.md, Final version, root cause): "the tubes are guessed ...
  and hiding is faked by cut-off numbers and shading, so each patch moves another view."
- Chat 6: source/solid_seat.py: the measured MakeHuman body (the GTA bench's way: posed by its own skin weights as ONE
  closed body, one depth pass, house flat colours and ink) built from any kit person's spec, posed on the kit's own
  joints (sitting.realize), drawn through the kit's own camera; trousers as a shell on the body. Judges rose at once
  (side 4/4/4, the rest 3-4; results-r7c6.md).
- Chat 7: patching the seams between solid legs and flat torso again; Sam: "Is there a more intelligent way?";
  Sam picked option 2, the whole person solid (r7.md "Sam's pick").
- Chat 8: mode seat_solid='body': the WHOLE solid body under May's UNCHANGED flat posted outfit (torso, arms, blouse,
  lapels drawn as before on top), the solid shown only below the jacket's seated hem. Sam: "This pose is 100%
  correct", "she is FINALLY correct. She has correct anatomy and outfit." First try had redrawn her clothes on the
  body: "you changed her clothes?", "This is the correct outfit. You have drawn a poor version of it".
- Chats 9-11: every later note was at a layer's edge, not the body: curves of the turned flat torso over the body
  (turned_curves), jacket colour under the hem (trousers seat layer), shoes vs trouser hem (shoe layer), the jacket
  hanging into the gap between parted legs (lap_open). Each fixed in the layer, with a picture check proved on Sam's
  saved frame (kittests turned_curves, jacket_under_hem, shoe_shapes, legs_apart_spread, jacket_triangle).
- New poses on the body are made by joint targets (sitting._leg_by_knee, chat 11) behind a pose flag, so locked
  poses stay pixel-identical (seated_r7_switch; chat 11's 'upright' diff: none).
- Cost: notes/ledger/r7.json, estimate 6.0; chats about 2.2-2.3 each on Opus; 9.87% of 15% at chat 10. Chats 1-5
  and 7 (outline patching) produced nothing kept in the final look.
- Still untested: mode 'body' for standing and moving poses; other people (Kemi, Blair) in mode 'body'; clothes other
  than a suit jacket over trousers (vest, skirt, dress). notes/proposals/model-body-all.md is the related chain.

## Record
notes/r7.md
notes/archive/r7-handovers.md
notes/ledger/r7.json
notes/learn/seated/
guides/kit-catalogue.md
guides/figure-rig.md
guides/pose-gallery.md
guides/job-packs.md
notes/proposals/seated-legs-3d.md
notes/proposals/model-body-all.md
notes/learn/seated/judge/
source/views.py
source/solid_seat.py
source/sitting.py
source/kittests.py
