# Pose gallery (film-quality-rules 41)

A pose is drawn and tested once, from every view, then kept here and in the kit. A film picks from this list; only a
pose that is not here is built new, listed in the film's plan, and added here once it passes.

**See them all:** `python3 source/posegallery.py [OUT.jpg] [--all]` draws each pose on a plain model from the front,
three-quarter, side, three-quarter back, behind and mirrored (three-quarter facing left), each picture cropped round
the whole body, in the house style (circle hands), runs the hand check (rule 41, `handcheck.py`) on every drawing,
and saves one labelled sheet (rule 48). Since Job G (9 Nov) the hand check also stops: a hand drawn over his body
when it is behind it; a hand inside the body; a hand off its arm (a gap all round); a point that doesn't read (the
forearm aims at or away from the lens), a bent pointing arm (`views.aim` straightens it) or a hidden finger; a hand
hovering over, sinking into or off the edge of what it rests on, or off its grip (`grips.py`); and the pose
flipping sides as he turns through front on or behind (fixed in `views.py`: never mirrored there). Since Job G chat 2 (10 Nov) it
also stops a seam where the arm meets the body (rule 41: a line or gap across the shoulder; behind the body, a gap).
**Props in hands:** `grips.held(j, side, sp, draw)` puts any held prop in the right drawing order for every view
(behind his back or head when it is; the hand over it); `grips.Table` and `grips.on_table` draw a table and rest
hands on it from the same numbers; `grips.Carry` checks a prop handed over never jumps. The last sheet is `guides/pose-gallery.jpg`. `--all` adds every other pose in
`moves.pose` (not yet in the table below: test before use). `python3 source/kittests.py gallery` checks that every
pose still passes wherever this table says it does.

**Use one:** `posegallery.pose('salute', sp)` (or the function named below) returns the joints for
`views.person(..., joints)`; each fits anyone's shoulders. Key two poses with `moves.keyed` for movement.

