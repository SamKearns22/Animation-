# The figure system: bodies and movement in the flat cartoon films

Read this before building or animating any person in the TikTok parody series (and any film drawn with
`source/burnham.py` people). The code is `source/figure.py`; the checks run automatically in `source/preflight.py`.
It builds on `character-anatomy.md` and `movement.md` (written for the Yuletide trailer), translated to our
flat 2D cartoon. Breaking a rule on purpose is fine when the script or the style asks for it: name the break in
the code (`with figure.allow('reason'):`) so it is a decision, never an accident.

## 1. Why it exists
In The Patriots 2 every arm was typed in by hand, shot by shot, as an elbow point and a wrist point. Nothing tied
those points to the body:
- the same people's forearms measured from 112 to 260 units between shots (more than double);
- the medical staff's hands hung to their knees, because they were reaching down to a trolley drawn too low (the
  arm was stretched to the prop, instead of the prop being put at the right height);
- the protester's fingertips landed on the desk in front of the keyboard;
- an audit of the finished film with the new checks found arm faults in hundreds of drawings, all invisible to
  any check at the time.
The same pattern caused the other repeat renders: props placed separately in each shot, a background redrawn for
the reverse shot, a monitor drawn through a curtain, uniform stripes drawn over arms. The fix is the same each
time: **one source of truth, measured, and checked by code before a render.**

## 2. The body (our standing adult, in the person's own units)
Neck base at (0, 0), y downwards; a head is about 190 units tall (hh = 90). The figure is about 6 heads tall:
a big head and short legs, which is the series' look. Proportions are taken from landmarks (the classic drawing
canon: elbows at the bottom of the rib cage, wrists at the crotch, fingertips about mid-thigh; Loomis), not from
a realistic 8-head body:

| Landmark | Units | Rule |
|---|---|---|
| Shoulder joint | y 60, x = ±(shoulders − 14) | both arms hang from here |
| Waist | y 270 | a hanging elbow sits here |
| Crotch / hip joints | y 440 | a hanging wrist sits here; legs start here |
| Knee | y 700 | |
| Soles | y 928 | the floor line for a standing person |
| Upper arm | 210 | shoulder to elbow |
| Forearm | 170 | elbow to wrist |
| Hand contact point beyond the wrist | fist 14, palm 30, pointing fingertip 66 | |

Every person in a film uses the same lengths (children and very tall or short characters get their own `Rig`
with scaled lengths, decided in the cast list). Clothes never change the skeleton: a long tunic (`bottom=600`)
hangs past the hands; that is the garment, not long arms.

## 3. Limbs are solved, never typed
- **Say where the hand goes; the rig works out the elbow** (two-bone inverse kinematics, the way professional
  cut-out rigs such as Toon Boom Harmony work, with joint limits on elbows and knees). `rig.arm(side, target,
  shape, bend='out')` returns burnham's `(elbow, wrist, shape)`. The arm always keeps its length.
- **A target the arm can't reach is an error.** Move the body (step closer, lean) or the prop (raise the trolley),
  never stretch the arm. (`fail(... move the body or the prop, never stretch the arm)`.)
