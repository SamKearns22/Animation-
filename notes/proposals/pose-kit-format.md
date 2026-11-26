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
- Cost: notes/ledger/r7.json, estimate 6.0, chats about 2.2-2.3 each on Opus; Sam's budget question at 9.8% (chat 10 handover).
- Sam's notes that each cost a round, with "Why missed" lines: notes/r7.md Brief checklist (bum/circular knees; "legs
  look awful" on sheet v4, all four views; "you changed her clothes?" (outfit redrawn unasked); "way too
  curvaceous"; purple under the jacket hem (side); shoes clipping (3/4) and confused shoe shapes (side), the sheet's
  crop cut the feet off; legs "spread ... bearing the crotch" and the jacket triangle on 'upright, apart').
- What Sam passed: "This pose is 100% correct" / "she is FINALLY correct" (chat 8, mode 'body': solid legs and seat
  under the unchanged flat outfit); chat 10's three-quarters and shoes; chat 11's 'upright, apart' awaits his look.
- What worked in chat 11 (one round, about 1 chat): Sam's marked picture saved; a picture check written that reads his
  own frame (solid_seat.apart_faults) and proved red on it and green on the fix (kittests legs_apart_spread,
  jacket_triangle) before showing him; the limbs placed by where the knee goes (sitting._leg_by_knee) instead of
  tuning foot numbers (chat 10's foot tuning had pushed the knees out); the locked pose proved pixel-identical; the new
  look opt-in by a flag on the pose (lap_open, leg_gap) so locked poses and old films cannot move; a 2-pose labelled
  sheet at full size with the feet in frame.
- What failed: reference photo search refused by Wikimedia and Openverse (too many requests, chat 11); chat 6-8 judges
  shown pictures before Sam; outfit changed with no Lost: line (chat 8); checks that passed numbers while the picture
  was wrong (chat 10 all seated checks 0 on the spread legs); JPEG pictures fooled a colour check (chat 11).
- Existing pieces: guides/kit-catalogue.md, guides/figure-rig.md, guides/pose-gallery.md, source/solid_seat.py
  (checks(), shoe_faults, apart_faults), notes/learn/seated/solid/sheet_solid.py and may_sheet.py, source/kittests.py.

## Record
notes/r7.md
notes/archive/r7-handovers.md
notes/ledger/r7.json
notes/learn/seated/
guides/kit-catalogue.md
guides/figure-rig.md
guides/pose-gallery.md
guides/job-packs.md
source/solid_seat.py
source/sitting.py
source/kittests.py
