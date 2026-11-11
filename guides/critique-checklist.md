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
- A1 (8) Everything the brief puts in a panel is named right in the cold look at phone size, and nothing reads as something it isn't (a flat blob, a rude shape, a hug, Stonehenge, an eye). Look: look.md against brief.md.
- A2 (2) Ours matches each reference beside it: how many, colours, positions, which way it faces, proportions, the details that make it that thing. Look: check sheet. Tool: compare.py.
- A3 (3) A fault found on one panel is looked for on every panel of the same kind, not only where it was found or noted (rule 56). Look: every panel.
- A4 (3) The Hook Text box and TikTok's own buttons and captions cover nothing that matters (a face, a hand, the action, a sign). Look: the Hook Text frame. Tool: hookcheck.

## P. People
- P2 (17) Acting reads: each face and body shows the feeling the acting list names on that beat, big enough for a phone, not overdone; eyes and head look at whom or what the beat says. Look: look.md feelings and gazes against the beats in brief.md.
- P7 (11) Weight rests where it should: feet on the ground, seated people on the seat, anyone lying flat with a neck and each arm on its own side; nothing floats, sinks, slides or bobs; legs the same length. Look: feet, seat or body, first and last frame of each shot. Tool: lying.py.
- P1 (10) Every hand that holds or rests on something touches it: no gap, no hover, nothing through the fingers; the prop sits the right way round in the hand. Look: each hand on a prop, full size, every view. Tool: handcheck (held), kitchecks.rests.
- P8 (10) Turned, from behind or mirrored, the body still makes sense: face and body point the same way, hands on the right sides, nothing held in front drawn over the back or wrapped round it. Look: each person in every view the film uses. Tool: views (AVOID lists).
- P3 (8) Arms bend only at the elbow, the right way, by a natural amount; no rubber or broken arm; upper arm and forearm keep their length. Look: arms at both ends of each move.
- P4 (8) Faces match their references: hair, beard (its five lines), glasses, colouring, how open the eyes are. Look: face crop beside each reference. Tool: likeness.py, beard tool.
- P5 (7) Each arm grows out of its shoulder in one flowing line: no gap, step, stray tick, or arm starting inside the chest, from every view. Look: each shoulder, full size, every view. Tool: handcheck (seam).
- P6 (7) Hands read as hands: a point shows one finger out along the forearm (rule 41); no hand lost behind a prop or body where it should show. Look: each hand, full size. Tool: handcheck.
- P10 (6) No body passes through another person, prop or set at a hit, step or touch; contact looks like touch. Look: frames at each contact. Tool: clipcheck.
- P12 (6) Mouths move only on that person's words, close between lines, and there is one mouth, always. Look: frames labelled with who speaks. Tool: the mouth check.
- P11 (5) Each head sits on a neck of believable length and is the right size for the body and for any helmet or hood. Look: head and neck, full size.
- P13 (4) Clothes fit the body: a pattern runs to every edge and onto the sleeves in every view; cuffs join their sleeve; wrists come out of the sleeve end. Look: sleeves and pattern edges, full size, every view.
- P14 (3) Eyes stay whole: the pupil, iris and shine sit inside the eye's outline at every size and glance, on people and creatures alike; nothing spills onto the lid or face. Look: each face crop, full size, at its hardest glance. Tool: eyekit.

## C. Creatures
- C1 (3) What it hits reacts (crumples, breaks, moves) and nothing passes through it or through what it hits. Look: frames at each hit.
- C2 (2) It has the parts its reference has, joined where they belong (a neck between head and body, wings from the shoulders), shaped like the animal, not a blob; open jaws seen side-on show through. Look: one alone at full size beside its reference.
- C3 (1) It reads as that animal at its smallest size and from every angle the film uses (from above, far off): outline and colour say what it is. Look: the smallest it appears, phone size.
- C4 (1) It keeps a believable distance from people unless the brief says otherwise (no pigeon at his face). Look: each shot it is in.

