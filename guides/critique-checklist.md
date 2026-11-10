# The critique checklist (Job H, 10 Nov): the faults Sam has flagged, as lines a fresh eye can confirm on a picture

**What it is for:** rule 89's critique. A fresh helper (a new agent each pass, nothing of the chat) first describes the
sheet cold, then reads this list and answers every line that fits each panel: ok, FAULT (where, what) or CAN'T TELL
(what picture would show it). `source/critique.py` gives it only section A and the sections on the sheet, never
"Came from". Each line is something right that the helper confirms; "Look:" says what the sheet must show for it
(a CAN'T TELL means the sheet failed, not the film); "Tool:" names a check that also holds it (tools miss things, so
the helper still looks). The number in brackets is how many of Sam's notes the line has had.

**How Sam's notes change it (each note adds one line or strengthens one):**
1. A note that names a fault (something wrong a fresh eye could spot) gets a line id in the film's notes table.
   A wish (more traffic, add a pram) is a brief item, not a line. A note with two faults counts on both lines.
2. A line already covers it: its count goes up and the note goes into "Came from". It is also a miss: say why (the
   line was unclear: reword it; the sheet didn't show it: change its Look; no critique ran) and fix that.
3. No line covers it: add one (30 words at most, a statement checkable on a picture, with Look and any Tool) with the
   next free id in its section. Ids never change or get reused; lines sit in order of count (A stays as written).
   At most 12 lines a section: a 13th merges the two closest (counts added, the older id kept).
4. Never ask the helper to name a real person from a face: it compares features with the references (likeness is
   rule 49's tool).

## A. Every sheet
- A1 (2) Everything the brief puts in a panel is named right in the cold look at phone size, and nothing reads as something it isn't (a flat blob, a rude shape). Look: look.md against brief.md.
- A2 (2) Ours matches each reference beside it: how many, colours, positions, which way it faces, proportions, the details that make it that thing. Look: check sheet. Tool: compare.py.
- A3 (3) A fault found on one panel is looked for on every panel of the same kind, not only where it was found or noted (rule 56). Look: every panel.
- A4 (1) The Hook Text box covers nothing that matters (a face, the action, a sign). Look: the Hook Text frame.

## P. People
- P1 (10) Every hand that holds or rests on something touches it: no gap, no hover, nothing through the fingers; the prop sits the right way round in the hand. Look: each hand on a prop, full size, every view. Tool: handcheck (held), kitchecks.rests.
- P2 (10) Acting reads: each face and body shows the feeling the acting list names on that beat, big enough for a phone, not overdone. Look: look.md feelings against the beats in brief.md.
- P3 (8) Arms bend only at the elbow, the right way, by a natural amount; no rubber or broken arm; upper arm and forearm keep their length. Look: arms at both ends of each move.
- P4 (8) Faces match their references: hair, beard (its five lines), glasses, colouring, how open the eyes are. Look: face crop beside each reference. Tool: likeness.py, beard tool.
- P5 (7) Each arm grows out of its shoulder in one flowing line: no gap, step, stray tick, or arm starting inside the chest, from every view. Look: each shoulder, full size, every view. Tool: handcheck (seam).
- P6 (7) Hands read as hands: a point shows one finger out along the forearm (rule 41); no hand lost behind a prop or body where it should show. Look: each hand, full size. Tool: handcheck.
- P7 (6) Anyone lying rests their weight on the ground: a neck, each arm on its own side, nothing hovering, sunk or curled up off the floor; a person, not a balloon. Look: the body from the shot's camera. Tool: lying.py.
- P8 (5) Turned, from behind or mirrored, the body still makes sense: hands on the right sides, nothing held in front drawn over the back, the head turned with the body. Look: each person in every view the film uses. Tool: views (AVOID lists).
- P9 (5) Feet stand on the ground and seated people sit on the seat: no float, no slide while standing, legs the same length; a bob never sinks them. Look: feet and seat, first and last frame of each shot.
- P10 (4) No body passes through another person, prop or set at a hit, step or touch; contact looks like touch. Look: frames at each contact. Tool: clipcheck.
- P11 (4) Each head sits on a neck of believable length and is the right size for the body and for any helmet or hood. Look: head and neck, full size.
- P12 (3) Mouths move only on that person's words and close between lines. Look: frames labelled with who speaks. Tool: the mouth check.

## C. Creatures
- C1 (2) What it hits reacts (crumples, breaks, moves) and nothing passes through it or through what it hits. Look: frames at each hit.
- C2 (1) It has the parts its reference has, joined where they belong (a neck between head and body, wings from the shoulders), shaped like the animal, not a blob. Look: one alone at full size beside its reference.
- C3 (1) It reads as that animal at its smallest size and from every angle the film uses (from above, far off): outline and colour say what it is. Look: the smallest it appears, phone size.
- C4 (1) It keeps a believable distance from people unless the brief says otherwise (no pigeon at his face). Look: each shot it is in.

## O. Props, text and signs
- O1 (2) Every word, label and badge reads left to right as the brief spells it, in every view: nothing mirrored. Look: every word on the sheet, full size.
- O2 (2) Layers are right: spray, smoke, drool or a hand goes in front of or behind a sign or prop as it would in the real place; nothing clips behind what it should cover. Look: frames where they overlap.
- O3 (1) Each prop can be named at phone size: shape, colour and one detail (a stripe, a label, creases) say what it is. Look: phone-size frames.
- O4 (1) Everything is its real size against the people and the set (bikes, phones, animals, vehicles). Look: a frame with a person beside it.

## S. Sets
- S1 (2) The eye goes to the action: nothing competes with it and nothing that matters is greyed out, dimmed or lost in the dark. Look: phone-size frames.
- S2 (2) Everything is where it would be in the real place: people on paths, cars in lanes, roads that lead somewhere, nothing floating or inside a wall. Look: the widest frame of each set.
- S3 (1) The place matches its references: layout, how many of each key feature, colours; repeated things (houses, windows) broken up as in the real place, not one flat block. Look: check sheet. Tool: benchmark.py (rule 3).
- S4 (1) No edge of the set shows at any camera move or zoom: the painting fills every corner. Look: the first and last frame of each camera move.

## M. Movement (strips of frames with their times)
- M1 (4) A fix made in one shot is in every shot the thing appears in, and nothing pops in, vanishes or jumps mid-shot unless planned: things enter from outside the frame or through a door. Look: first and last frames of each shot; the where-list. Tool: critique.py where.
- M2 (4) Every move takes a natural time: rises, turns and reactions neither slow nor rushed; vehicles and creatures at the brief's speed (whales speed up into a hit). Look: the times across each strip.
- M3 (2) Parts keep their length and shape through a move: no neck, arm or wing stretching or shrinking, no head snapping to profile. Look: each strip, frame to frame.
- M4 (1) Scrolling or repeating backgrounds move smoothly: no loop jumps back. Look: frames across each scroll.
- Tools already hold (look only if you see it plainly): no pose drops back to rest in the last 0.4 s before a cut (rule 72); nothing flips from in front to behind between frames (rule 57, clipcheck).

## Came from (for Claude; the helper never sees this)
A1: Cry Minister 11, 15. A2: Islamocommunism 1 and the beard (rule 76). A3: Elder Swindon 59, 64; the whales (rule 56). A4: Flying Whales 13.
P1: Islamocommunism 9, 11, 16, 19; Patriots 3 5, 9, 12, 18; Patriots 4 15; Ad-Vanced 47c. P2: Job E's arm-acting notes (about 10, among them Cry Minister 33, Halo 16). P3: Ad-Vanced 16, 17; Terfwarts 15.1, 15.3, 14.6; Patriots 3 1; Patriots 4 19; MidTerminal 34. P4: Job E's likeness, face and beard notes (about 8). P5: Ad-Vanced 14, 18, 37c, 40, 41a; Patriots 3 17, 20. P6: Ad-Vanced 37e, 39b, 42d; MidTerminal 33; Patriots 4 6; Terfwarts 9, 14.14. P7: Ad-Vanced 52a, 54c, 57, 58, 59a; Elder Swindon 6. P8: Ad-Vanced 41b, 42c, 42e; Terfwarts 7; Patriots 3 21. P9: Ad-Vanced 15; Terfwarts 14.2, 14.3; Patriots 4 32; Islamocommunism 10. P10: Ad-Vanced 34, 36b, 37b, 54d. P11: Ad-Vanced 37a, 38; Halo 2, 4. P12: Ad-Vanced 52b; Terfwarts 14.1, 17.2.
C1: Flying Whales 8 (helideck), 15. C2: Elder Swindon 63. C3: Elder Swindon 62. C4: Elder Swindon 64.
O1: Elder Swindon 60; MidTerminal 37. O2: Flying Whales 11; Elder Swindon 59. O3: Elder Swindon 61. O4: Elder Swindon 53.
S1: Elder Swindon 50; Ad-Vanced 22. S2: Elder Swindon 55; Ad-Vanced 23. S3: Elder Swindon 51. S4: Cry Minister 44.
M1: Elder Swindon 59, 62, 64; Cry Minister 47. M2: Islamocommunism 18; Elder Swindon 53; Flying Whales 8; Ad-Vanced 36a. M3: Elder Swindon 63; Patriots 3 11. M4: Cry Minister 48.
