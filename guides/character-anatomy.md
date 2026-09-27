# Drawing people for the film: anatomy guide

Read this before building or changing any character. It records what went wrong with the first mother shot
("plastic Barbie face, hands not connected to the tools") and how to avoid it.

## 1. The big decision: stop sculpting bodies from scratch

The first shot built her face, body and hands out of hand-placed blobs (ellipsoids, capsules). That is why she
looked like a mannequin: no skull, cheekbones, tendons or knuckles underneath, just smooth shapes guessed by eye.
Professionals never do this. They start from a measured human model and adjust it.

**Use MakeHuman's base human instead.** It is a full, anatomically correct body (head, hands with proper
knuckles and fingers, ears) with a skeleton, plus thousands of "sliders" (targets) for age, sex, weight, face
shape, nose, lips, eyes, etc.

- Licence: since September 2020 the base mesh, targets, skeleton, poses and expressions are all **CC0**
  (public domain), including when used from a script, and renders are ours to use however we like.
  Source: https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.md
- Download works from the cloud sessions: `https://raw.githubusercontent.com/makehumancommunity/makehuman/master/makehuman/data/...`
  - `3dobjs/base.obj` (the body, 1.7 MB)
  - `targets/...` (shape sliders, e.g. `macrodetails/universal-female-young-averagemuscle-averageweight.target`)
  - `rigs/default.mhskel` (the skeleton, for posing arms, fingers and head)
- Download at the start of work; don't commit their files to our repo (they're large and not ours).
- Our renderer draws smooth shapes (distance fields), so the mesh has to be converted: turn the posed triangle
  mesh into a distance grid (same kind of grid the head already uses), with finer grids for face and hands.

Keep our own work for what makes her *ours*: her particular face shape (via sliders), hair, clothes, the
kitchen, lighting and the pencil style.

## 2. Why faces look "plastic" and how to fix it

Research on the uncanny valley (MacDorman 2009; Schwind 2018) finds eeriness comes from *mismatched* cues: a
realistic-shaped face with a too-smooth surface, or realistic skin on wrong proportions. Fixes, in order:

1. **Real bone structure.** Brow ridge, cheekbones, jaw angle and chin must read through the skin. A face with
   no underlying bone reads as a doll.
2. **Asymmetry.** No real face is mirror-symmetric. Nudge one eye 1 mm higher, the mouth corner on one side
   up more in the smile, one brow slightly more arched, the nose tip 1 mm off-centre, the parting off-centre.
3. **Surface detail.** Skin isn't smooth: faint pores, the fold of the upper eyelid, the tear duct, a slightly
   wet lower lid rim, lip creases running vertically, a nasolabial fold that deepens when smiling, fine hair at
   the hairline. In pencil these become a few light marks, not a smooth gradient.
4. **The smile is the whole face.** A real (Duchenne) smile needs two muscles at once: zygomaticus major (pulls
   the mouth corners up and back) and orbicularis oculi (the ring round the eye). Paul Ekman's markers: the
   cheeks are pulled up; the skin below the eye bags or bulges; the lower eyelid moves up; crow's feet appear
   at the outer corners; the skin between brow and upper lid is pulled slightly down; the brows drop very
   slightly. Nasolabial folds deepen. A mouth-only smile on a still face is exactly the "Barbie" look.
   In MakeHuman these are face pose units: LeftCheekUp/RightCheekUp, LeftLowerLidUp/RightLowerLidUp, the
   mouth-corner units, NasolabialDeepener and a touch of BrowDown. Use them together, slightly unequal on the
   two sides.
5. **Eyes.** Both eyes converge on the *same point* (her daughter), not parallel. Upper lid covers the top
   1–2 mm of the iris; lower lid touches the bottom. Eyelids have thickness and cast a shadow on the eyeball.
   Catchlight in both eyes in the same place.
6. **Don't over-render.** A pencil drawing *suggests*. Stylised line + shading hides small errors better than
   smooth realistic shading, which exposes them (this is why Waltz With Bashir works: bold lines, flat tone).

### Proportions (adult woman, head-on)
- Eyes sit halfway down the head (top of skull to chin). One eye-width between the eyes.
- Face in thirds: hairline→brow, brow→bottom of nose, bottom of nose→chin, roughly equal (lower third can be a
  touch shorter for a feminine face). Mouth one third of the way from nose to chin.
- Mouth corners line up with the centres of the pupils; nostril wings with the inner eye corners.
- Ears run from brow line to nose bottom.
- Adult is ~7.5 heads tall. Shoulders ~2 heads wide for a woman, and slope down from the neck (trapezius);
  never square. Neck rises forward from the shoulders, not straight up.
- Chest (nipple line) ~1 head below the chin; waist ~2 heads; elbow at waist height when arm hangs.

## 3. Hands: the most-noticed part after faces

- Palm is roughly square; fingers are about as long as the palm. Middle finger longest; ring ≈ index;
  little finger ends at the last knuckle of the ring finger. The whole hand is about 2/3 of the forearm.
- Each finger's first bone is about as long as the other two together; bones get smaller towards the tip.
- Fingers start at the knuckles seen on the *back* of the hand; on the palm side the skin creases sit further
  out, so fingers look shorter from the palm side.
- The thumb has two visible joints and is rotated: its nail faces sideways when the other nails face up. It
  spreads much further than the fingers.
- A relaxed hand tilts slightly towards the little-finger side; tilting towards the thumb reads as effort.
- Knuckles form an arc, not a straight line. Fingers taper and each joint bends only one way (hinge).
- Thumb starts near the wrist, not at the side of the palm, and swings round in front of the palm to oppose
  the fingers. It is the most common thing to get wrong (in shot 1 it stuck up in the air).