## O. Props, text and signs
- O5 (7) Every prop, piece and mark rests on, hangs from or sticks into something, whole: no bullet hole, scorch, belt, table or body part in mid-air, sunk, piled oddly or chopped off. Look: each prop's contact, full size.
- O2 (6) Layers are right: spray, smoke, debris, drool or a hand goes in front of or behind a person, sign or prop as it would in the real place; nothing clips into what it should cover or sit behind. Look: frames where they overlap.
- O4 (6) Everything is its real size against the people and the set (bikes, phones, tables, flags, animals, vehicles), and people the right size against each other. Look: a frame with a person beside it.
- O3 (5) Each prop can be named at phone size from any angle it is seen at: shape, colour and one detail (a stripe, a label, a string) say what it is; nothing is a flat line. Look: phone-size frames.
- O6 (4) Effects suit the house style and read at phone size: no cartoon stars or white nuclear flash; sparks, smoke and trails big enough to see and shaped like the real thing. Look: frames at each effect.
- O1 (3) Every word, label and badge reads left to right as the brief spells it, in every view: nothing mirrored; flags fly the right way round; no face, prop or glance flipped against its cast-sheet tile (old rule 34). Look: every word and flag on the sheet, full size.

## S. Sets
- S1 (6) The eye goes to the action: nothing competes with it, nothing that matters is dimmed or lost, and what the beat needs (the thing about to blow up, the faces reacting, the eyes) is in shot and big enough. Look: phone-size frames.
- S2 (6) Everything is where it would be in the real place: people on paths, cars in lanes, roads that lead somewhere, chairs at tables, boats at sea, the street up to the feet; nothing inside a wall. Look: the widest frame of each set.
- S5 (3) Every wall and building has the detail its real one has (windows, doors, signs, texture): no blank block, no white void; every set has front, middle and back layers, a textured ground and life (old rule 4). Look: the widest frame of each set.
- S6 (3) A set is the same set in every shot: sizes, walls and where people and furniture stand match from shot to shot. Look: one frame per shot of the set, side by side.
- S3 (1) The place matches its references: layout, how many of each key feature, colours; repeated things (houses, windows) broken up as in the real place, not one flat block. Look: check sheet. Tool: benchmark.py (rule 3).
- S4 (1) No edge of the set shows at any camera move or zoom: the painting fills every corner. Look: the first and last frame of each camera move.

## M. Movement (strips of frames with their times)
- M1 (8) A fix made in one shot is in every shot the thing appears in, and nothing pops in, vanishes or jumps mid-shot unless planned: things enter from outside the frame or through a door. Look: first and last frames of each shot; the where-list. Tool: critique.py where.
- M2 (8) Every move takes a natural time (people react before a hit lands: old rule S1): rises, turns, pauses, cuts and reactions neither slow nor rushed; vehicles and creatures at the brief's speed (whales speed up into a hit). Look: the times across each strip.
- M3 (7) Parts and faces keep their shape through a move and across views: no neck, arm or wing stretching, no squeezed or stretched in-between on a turn (a turn SNAPS to the other view in one frame, rule 72: never flag the snap itself), the same eyes, brows and glasses style, no line flickering, a flight path that doesn't jump at a cut. Look: each strip, frame to frame.
- M5 (5) Every hit shows: the thing hit jolts, dents, sparks or breaks, and the damage stays for the rest of the film. Look: frames just after each hit and the shot's last frame.
- M4 (1) Scrolling or repeating backgrounds move smoothly: no loop jumps back. Look: frames across each scroll.
- Tools already hold (look only if you see it plainly): nothing flips from in front to behind between frames (rule 57, clipcheck). Rule 72's drop back to rest before a cut is checked for standing people (kitchecks.cut_rests, Job L); under M2, look at the last frames only for seated people, creatures, and anything not drawn by views.py.

