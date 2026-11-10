
# 10 Nov (planning, before the cast build)
## Where things stand (the ONE handover)
- **Rules that bite next:** 89 (each new character drawn alone beside its references, critiqued cold), 38 (front
  on; build only the views the shots use), 41 (every arm ends in a hand: KG's wings act as arms, decide his "hand").
- **Done (10 Nov, planning, Opus high):** brief checklist, estimate 14.5% (Sam: the full version), shots and acting
  list, Sam's answers (Decisions below), all 24 references filed and written up as checklists.
- **Spent against the estimate:** planning about 1% of 14.5%. Week at 43% at the start.
- **Next:** Build, Opus high: the cast, each new character alone beside its references and critiqued
  (`critique.py`), then the cast sheet (front/side/back where shots need them) for Sam's look. Then the
  composition sheet (rule 11) and the 4 rehearsal clips (rule 8).
- **Needs Sam:** nothing until the cast sheet; his recordings any time (01-14, a second of silence after each).
- **Read:** `guides/job-packs.md` Build; this file's estimate, references, acting list and Decisions.
- **Lost / Added:** Lost: Ruto's over-sexual preening (a child: vain and pushy instead; Sam: "100% correct").
  Added: Saria; R1/R2 prompts; gunfire, neck crack and blast sounds.
- **Open rule requests:** none.
- **For Claude:** film `remakes`, `source/remakes.py` from `source/satire_template.py`; refs `references/remakes/`;
  MG42 + belt + flash + cases `patriots3_cast.py`; balaclava `patriots3_cast.balaclava`; fx `prepper_fx.py`;
  body pieces `lying.py`; thrown against a wall `patriots3_act.py`; front run `moves.GAITS['front_run']`.



## Handover, build chat 1 (10 Nov)
- **Rules that bite next:** 89 (each new character alone beside its references, critiqued cold), 41 (every arm ends
  in a hand; KG's wings are arms), 38 (only the views the shots use: Link front, side, back; gunman front, side).
- **Done (10 Nov, build chat 1, Opus high; stopped on cost amber):** `source/remakes_cast.py` started: all five
  children (head, hair, outfit, sleeves, boots, faces), the gunman (Patriot balaclava + helmet, goggles, plate vest),
  milk bottle, ocarina, rifle; `alone WHO OUT.jpg` sheet. Only Link has been looked at.
- **Link's faults from my own look (fix before the critique):** 1 head too small for a 9-year-old, legs too long
  (aim about 4 heads tall: bigger hh or shorter legs); 2 long thin neck, and side on the head floats off the body;
  3 brows hidden under the fringe (draw them over it); 4 cap too small and flat, its tail reads as a leaf (ref 04:
  big floppy cap hanging to his left); 5 faces too alike at phone size (unsure, horror, deadpan need bigger brows and
  mouths); 6 side view shield sticks out like a slab; 7 the sheet's figure tiles are mostly empty (crop tighter).
- **Next:** Build, Opus high: fix Link's 7, check the same faults in Zelda, Malon, Saria, Ruto and the gunman
  (`alone` each), then `remakes_creatures.py` (KG, Navi, Goron), critique each (`critique.py pack`), cast sheet.
- **Needs Sam:** nothing until the cast sheet; his recordings any time (01-14, a second of silence after each).
- **Read:** `guides/job-packs.md` Build; this file's references and Decisions; `source/remakes_cast.py` MAP.
- **Open rule requests:** none.
- **For Claude:** refs `references/remakes/`; MG42 `patriots3_cast.py`; fx `prepper_fx.py`; pieces `lying.py`;
  wall throw `patriots3_act.py`; `moves.GAITS['front_run']`. Kids draw at `height` via `scale_for`.


## Handover, build chat 2 (11 Nov)
- **Rules that bite next:** 89 (each new character alone beside its references, critiqued cold), 41 (every arm ends
  in a hand; KG's wing feathers are his fingers), 38 (only the views the shots use).
- **Done (11 Nov, build chat 2, Opus high; stopped on cost amber):** Link's 7 faults fixed; the same checks on Zelda,
  Malon (hair now behind her body), Saria, Ruto (head fin no longer a hat; a waist) and the gunman (goggles). Sam's
  note "not too chibi": heads a bit smaller, longer jaw, almond eyes with one shine, faint cheeks. NEW
  `source/remakes_creatures.py`: KG (front and side, 8 wing poses, 6 faces, bandana), Navi (glow, wings, heat), the
  Goron (frilly dress, drool); `alone kg|navi|goron OUT.jpg`. First look only, nothing critiqued yet.
- **My first look at the creatures (fix before the critique):** KG 1 crests are thin wavy worms (ref: broad swept
  feather fans curling out); 2 hype/show grins too small; 3 front feet read as blocks; 4 side wings are sticks, grip
  hands stumps; 5 folded wings hang below his body like sausages; 6 the tail reads as a comb between his feet.
  Navi 1 the top wings merge into one heart (ref: a V, apart); 2 lower wings hidden; 3 red ring reads as a donut.
  Goron 1 reads as a bell (ref: big round belly, face lower); 2 drool too faint; 3 the dress is flat stripes (ruffles).
- **Next:** Build, Opus high: fix those, then one critique pack of all nine (`critique.py pack remakes SPEC.json`, a
  new helper), fix, then the cast sheet (all nine at true heights, Link's front for scale) to Sam; wait for his look.
- **Needs Sam:** nothing until the cast sheet; his recordings any time (01-14, a second of silence after each).
- **Read:** `guides/job-packs.md` Build; this file's references and Decisions; both files' MAPs.
- **Open rule requests:** none.
- **For Claude:** refs `references/remakes/`; kids draw at `height` via `scale_for`; creatures in person units
  (`KG_HEIGHT_U`, `GORON_HEIGHT_U`), `kg()` returns wing hands for props; MG42 `patriots3_cast.py`.



## Build chat 3 handover (archived 11 Nov by build chat 4)
- **Rules that bite next:** 89 (pass 2 by a NEW helper after the fixes), 41 (every arm ends in a hand: the kids' hands
  are dots), 38 (only the views the shots use).
- **Done (11 Nov, build chat 3, Opus high; stopped on cost amber):** all 12 creature faults fixed (KG: feather-fan
  crests, big grins, toes and talons, wings with hanging feathers, folded wings on his sides, a barred fanned tail;
  Navi: V wings apart, lower pair showing, a soft white-hot ball; Goron: a pear with a round belly, thick drool,
  gathered ruffles). Critique pass 1 of all nine (`r1-p1`), then the creature faults it found fixed (one teacher
  wing, bigger beak and spit, tails fanned with pale tips, Navi's flutter tiles differ, boulders on the Goron's back,
  arms clear of his body, a tuft goatee). NEW `cast_sheet` (all nine at true heights, ruler).
- **Pass 1 faults still open (the children, from build chat 1-2):** every kid and the gunman: dot hands (P6, rule 41).
  Link: cap's bead band not showing; the shrug reads as a smiling T-pose. Zelda: collar grey (ref gold), tabard reads
  gold (ref purple); "down" face doesn't look down. Malon: bottle at her waist, not held up. Saria: no hand on hip, no
  shorts showing. Ruto: head-fin reads as a helmet, no hip fins, arm fins float off the arms, stiff not vain. Gunman:
  rifle low, eyes at us (beat: into the trees). Cast sheet: Zelda's and Malon's hem points dip below the ground.
  KG: crests still read "antlers" to a cold eye (the ref's are horn-like: judge at pass 2); side grip hands mittens.
- **Next:** Build, Opus high: fix those, pass 2 (`critique.py pack remakes_cast SPEC.json`, a NEW helper; panels from
  `source/remakes_cast.py` alone sheets, no names), fix, then the cast sheet (`remakes_cast.py castsheet OUT.jpg`) to
  Sam; wait for his look.
- **Needs Sam:** nothing until the cast sheet; his recordings any time (01-14, a second of silence after each).
- **Read:** `guides/job-packs.md` Build; this file's references; `r1-p1/result.md`; both files' MAPs.
- **Open rule requests:** none (the helper suggested "tiles must differ" and "named backgrounds drawn": not Sam's).
- **For Claude:** packs `source/data/critique/remakes_cast/` (film name `remakes_cast`); panels `remakes_panels.py OUTDIR`
  (then a spec: crop = the whole image, so each is a detail); KG
  `tail=` shortens his tail for standing; creatures in person units; MG42 `patriots3_cast.py`.

