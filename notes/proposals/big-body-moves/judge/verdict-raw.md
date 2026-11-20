## Leak
yes: the facts quote lesson 10's remedy ("key poses drawn for each angle of the move, layered by hand, checked on a pose sheet") and Sam's line that a 2D body can do it, and the problem lists the check's contents (limbs joined, human lengths, arms on the correct side, nothing tangled, nothing through solids). V3 follows the leak closely; V1 and V2 weigh it and move past it.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 4 | 3 | 4 | 4 | 4 | 19 |
| V3 | 3 | 3 | 3 | 2 | 3 | 14 |
## Sam test
Q1: Yes once patched: an expert measures the failed frames first, puts the check where no file can skip it (the drawing and the clip writer), and reuses the 3D skeleton the kit already draws in the house style rather than hand-built layer tables per film.
Q2: The evidence is version 4's real frames (8 of 16 notes share cause A) widened by V2's 11 past body-placement notes (critique checklist P7, 9 films). Wide enough for the check; the look of the 3D route is shown to Sam before it is built.
Q3: Root cause found with evidence: the shot was drawn in a practice file that runs no pre-flight, no pose check and no critique (checked: none called), and clips (`--span`) skip the pre-flight lock (checked, film_engine). Enforced at the drawing and the writer, not by a chat choosing to run it; numbers to beat are set.
Q4: Four different approaches weighed (hand-drawn keys per angle, a 3D skeleton route, a send gate, measure first); measure-then-gate-then-route is the strongest.
Q5: The first step changes nothing; each change is its own Y and undoes alone; the 3D look is shown on a sheet before any build. Risk named: the check sits in drawing code every film uses, so it must show 0 false flags on past films first.
Q6: Mostly checked; patched: the film's spend is now 28.82% (both helpers quoted 27.71%), and the 3D body now draws through the flat house pieces (`lying_flat`), nearer pieces over farther, not per-pixel; all costs and render speed marked unchecked.
Q7: Sized to the result (a kit for every film's big moves plus an unskippable check), about 6% of a week once, built only as the replay shows which parts matter. No cheap patch to shot 4 alone.
Q8: Nothing provisional: each change is permanent when made and reviewed at film end.
## Pick
V1
## Why
V1 and V2 share the right shape (measure first, then a 3D skeleton route and a human-body check, each its own Y). V1 wins on the root cause: it puts the check where every person is drawn and makes the clip writer refuse an unnamed fault, so a practice file or a quick clip cannot slip past it. V2's gates live in pre-flight and finishing, and the record shows shot 4 was built in a file that runs neither, and quick clips skip pre-flight's lock: the same bypass would recur. V3 builds a new part-layer drawing in the shared drawing code when `lying_flat` already lays the flat rig's pieces along a 3D skeleton, needs a hand-written layer table for every key of every film, has no learn step, and bundles drawing, check and gallery into one yes.
Taken from V2: the cold critique of version 4 in the learn step; drawing the skeleton with the flat house pieces (`lying_flat`) at full and phone size; the 11 past P7 notes as wider evidence; "0 false flags on the pose gallery"; each change its own Y. Taken from V3: the check's extra tests (each drawn piece joined to its parent, the person's picture one joined shape, knees and elbows within human bend, samples along every bone not only joints); keys posed in the body's own frame (hands placed from the chest); passing poses (car climb, lean-out, aim from a window) added to the pose gallery; passing shot 3 as a no-false-flag test. From the record: the screenplay says Jason "leans out", whole to the hips; versions 3-4 made a bigger sill-sitting climb.
## Faults in the pick
- F1 [fixed] V1 described the 3D body's look as its own fills with per-pixel depth; it now draws through `lying_flat` (house pieces, nearer over farther). The final version says so and shows that look first.
- F2 [fixed] V1's learn step had no cold critique of version 4; added from V2, so the picture-only faults are counted too.
- F3 [fixed] Stale spend figure (27.71%); the ledger now reads 28.82%.
- F4 [fixed] V1 left the three changes' Ys implicit; each is now its own Y.
- F5 [named] The check sits in drawing code every film uses: a slower render or false flags on old films are possible; it must pass the pose gallery, shot 3 and two past films with 0 false flags before it can refuse anything. Its speed is unchecked.
- F6 [named] Whether Sam accepts the flat-pieces-on-a-skeleton look upright, and whether the car gives depth for every piece, is unknown until the look sheet.
- F7 [named] All costs (about 1% + 1.5% + 3-4%) are unchecked estimates.
- F8 [named] The move itself: the screenplay says "leans out" (whole to the hips through the window); the sill-sitting climb is bigger than written. Shot 4's build proposal (rule 8) should put the written move to Sam first.
## Final version
**Learn (changes nothing; about 1% of a week, unchecked; Opus).** Replay version 4 (5edd1c1d) every frame. (a) A fresh helper critiques it cold: how many of the 8 cause-A notes (2, 3, 4, 6, 7, 8, 11, 15) it names. (b) Turn Jason's poses into the 3D skeleton (`lying.from_views`); run `body_faults`, `check_arm3` and the skeleton's collision shapes against the 3D car; count which notes each catches. (c) One sheet for Sam: 6 moments of version 4 beside the same skeleton drawn with the flat house pieces (`lying_flat`), at full and phone size, plus Jason from five views. (d) List what is missing upright.