## Came from (for Claude; the helper never sees this)
Harvest, 10 Nov (Job H chat 2: the notes tables of Ad-Vanced, Cry Minister, Islamocommunism, MidTerminal, Patriots 3 and 4, Terfwarts, Halo, Prepper, Netan-Yahoo; notes found by the checks themselves not counted; P9 merged into P7, rule 3 of the header). Short names: AV Ad-Vanced, CM Cry Minister, IC Islamocommunism, MT MidTerminal, P3/P4 Patriots, TW Terfwarts, PM Prepper, NY Netan-Yahoo.
A1: Cry Minister 11, 15; AV25, P3 1, P3 2, P4 10, NY11, CM29. A2: Islamocommunism 1 and the beard (rule 76). A3: Elder Swindon 59, 64; the whales (rule 56). A4: Flying Whales 13; P3 13, CM43.
P1: Islamocommunism 9, 11, 16, 19; Patriots 3 5, 9, 12, 18; Patriots 4 15; Ad-Vanced 47c. P2: Job E's arm-acting notes (about 10, among them Cry Minister 33, Halo 16); NY9, PM21, PM59, P3 11, AV36c, MT35, MT48. P3: Ad-Vanced 16, 17; Terfwarts 15.1, 15.3, 14.6; Patriots 3 1; Patriots 4 19; MidTerminal 34. P4: Job E's likeness, face and beard notes (about 8). P5: Ad-Vanced 14, 18, 37c, 40, 41a; Patriots 3 17, 20. P6: Ad-Vanced 37e, 39b, 42d; MidTerminal 33; Patriots 4 6; Terfwarts 9, 14.14. P7 (with old P9): Ad-Vanced 52a, 54c, 57, 58, 59a; Elder Swindon 6; Ad-Vanced 15; Terfwarts 14.2, 14.3; Patriots 4 32; Islamocommunism 10. P8: Ad-Vanced 41b, 42c, 42e; Terfwarts 7; Patriots 3 21; PM11, PM12, PM16, PM42, PM45. P10: Ad-Vanced 34, 36b, 37b, 54d; PM47, PM58. P11: Ad-Vanced 37a, 38; Halo 2, 4; AV51. P12: Ad-Vanced 52b; Terfwarts 14.1, 17.2; CM17, CM35, CM45. P13: AV10, AV12, PM26, PM38 (and Job I's open note: the driver's checks on non-front views). P14: rule S5 (Sam, 11 Nov: every cast; the tool job).
C1: Flying Whales 8 (helideck), 15; CM23. C2: Elder Swindon 63; CM1. C3: Elder Swindon 62. C4: Elder Swindon 64.
O1: Elder Swindon 60; MidTerminal 37; IC1. O2: Flying Whales 11; Elder Swindon 59; PM13, AV24, AV42b, PM3. O3: Elder Swindon 61; PM19, PM27, PM31, PM50. O4: Elder Swindon 53; PM15, CM16, CM21, IC3, P4 1. O5: AV42a, PM18, PM22, PM55, NY4, NY11, P4 2. O6: AV29, PM20, PM46, PM53.
S1: Elder Swindon 50; Ad-Vanced 22; PM2, P4 9, AV54a, NY6. S2: Elder Swindon 55; Ad-Vanced 23; P3 6, P4 5, P4 27, CM2. S3: Elder Swindon 51. S4: Cry Minister 44. S5: CM31, MT31, P3 7. S6: P4 18, 25, 26.
M1: Elder Swindon 59, 62, 64; Cry Minister 47; P4 12, PM29, PM34, PM60. M2: Islamocommunism 18; Elder Swindon 53; Flying Whales 8; Ad-Vanced 36a; AV47c, MT36, PM35, PM9. M3: Elder Swindon 63; Patriots 3 11; AV37d, AV42e, P4 16, P4 17, PM57. M4: Cry Minister 48. M5: PM8, PM10, PM17, PM30, AV29.
