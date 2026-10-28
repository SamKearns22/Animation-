# Pose gallery (film-quality-rules 42)

A pose is drawn and tested once, from every view, then kept here and in the kit. A film picks from this list; only a
pose that is not here is built new, listed in the film's plan, and added here once it passes.

**See them all:** `python3 source/posegallery.py [OUT.jpg] [--all]` draws each pose on a plain model from the front,
three-quarter, side, three-quarter back and behind, in the house style (circle hands), runs the hand check (rule 41,
`handcheck.py`) on every drawing, and saves one labelled sheet (rule 48). The last sheet is `guides/pose-gallery.jpg`. `--all` adds every other pose in
`moves.pose` (not yet in the table below: test before use). `python3 source/kittests.py gallery` checks that every
pose still passes wherever this table says it does.

**Use one:** `posegallery.pose('salute', sp)` (or the function named below) returns the joints for
`views.person(..., joints)`; each fits anyone's shoulders. Key two poses with `moves.keyed` for movement.

| pose | call | from | passes (rule 41) | avoid | notes |
|---|---|---|---|---|---|
| arms folded | `posegallery.arms_folded(sp)` (`moves.pose(sp, 'arms_folded')`) | the kit | all 5 views | | hands tucked under the arms on purpose (`j['tucked']`, so the hand check allows it) |
| hands up | `posegallery.hands_up(sp)` | new, 28 Oct | all 5 views | | palms up beside the head, wide and a little forward (closer in, the hands hide behind the head side on) |
| pointing | `posegallery.pointing(sp, target)` (`moves.pose(sp, 'point')`) | the kit | all 5 views | | the left hand on the hip; `target` in the torso frame |
| binoculars | `posegallery.binoculars(sp)` | Patriots 3, note 21 | all 5 views | | hands on the barrels' outer sides, elbows out: the hands show past the head from behind (the film's own version hid one) |
| salute | `posegallery.salute(sp, k)` | Patriots 3 | all 5 views | | `k` 0-1 eases it up round the shoulder (never across the man beside him); `steep` for higher |
| hands on a gun | `posegallery.rifle(sp)` | new, 28 Oct | front, three-quarter, side, three-quarter back | behind | port arms, hands over the rifle. From behind both hands are hidden by his back: show him three-quarter back instead. A big 3D gun through the real camera: `held3d.hold` |
| flapping (up) | `posegallery.flapping(sp, 'up')` | Patriots 3, note 18 | all 5 views | | hands high and wide, at the sleeves' ends |
| flapping (pat) | `posegallery.flapping(sp, 'pat')` | Patriots 3, note 18 | all 5 views | | patting the air down |

**Adding a pose:** write it in `source/posegallery.py` (a function of `sp` returning the joints; credit the film), add
it to `GALLERY`, run the sheet, fix it until every view passes or list the views that fail in `AVOID` with the reason,
then add its row here.
