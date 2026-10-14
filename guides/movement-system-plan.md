# Plan: walking, running and turning for every film (agreed with Sam before building)

Written 14 Oct after Sam's notes on Bingo Bingo's animatic v2: the walk "looks horrible", Zack's turn "flips like a
piece of paper", and the card reveal must be done with the camera's frame, not blur. The walk and the turn are
structural: our people library (burnham.py) draws everyone from the front only, so anything that moves sideways or
turns round has been faked (a squashed front view, a squashed body for a turn). This plan fixes that once, for all
films (the satire template picks it up automatically).

## The professional references it is built on
- **Richard Williams, *The Animator's Survival Kit*** (2001): every step is four key poses: contact (heel just
  touching, legs widest), down (weight lands, body lowest, arms widest), passing (the free leg passes the standing
  one, body rising), up (pushing off, body highest). Tempo (at 24 fps; we draw on 12): 16-frame steps = a stroll
  (1.5 steps a second), 12 = a natural, business-like walk (2), 8 = a brisk "cartoon" walk (3), 6 = a run (4),
  4 = a very fast run/sprint (6). In a walk one foot is always on the ground; in a run both leave it for a frame or
  more. Arms swing opposite the legs, widest on the down; feet pick up slowly and put down fast; vary a fast run's
  silhouettes so it doesn't read as a loop.
- **Eadweard Muybridge, *The Human Figure in Motion*** (1887, public domain): photographed walks, runs and turns from
  the side, front, back and three-quarter angles at the same moment. The ground truth for how a stride looks from
  each angle.
- **Gait biomechanics** (David Winter, *Biomechanics and Motor Control of Human Movement*): the normal angles of hip,
  knee and ankle through a stride, and real speeds and cadences: stroll about 1 m/s and 90-100 steps a minute; walk
  1.4 m/s and 110-120; brisk 1.8 m/s and 130; run 3-4 m/s and 160-180; sprint 6-9 m/s and 190+.
- **Character turnarounds** (the industry model-sheet standard): every character drawn in front, front
  three-quarter, profile, back three-quarter and back views at the same proportions.
- **Cut-out animation as South Park and Toon Boom Harmony do it**: a turn is never a flat squash. Each body part
  *swaps drawings* to the next view (front -> three-quarter -> profile ...), holding each for a frame or two, the
  eyes and head leading, the body following a frame later, the feet stepping round, sometimes with one quick smear
  drawing in the middle. It reads as a quick snappy turn because every frame is a real drawing of the person.

## What gets built
1. **A turnaround for everyone** (`views.py`): eight views (front, three-quarter front left/right, profile left/right,
   three-quarter back left/right, back) drawn from the same person spec, same proportions, same new limbs. The face
   moves round the head with the view (eyes, nose and mouth slide over and the far eye narrows; in profile a real
   profile of brow, nose, lips and chin, with the profile mouth shapes for lip sync), the torso narrows and shows its
   side, the near arm and leg come in front of the body, the far ones go behind. Every character's cast sheet
   shows all eight views, for approval before animating (as satire.md already asks).
2. **Turns** (`views.turn`): the South Park method above. A half turn (front to back) takes about 4-6 drawings at
   12 fps: eyes glance first, head leads by a frame, body swaps view by view, feet take two small steps round.
   Optional one-frame smear. No squashing.
3. **Gaits on a small hidden 3D skeleton** (`gait.py`): hips, knees, ankles, toes, shoulders, elbows and wrists
   move in 3D through Williams' key poses with the reference angles and timings. Five gaits: stroll, walk, pace
   (walking a line and turning at each end), run, sprint, each with its own steps a second, stride, bounce, lean and
   arm swing (a sprint leans forward, pumps the arms, flies for a frame or two). The skeleton can face any
   direction, so a walk can go across, towards, away or diagonally: the camera looks at it from the right angle,
   our flat drawing of that view is put on it (step 1), and the body and face always face the way the person is
   going (or are told to look somewhere else, head and eyes only).
4. **Checks**, run by preflight on every frame: a planted foot never slides; the body faces where it travels;
   the head never turns more than about 90 degrees from the body; steps a second match the gait; one foot is always
   down in a walk; both leave the ground in a run.
5. **A test reel for Sam** before anything goes into a film: each gait at five angles (across, towards, away, two
   diagonals), a pace with its turns, and the turn from front to back, side by side with the matching
   Muybridge plates' timing. Sam approves it; then it becomes the standard in the satire template, figure-rig.md and
   satire.md, and the old walker.py is retired.

## Bingo Bingo meanwhile
- **The card reveal by framing:** a 9:16 frame wide enough to read a line of the A3 card always holds the whole card
  (the frame is taller for its width than the card is), so the camera can only hide the other items if they are
  written in different places on the card. The card is redrawn as a real brainstorm sheet: item 1 top left, item 2
  top right, item 3 written across the bottom; each close-up frames only its own item (narrow and high), so the next
  one is out of frame until the camera moves to it. No blur.
- The walk-in and Zack's spin wait for steps 1-3 and are then rebuilt with them.

## Agreed with Sam, 14 Oct (after his critique round)
- **Build to order:** the shared engine once; angles, gaits and poses only when a script needs them, then kept on a
  pose menu for every film after.
- **Order:** (1) finish Bingo Bingo with film cheats (done: animatic v3); (2) one main line of work (all branches merged,
  every chat starts from it); (3) research pass -> `guides/reference-pack.md` (limited animation, "on twos", as the style
  target; realism only keeps poses believable); (4) look test: Zack in three-quarter and profile plus one short walk,
  Sam approves before any engine is built; (5) build: **a floor-and-camera model with true perspective first** (Sam:
  "perspective is important"), angles, walk and turn, core pack (standing styles, talking gestures, sitting and standing
  up, holding things), combat pack (punch, kick, sword swing, taking a blow and falling), car-ready seated poses and
  getting in and out (the car itself drawn per film); checks; footstep and hit sounds; a regression still from every
  finished film before and after; (6) one **Satire film package**: the people library, figure.py, limbs.py, the new
  views and gaits, satire_style, filmkit and film_engine combined into one efficient package behind the satire
  template (walker.py retired, nothing duplicated).
- **Real people from the side:** Sam sends profile photos when he can; otherwise the side and back views are worked out
  logically from what the front shows (hairline, beard line, nose and jaw from the front photos).
