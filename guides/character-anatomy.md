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
4. **The smile is the whole face.** A real (Duchenne) smile: cheeks lift, lower eyelids rise and bunch, crow's
   feet at the outer eye corners, nasolabial folds deepen, lips thin and stretch. A mouth-only smile on a still
   face is exactly the "Barbie" look.
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
  little finger ends at the last knuckle of the ring finger.
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

## 4. Checklist before showing any character shot
- [ ] Built on the MakeHuman body (or another measured, licensed human), not hand-placed blobs
- [ ] Face asymmetry added; smile involves cheeks and eyes
- [ ] Eyes converge on what she is looking at
- [ ] Proportions checked against section 2 from the front and side
- [ ] Every hand–object contact measured in 3D; no gaps or overlaps
- [ ] Thumb opposes the fingers; wrist straight
- [ ] Looked at it at full size *and* phone size