| pose | call | from | passes (rule 41) | avoid | notes |
|---|---|---|---|---|---|
| arms folded | `posegallery.arms_folded(sp)` (`moves.pose(sp, 'arms_folded')`) | the kit | all 6 views | | hands tucked under the arms on purpose (`j['tucked']`, so the hand check allows it) |
| hands up | `posegallery.hands_up(sp)` | new, 28 Oct | all 6 views | | palms up beside the head, wide and a little forward (closer in, the hands hide behind the head side on) |
| pointing | `posegallery.pointing(sp, target)` (`moves.pose(sp, 'point')`) | the kit | front, three-quarter, side, behind, mirrored | three-quarter back (points away) | the left hand on the hip; `target` in the torso frame |
| binoculars | `posegallery.binoculars(sp)` | Patriots 3, note 21 | all 6 views | | hands on the barrels' outer sides, elbows out: the hands show past the head from behind (the film's own version hid one) |
| salute | `posegallery.salute(sp, k)` | Patriots 3 | all 6 views | | `k` 0-1 eases it up round the shoulder (never across the man beside him); `steep` for higher |
| hands on a gun | `posegallery.rifle(sp)` | new, 28 Oct | front, three-quarter, side, three-quarter back | behind | port arms, hands over the rifle. From behind both hands are hidden by his back: show him three-quarter back instead. A big 3D gun through the real camera: `held3d.hold` |
| flapping (up) | `posegallery.flapping(sp, 'up')` | Patriots 3, note 18 | all 6 views | | hands high and wide, at the sleeves' ends |
| flapping (pat) | `posegallery.flapping(sp, 'pat')` | Patriots 3, note 18 | all 6 views | | patting the air down |
| palms together | `posegallery.palms_together(sp)` | Patriots 4, 1 Nov | all 6 views | | hands pressed together at the chest (moved, grateful) |
| hands on table | `posegallery.hands_on_table(sp, h)` | Patriots 4, 1 Nov | front, three-quarter, side | three-quarter back, behind | both palms on a table edge `h` metres high in front; from behind the table is beyond him, so the hands are hidden |
| pointing both ways | `posegallery.point_both(sp)` | Patriots 4, 1 Nov | front, side, behind | three-quarter, three-quarter back, mirrored | both arms flung out straight (`views.aim`), one finger at each of two people; side on, one arm points away and the point doesn't read |
| hands on a table (drawn) | `posegallery.hands_on_table_drawn(sp, h)` | Job G, 9 Nov | front, three-quarter, side, mirrored | three-quarter back, behind | `grips.Table` drawn with him; prefer it to "hands on table" |
| phone, reading | `moves.pose(sp, 'phone_read')` | kit, fixed Job G | front, three-quarter, side, mirrored | three-quarter back, behind | phone held up to read, the hand over its bottom; from behind his back hides it (it was drawn over his back at its edge until Job G chat 3), so the pose doesn't read there |
| cup in hand | `moves.pose(sp, 'mug')` | kit, fixed Job G | front, three-quarter, side, three-quarter back, mirrored | behind | takeaway cup at the hip |
| cup, sipping | `moves.pose(sp, 'mug_sip')` | kit, fixed Job G | all 6 views | | cup at the lips; from behind it is hidden by his head |
| phone at the ear | `moves.pose(sp, 'phone_ear')` (`moves.phone_at_ear(j, sp, side)`) | kit, redone Job G chat 3 | all 6 views | | the left hand: hand at the cheek, the phone flat along the side of the head from the ear down, elbow forward and out. Side on or three-quarter back facing left, use `side='R'` (the phone must be at the ear nearer us there: at the far ear the head hides the hand) |
| hands on hips | `moves.pose(sp, 'hips')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | front, three-quarter, side, behind, mirrored | three-quarter back | the far hand is behind his body |
| hands in pockets | `moves.pose(sp, 'pockets')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | all 6 views |  |  |
| hands behind the back | `moves.pose(sp, 'behind_back')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | all 6 views |  |  |
| leaning on something | `moves.pose(sp, 'lean_on')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | all 6 views |  |  |
| slumped | `moves.pose(sp, 'slumped')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | front, three-quarter, side, three-quarter back, mirrored | behind | the far hand hangs in front, hidden by his back |
| palm open | `moves.pose(sp, 'palm_open')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | front, three-quarter, side, three-quarter back, mirrored | behind | the palm is in front of him, hidden by his back |
| shrug | `moves.pose(sp, 'shrug')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | all 6 views |  |  |
| facepalm | `moves.pose(sp, 'facepalm')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | front, three-quarter, side, mirrored | three-quarter back, behind | the hand is on his face, hidden by his head |
| microphone | `moves.pose(sp, 'mic')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | all 6 views |  |  |
| pen in hand | `moves.pose(sp, 'pen')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | front, three-quarter, side, three-quarter back, mirrored | behind | the pen hand is hidden by his back |
| bag in hand | `moves.pose(sp, 'bag')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | front, three-quarter, side, mirrored | three-quarter back, behind | the bag hand is beyond his body |
| fists up (guard) | `moves.pose(sp, 'guard')` | kit, tested Job G chat 4 (by the check only; not yet looked at by eye) | all 6 views |  |  |

**Seated poses (the sitting kit, `source/sitting.py`; plan and notes `notes/archive/sitting-kit.md`).** Sheet: `python3 source/sitting.py sheet OUT.jpg`; photos beside them: `sitting.py refs OUT.jpg`; checks: `sitting.py audit`.

| pose | call | from | passes (rule 41) | avoid | notes |
|---|---|---|---|---|---|
| upright | `sitting.pose(sp, 'upright')` | the kit, 8 Nov | front, three-quarter, side, three-quarter back | behind | hands on the thighs; knees and lap show front on (rule 80) |
| hands folded | `sitting.pose(sp, 'hands folded')` | the kit (Vance, line 1) | front, side, three-quarter back | three-quarter, behind | forearms on the desk, elbows bent, hands meeting (rule 78) |
| lean in | `sitting.pose(sp, 'lean in')` | the kit | front, side, three-quarter back, behind | three-quarter | elbows on the desk, hands together before the chin |
| lean back | `sitting.pose(sp, 'lean back')` | the kit | all 5 views | | chair reclines with him; hands cup the back of the head, fingers showing at its sides |
| lean back, belly | `sitting.pose(sp, 'lean back, belly')` | the kit | front, side, three-quarter back | three-quarter, behind | fingers laced on the stomach |
| armchair | `sitting.pose(sp, 'armchair')` | the kit | front, three-quarter, side, three-quarter back | behind | low and deep, sunk in, leaning back, forearms along the arms |
| stool | `sitting.pose(sp, 'stool')` | the kit | front, three-quarter, side, three-quarter back | behind | no back to lean on |
| cross, knee over knee | `sitting.pose(sp, 'cross, knee over knee')` | the kit, part 2 | all 5 views | | prim, closed: the top calf over the lower knee, foot off the floor; hands side by side on the knee |
| cross, ankle on knee | `sitting.pose(sp, 'cross, ankle on knee')` | the kit, part 2 | all 5 views | | the figure four: cocky, at ease; top knee out wide |
| feet up | `sitting.pose(sp, 'feet up')` | the kit, part 2 | all 5 views | | heels on the desk, ankles crossed, hands behind the head; soles to us front on |
| perch, chair edge | `sitting.pose(sp, 'perch, chair edge')` | the kit, part 2 | all 5 views | | eager, about to go: front third of the seat, hands on the knees |
| perch, desk corner | `sitting.pose(sp, 'perch, desk corner')` | the kit, part 2 | front, side, three-quarter back, behind | three-quarter | one thigh along the desk, the other leg standing |
| slump | `sitting.pose(sp, 'slump')` | the kit, part 2 | all 5 views | | defeated: slid down, head forward, legs out and splayed |

**Lying poses (the lying kit, `source/lying.py`: one 3D body).** Call: `lying.lie(sp, 'face_down', x, z, yaw)` (yaw
turns the head's way; `flip=-1` lies the other way round), then `lying.draw`. Tested from 12 views: eye level, 30 and
60 degrees down, each with the head to the right, away, to the left and towards us, three people, both ways round
(`python3 source/lying.py check`). Since Job G chat 4 (10 Nov) the check also stops Sam's lying notes: no neck
showing (Ad-Vanced 57); an elbow or hand held up in the air with nothing under it (Elder Swindon 6: a limp arm
lies flat); and an arm crossing to the other shoulder's side, so both arms read as one side (Ad-Vanced 57-58).

| pose | call | from | passes | avoid | notes |
|---|---|---|---|---|---|
| face down | `lying.lie(sp, 'face_down', x, z, yaw)` | Poker Mon, fixed Job G chat 4 | all 12 views | | cheek on the floor, one arm flung past the head, one by the hip, elbows out flat along the floor (they bent up into the air until 10 Nov) |
| on the back | `lying.lie(sp, 'back', x, z, yaw)` | the kit, fixed Job G chat 4 | all 12 views | | arms flung out, elbows flat on the floor; one knee up |
| on the side, curled | `lying.lie(sp, 'side', x, z, yaw)` | the kit, fixed Job G chat 4 | all 12 views | | knees up, the lower arm under the head, the upper arm limp in front with its hand by the face |
| slumped against a wall | `lying.lie(sp, 'slump', x, z, yaw)` | the kit | all 12 views | | sat on the floor, back on the wall, head dropped |
| curled in a ball, guarding the head | `lying.lie(sp, 'ball', x, z, yaw)` | Ad-Vanced Notice, note 58 | all 12 views | | a hand each side of the head (the upper arm over it, held up on purpose), knees to the chest |

**Pre-flight checks the poses (Job G, 10 Nov; `source/posecheck.py`):** every pose a film takes by name
(`posegallery.pose`, `moves.pose`, `sitting.pose`, `lying.lie`) is followed to the frames it is drawn on. A pose seen
from a view its row lists under "avoid", or one with no row in these tables, stops pre-flight ("POSE: ..."), and every
lying body drawn gets the lying checks above. A pose a film builds by hand (its own joints) is not seen there: list it
in the plan as new, and price building and testing it in the film's estimate (rule 86) at planning.

**Adding a pose:** write it in `source/posegallery.py` (a function of `sp` returning the joints; credit the film), add
it to `GALLERY`, run the sheet, fix it until every view passes or list the views that fail in `AVOID` with the reason,
then add its row here.