- Hands are connected: forearm muscles and tendons flow into the wrist; the wrist is narrower than the palm.

### Gripping the cleaver (from cooking guides, e.g. Kamikoto's chef's guide)
- Hold the handle **right up against the blade**, not at the end.
- Grip 1 (chopping): thumb on one side of the handle where it meets the blade, all four fingers curled round
  the other side.
- Grip 2 (control, what chefs prefer): pinch the *blade* just past the handle between thumb and index finger,
  the other three fingers wrapped round the handle.
- Wrist stays straight in line with the forearm; the knuckles face forward/outward.
- Every contact must be real: fingers *touch* the handle all the way round. No gaps, no fingers passing through
  it. Check this by measuring distances in 3D (skin to handle surface ≈ 0), not just by looking.

### The other hand (steadying the meat)
- Chefs use the "claw": fingertips curled under, knuckles forward. For the story, she instead has her hand
  resting too flat and too close to the blade, which is the point, but the hand must still look relaxed and
  weighted: fingers slightly curved, pads pressing into the meat (make a dent), wrist resting.

## 4. Faces: female structure
- The forehead's shape comes almost entirely from the frontal bone (Anatomy for Sculptors): female foreheads are
  rounder and more upright with little brow ridge; the hairline is rounded.
- Softer, smaller jaw angle and chin; cheekbones carry the width; fuller lips; eyebrows sit on (not below) the
  brow bone and arch towards the outer third.

## 5. How MakeHuman works (learned from its own code)
- Units: 1 unit = 1 decimetre (its height in cm is 10 × the bounding box). Y up, face towards +Z.
- `base.obj` holds helper geometry too (tights, joint markers); use only the `body` group for skin.
- Shape "targets" are text files: `vertex_index dx dy dz`. Macro targets are mixed by multiplying the values
  in their names, e.g. weight of `universal-female-young-averagemuscle-averageweight` =
  female × young × averagemuscle × averageweight, where gender 0..1 gives female = 1 − gender; age 0.5 = 25
  years (young = 1 − old, old = 2·age − 1 above 0.5); muscle/weight 0.5 = all "average". Ethnic targets
  (`caucasian-female-young` etc.) are weighted by ethnic mix × gender × age.
- Skeleton (`default.mhskel`, 163 bones incl. face and every finger joint): each joint = the average of a
  listed set of vertices; each bone's X axis comes from the normal of a named plane of three joints; Y runs
  head→tail; Z = X × Y.
- Posing: each bone gets a local rotation; global = parent_global · rest_relative · pose; each vertex moves by
  the weighted sum of (global · rest_global⁻¹) over its bones (weights in `default_weights.mhw`). This is
  standard linear-blend skinning.
- Expressions: `face-poseunits.bvh` has one frame per named unit (list in `face-poseunits.json`). A unit's
  frame gives local rotations for face bones; blending = slerp each from rest by its weight, then multiply.
- Eyes: `data/eyes/high-poly` is a separate eye mesh fitted to the head.

## 6. Lessons from building her (so they aren't learned twice)
- MakeHuman's pose files give rotations along the **world** axes; convert each to the bone's own axes
  (R_local = R_rest^T · R · R_rest) before skinning, or expressions come out as grotesque pouts.
- Its face units file is **z-up**: a Y rotation becomes a negated Z one and Z becomes Y.
- Don't guess finger angles. `mhuman.solve_grip` curls the fingers and thumb until they wrap a cylinder the
  size of the real handle (touching all round), keeps joints in their natural range and stops the thumb
  passing through the fingers. Then the prop is placed to fit the hand, not the other way round.
- Don't force the handle's angle in the palm to line up the arm: keep the good grip and let the **wrist** bend
  within its range (flexion ±50°, sideways ±25°) so the forearm heads back to a natural elbow. Forcing the
  angle wrecked the grip; an unbent wrist put the elbow out like a chicken wing.
- Linear-blend skinning loses volume at big bends: keep finger joints under ~90°.
- A smile at full strength squints the eyes at a downward three-quarter view: keep the lower-lid raise gentle
  (~0.2) and the upper lids open.
- Features that are colour, not shape (lip colour, brows) must be re-fitted to the new head by *measuring*
  it (e.g. the mouth's depth profile gave lip heights and corners), never carried over from an old head.

- Hands that *rest* on something need the same care as hands that grip: measure the hand's surface against
  the object's and lift/tilt the hand until it just touches (skin pressing in ~1 mm), never trust a guessed
  height. The left hand on the ham had sunk 4 cm in before this check existed.

- **A fix must not break the rest.** Moving a hand moved its wrist twice and left the hand floating
  below the sleeve. Now the scene refuses to build if any hand is more than 3 mm from the end of its
  sleeve, and after every change the *whole* picture is reviewed, not just the part that was fixed.

## 7. Checklist before showing any character shot
- [ ] Built on the MakeHuman body (or another measured, licensed human), not hand-placed blobs
- [ ] Face asymmetry added; smile involves cheeks and eyes
- [ ] Eyes converge on what she is looking at
- [ ] Proportions checked against section 2 from the front and side
- [ ] Every hand–object contact measured in 3D; no gaps or overlaps
- [ ] Thumb opposes the fingers; wrist straight
- [ ] Looked at the whole picture (not just the part changed) at full size *and* phone size
- [ ] Every hand joins its arm (checked automatically)