- **The elbow bends the natural way.** A relaxed or resting arm seen from the front (hanging at the sides, hands on
  a rail or trolley, clasped, in the lap) bends back into the picture: `bend='depth'` keeps the elbow on the line
  from shoulder to hand and draws the arm a little shorter. Never let a relaxed elbow wing out sideways with the
  hands folding in to the body: nobody stands like that (The Patriots 2's first rig did exactly this). Sideways
  elbows (`'out'`) are for hands on hips, typing, gestures; `'in'` when a hand crosses the body (clutching the chest).
- **Foreshortening only shortens.** An arm reaching towards or away from the camera (typing towards the screen) is
  given `depth` (0-0.6) and is drawn shorter; nothing is ever drawn longer than the rig.
- **The guard measures every arm drawn anywhere** (`figure.guard(B)`), including hand-typed ones and other people's
  code: an upper arm or forearm more than 6% too long, an arm squashed below 40%, or an elbow folded tighter than
  25 degrees stops the render with the shot and time.
- **Standard poses** (`rig.pose(name)`): sides, hips, clasped, rail (hands on a rail or mattress at waist height),
  clutch, point (at a target, the other hand on the hip), reach (as far as the arm allows), typing (fingertips on
  given keys). New poses are added to the library, not typed into a shot.

## 4. Contacts: proof that things touch
- **Feet on the floor:** a standing person's soles are on the floor line (`check_feet_on`); seated, the hips are on
  the seat (`check_seated`).
- **Hands on things:** a contact point (fingertip, palm on a rail) must land on the thing (`check_on`), e.g. the
  typing fingertips inside the keyboard. Things a person uses sit at real working heights: a desk and keyboard
  at elbow height when seated; a hospital trolley's mattress at the staff's waist; a counter at hip height.
- **Lying down:** a person lying on a bed is drawn side-on on their back, face up, resting on the mattress, the
  face in profile (forehead, brow, nose, mouth, chin), never a front view turned on its side. A mask or a blanket
  is fitted to the profile.
- **Seated at a desk** (the protester): thighs under the desk, forearms over it, hands on the keyboard.

## 5. Sets and props: one plan per place (see best-practice.md, 1.3)
- Every location is built once and every shot is that set from another camera; props are part of the set, with
  one place each in a written plan (`DESK_ITEMS` in patriots2.py: left/right from the character, depth across the
  desk). Every camera draws from the plan.
- A recurring object (a vehicle, a chair, a prop seen in several shots) is one drawing at one size relative to
  its people: its scale comes from the person's scale through a fixed ratio, so it can't change between shots.
- Seated people's hips are on the seat; behind a desk seen from the front, their legs and the chair's stand show in
  the knee space under it.
- Set pieces that must stay apart are listed with their outlines and checked (`check_apart`): monitor and
  curtain, dispenser and cupboard, items on a desk.
- Uniform details (reflective bands, badges, lanyards) are part of the garment, drawn before the arms, so arms
  always pass in front of them.

## 5b. Polish: shadows and hands (`source/kit.py`, test sheet `python3 kit.py sheet OUT.png`)
- **Contact shadows:** everything that touches the ground gets a soft flat shadow where it touches: people's feet
  (`kit.feet_shadow`), chair castors, bins, bags, boxes, a trolley's wheels (`kit.contact_shadow`). Draw it before
  the thing itself. Nothing floats.
- **Hands library** (after `kit.install(B)`; each shape's contact offset is in `figure.HAND`): relaxed, flat
  (resting on a surface), cup (a takeaway cup, the cup drawn with it), phone, pen, wave, thumbs, grip (round a rail,
  rope or handle) plus burnham's own fist, point and palm. Props held in a hand are drawn with the hand at one size
  against the person, like any recurring object.
- **Holding something** (`rig.pose('hold', side, shape, lift)`): the upper arm hangs by the side and the forearm
  comes forward towards the viewer, drawn shorter. This is how people hold a cup, a phone or a pen; never an elbow
  lifted out to the side to bring the hand in front of the chest.

## 6. Movement and timing (numbers from movement.md, at our 12 drawings a second)
- **Slow in, slow out** (`ease`), **anticipation** before a big move (`anticipate`: a small opposite move first),
  **follow-through** (`overshoot`: arrive a touch past the pose and settle).
- **Moving holds:** breathing lifts the chest a few units every ~4 s (`breath`); blinks are irregular, 8-21 a
  minute (more when talking or upset), about two drawings long (`blinks`, `blinking`), often with a glance.
- **Eyes lead:** a glance is a jump of the eyes in one drawing (never eased), the head following a beat later
  over ~0.3 s (`saccade`, `eyes_then_head`). Eyes point at the person spoken to (`look_at`).
- **Walks:** about two steps a second (6 drawings a step); the stride matches the speed so feet never slide
  (`walk`); a run is about three steps a second. People pushing a trolley lean into it.
- **No twins:** left and right, and people side by side, never move identically at the same moment: offset their
  phases.
- **Mouths: proper mouth shapes** (`source/mouths.py`, test sheet `python3 mouths.py sheet OUT.png`). The ten
  standard cartoon shapes (Preston Blair): rest, M/B/P (lips shut), etc (most consonants, teeth nearly together),
  E (wide), A/I (wide open), O (round), U (small round), W/Q (pucker), F/V (teeth on lip), L (tongue up).
  `mouths.track(script_line, stretches, envelope)` spreads the line's words over the recording's own stretches of
  speech by syllables, turns each word's spelling into shapes, closes the mouth wherever the recording is quiet,
  and shows each shape a twelfth of a second before its sound (that reads as in sync). Then
  `sp['mouth'] = 'v:' + mouths.at(track, t)` after `mouths.install(B)`. The stretches come from
  `mossad_audio.pauses`, so the words line up with Sam's real pauses. A character who is typing or thinking a
  letter we hear does not move their mouth.
- **Secondary motion** (`source/kit.py`): anything hanging off a body (lanyards, headscarf tails, ponytails, ropes,
  a dangling sign) follows a beat behind: `kit.follow(t, keys)` gives the lag, the swing past and the settle (a
  damped spring) after each move of the body; `kit.idle_sway` keeps it drifting gently in a held pose;
  `kit.dangle(...)` draws the strap with its badge or weight.
- **Deadpan:** stillness is a choice; even a deadpan character acts beat by beat with the face (brows, a blink, a
  glance), while the camera stays still.

## 7. In the satirical series' style
- Flat shapes, clean outlines, almond eyes with small pupils, soft shading; the stylisation is in the shapes, not
  in broken anatomy. Arms keep their length, elbows bend the right way, feet stand on the floor.
- Comic exaggeration is allowed, named: a deliberate stretch or a squash for a gag goes inside
  `figure.allow('…')`, so it shows in the review as a choice.
- Real-world groups and settings are checked against sources before drawing (who travels in small boats; what a
  UK ambulance carries); everyone is drawn with dignity and individual faces. Hair, headscarves and clothing are
  drawn deliberately per person (no style borrowed from another character that means something else, e.g. a
  greying man's hair on young men).

## 8. The checks, and when they run
| Check | Where | Stops the render when |
|---|---|---|
| Arm guard | every arm drawn (`figure.guard`) | a segment is >6% too long, <40%, or the elbow folds past 25° |
| Unreachable target | `Rig.arm` | the hand can't reach without stretching |
| Fingertips on the keyboard | patriots2 `check_on_keys` | a typing fingertip misses the keys |
| Set pieces apart | `check_apart` (ward, ambulance, desk) | two listed outlines overlap |
| Feet / seat contact | `check_feet_on`, `check_seated` | soles off the floor, hips off the seat |
| Captions | `preflight.py` | over 2 rows, 700 px or 42 characters a row; faster than ~200 words a minute |
| Shot length | `preflight.py` | a shot over 8 s (flagged: fine when chosen) |
| Duplicate recordings | `voices.py` | two files hold the same take |

`python3 preflight.py FILM OUT_DIR` runs all of them on every third frame (a couple of minutes) and makes a
contact sheet with the safe area drawn on, before the first animatic.

## 9. What is still missing (next steps, in order of value)
1. **A cast model sheet per character, before the storyboard:** front, three-quarter, profile, back, seated and
   lying views, at the same proportions. We invented the lying profile late; a turnaround up front would have
   caught it.
2. ~~Proper mouth shapes~~, ~~a hands library~~, ~~contact shadows~~ and ~~secondary motion~~: built (October
   2026, `mouths.py` and `kit.py`; sections 5b and 6). First used in the next film; check them on its animatic.
3. **Mouth shapes for profile and three-quarter faces** (the set is drawn for the front view).
4. **Back and three-quarter-back views** of the person (people walking away; the over-the-shoulder shot).
5. **A ground plane for every set** (the camera-and-floor model in peepee.py) so that people's sizes follow
   their distance automatically and feet always meet the floor.
6. **People-against-props overlap checks** (an arm through a can, a body through a trolley), extending
   `check_apart` from set pieces to people's outlines.