**Change 1, the human-body check (own Y; about 1.5%).** Recorded where people are drawn (`views.person`, `lying.draw`), so no file bypasses it. Every person, every frame: bones at rig length in 3D (within 6%), elbows and knees in human range, each arm on its own side as drawn, each drawn piece joined to its parent and the person's picture one joined shape, no limb through another, samples along every bone outside every listed solid, a held gun within 10 degrees of its target while firing. The clip and animatic writer (including `--span` clips) refuses a render with an unnamed fault or without a critique record for that render (rule 89). Beat: catches every skeleton-held fault of version 4; 0 false flags on the pose gallery, shot 3 and two past films.

**Change 2, big moves on the 3D skeleton (own Y, only if Sam passes the look sheet; about 3-4%).** Climbs, turns past side-on, leaning out, car doors and falls are posed as 3D key poses in the body's own frame, drawn with the flat house pieces, hidden by the 3D car piece by piece; key poses shown on a five-view pose sheet in the rule 8 build proposal before building; passing poses go into the pose gallery. Pre-flight refuses a big move built on the flat standing figure. Beat: shot 4's next clip has 0 of the 8 cause-A notes; the next film's big move gets 0 repeated body notes.

Total about 6% of a week once (unchecked); later films reuse it. Shot 4's build proposal puts the screenplay's "leans out" move to Sam.
## For Sam
### Option 1: Measure, then a check nothing can skip, then a proper 3D skeleton
First, at no risk, we replay the bad version and measure which of your 8 body notes our existing tools and a fresh critic would have caught, and show you one sheet: the bad frames beside Jason drawn on a 3D skeleton (a hidden stick-figure that knows where each limb is in space) dressed in our usual flat pieces. Then, each on its own yes: a check that looks at every person in every frame as a body (joined arms, right lengths, right sides, nothing through the car, gun aimed right), placed where people are drawn so no shortcut skips it, and nothing reaches you with a fault unnamed; and big moves built on that skeleton. You would notice: no more twisted bodies reaching you, and a look sheet before any rebuild.
Lost: the old flat figure for big moves (kept for normal poses); a quick clip can no longer be sent before the critique runs.
Added: one look sheet for you; a check that can stop a clip; climb, lean and aim poses kept for future films.
### Option 2: The same, with the check at the usual pre-send checks
The same measuring and the same skeleton, but the body check and a "critic must have looked" rule run at the usual pre-send checks and when finishing, not where people are drawn. Simpler to add, but shot 4 was built in a practice file that runs none of those checks, and quick clips skip them, so the same slip could happen again.
Lost: the old flat figure for big moves; sending without a critique when finishing.
Added: one look sheet; the skeleton route; the body check; a critique rule at finishing.
