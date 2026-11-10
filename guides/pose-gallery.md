# Pose gallery (film-quality-rules 42)

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
also stops a seam where the arm meets the body (rule 81: a line or gap across the shoulder; behind the body, a gap).
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
| phone, reading | `moves.pose(sp, 'phone_read')` | kit, fixed Job G | all 6 views | | phone held up to read, the hand over its bottom |
| cup in hand | `moves.pose(sp, 'mug')` | kit, fixed Job G | front, three-quarter, side, three-quarter back, mirrored | behind | takeaway cup at the hip |
| cup, sipping | `moves.pose(sp, 'mug_sip')` | kit, fixed Job G | all 6 views | | cup at the lips; from behind it is hidden by his head |

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

**Adding a pose:** write it in `source/posegallery.py` (a function of `sp` returning the joints; credit the film), add
it to `GALLERY`, run the sheet, fix it until every view passes or list the views that fail in `AVOID` with the reason,
then add its row here.
