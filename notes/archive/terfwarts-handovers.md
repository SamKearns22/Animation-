
# Handover after planning (3 Nov)
## Where things stand (the ONE handover, 15 lines at most)
- **Rules that bite next:** 41 (every arm ends in a hand), 18 (the Hat's face and GIRLS plaque readable: joke props 40 px+), 10 (Hook Text clear of the Hat's face)
- **Done:** planning. Brief checklist (25 items), 19 references, plan in metres, layout approved (note 1: opens close on Harry + the Hat; note 2: McGonagall places it).
- **Spent against the estimate (rule 55):** estimate about 19% (vs Netanyahu 16%, Patriots 4 15%); target 10%. Usage asked after the cast stage (rule 44).
- **Next:** cast sheet, Opus high effort, new chat. Sam types: "Terfwarts: build the cast sheet".
- **Needs Sam:** the scream and splat sound files (any time before the animatic).
- **Read:** `guides/satire.md` Start step 3 and "The look"; `guides/figure-rig.md`; `guides/preflight.md`; rulebook Building table.
- **Lost / Added:** Lost: hall wide, students. Added: GIRLS plaque, McGonagall.
- **Open rule requests:** none (voices, bleeps, rule 62 written 3 Nov)
- **For Claude:** cast: Harry, Ron (one child body, real heights 1.42/1.47), McGonagall (HBO tartan coat, bun, glasses), Myrtle (see-through blue tint, no glow), the Hat (talking fold face). Faces by costume/hair/glasses, no likeness tool (Sam, 3 Nov). Copy `source/satire_template.py` to `source/terfwarts.py` with a `MAP`; stand-ins in `source/terfwarts_compose.py`, plan in `source/terfwarts_plan.py`.

# Handover after the cast (3 Nov)
## Where things stand (the ONE handover, 15 lines at most)
- **Rules that bite next:** 41 (every arm ends in a hand), 18 (the Hat's face and GIRLS plaque 40 px+), 10 (Hook Text clear of the Hat's face)
- **Done:** cast approved 3 Nov (Sam: Y, annoyance 3, strap removed; sheet (`review/terfwarts-cast.jpg`): four turnarounds at real heights, McGonagall with the Hat, the run, Myrtle blocking, Harry's annoyance 1-6, faces).
- **Spent against the estimate (rule 55):** Sam's usage 58% at the start of the cast stage (target 10% for the film): well over; keep every step lean.
- **Next:** stills per shot, Opus medium, new chat. Sam types: "Terfwarts: make the stills".
- **Needs Sam:** the scream and splat sounds (before the animatic).
- **Read:** `guides/satire.md` Start step 4; rulebook Building table; `terfwarts_cast.py` MAP only.
- **Lost / Added:** Lost: Ron's strap (Sam). Added (cast): Myrtle's blue-and-bronze tie, a stand-in stool.
- **Open rule requests:** none
- **For Claude:** cast in `source/terfwarts_cast.py` (`person(img, cam, x, floor, s, who, yaw, j, extra, lift, head_props)`, `hat(p, cx, by, k, mood)`, `worn_hat(mood)`, Myrtle via `ghost`). Harry's annoyance in shot 1 = sheet face 3: brows='fierce', lid=2, mouth='line'. `source/terfwarts.py` is the template copy: `cast` routes to the cast file; its STORY is still the template's. Harry's eyebrows show under the Hat only with the fringe at 0.46 hh.

