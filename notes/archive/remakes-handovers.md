
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


## Handover: build chat 4 (11 Nov)
- **Rules that bite next:** 89 (pass 2 by a NEW helper), 41 (hands read as hands), 38 (only the views the shots use).
- **Done (11 Nov, build chat 4, Opus high; stopped on cost amber):** every open pass-1 fault on the children and the
  gunman fixed and looked at full size: kids' circle hands sized to their big heads (36, was 26); Link's beads bigger
  with shines, the shrug now shoulders up, elbows in, palms out at the chest; Zelda's veil ends at the neck so the gold
  collar shows, the tabard purple with gold trim, scrolls and crest, "down" tips the head and drops the eyes; Malon's
  bottle up at her chest, over her sleeve; Saria's hand on hip (elbow out) and green shorts; Ruto a broad
  mushroom head-fin growing from her pale skull (no brim line), hip fins rooted on the hips, forearm fins under the
  arm's edge, a vain pose (weight on one leg, chin up, one brow); the gunman side on, rifle at the shoulder, looking
  along it; the hems no longer dip below the ground.
- **Next:** Build, Opus high: critique pass 2 of all nine (`remakes_panels.py OUTDIR`, then `critique.py pack
  remakes_cast SPEC.json`, a NEW helper; say in each kid panel's "is" that circle hands are the house style), fix,
  then the cast sheet (`remakes_cast.py castsheet OUT.jpg`) to Sam; wait for his look.
- **Needs Sam:** nothing until the cast sheet; his recordings any time (01-14, a second of silence after each).
- **Read:** `guides/job-packs.md` Build; this file's references; `notes/ledger/remakes_cast/round-1.txt`; both MAPs.
- **Open rule requests:** none.
- **For Claude:** poses carry `_mood` and `_yaw` (panels and `alone` read them); kids' hands `remakes_cast.hand`
  (`KID_HAND_R`); Malon's bottle uses `wrap`; KG crests ("antlers" to a cold eye) and his side grip mittens: judge at
  pass 2. Packs `source/data/critique/remakes_cast/` (git-ignored: pass 1 is only in the ledger).



## Build chat 5 handover (10 Nov)
- **Rules that bite next:** 89 (pass 3 by a NEW helper), 87 (KG's crests: options sheet sent, Sam picks), 41 (hands).
- **Done (11 Nov, build chat 5, Opus high; stopped on cost amber):** critique pass 2 recorded (52 faults, many real).
  Sam's ask: Link carries the Kokiri Sword (hilt over his left shoulder, carved wooden sheath behind the shield,
  ref 03); the front chest strap now crosses his left shoulder like the back and refs. Fixed from pass 2: KG's bib
  spots (read as breasts) now three pale rings in a row; KG's crests are on an options sheet (1 fan, 2 narrow plume,
  3 layered feathers; 3 is in use, Claude's pick); the Goron's rocks five small lumps (two read as ears), thin drool
  (read as a spoon), small goatee point and no neckline bow (read as a jabot), vacant face (half lids, flat brows,
  slack jaw); Navi's ball bigger, veins on her wings.
- **Next:** Build, Opus high: fix the rest of pass 2 (Link's shrug reads "ta-da", his side view has no ear; Zelda's
  shy face reads startled, her trim pink; Malon's bottle at chest, hair to the waist; Saria's ocarina shows clear of
  her hand; Ruto's head-fin still a mushroom helmet, stalk neck, not vain; gunman's scope to his eye, stock on the
  shoulder, an arm to the trigger hand, mask reads beard side on; KG war pose has no gun, side wings read as
  sleeves, swoop upright, stub side tail, faces alike), then pass 3 (`remakes_panels.py OUTDIR`, spec as in pass 2),
  then the cast sheet to Sam with Sam's crest pick.
- **Needs Sam:** crest pick 1/2/3; recordings any time (01-14, a second of silence after each).
- **Read:** `guides/job-packs.md` Build; this file's references; `notes/ledger/remakes_cast/round-1.txt`; both MAPs.
- **Open rule requests:** none.
- **For Claude:** pass 2 spec: `source/data/critique/remakes_cast/r1-p2.spec.json` (git-ignored; the empty r1-p1 dir
  keeps numbering); false alarms to `critique.py false`: P13 bare arms (refs have short sleeves), KG's empty neck-grip
  talons (the victim is in the shot). Crest look `remakes_creatures.CREST` ('fan', 'plume', 'layered'); drop the two
  unpicked after Sam's answer. Sword: `remakes_cast.kokiri_hilt/kokiri_sheath/link_hilt` (a head prop, so over the cap).


## Build chat 6 handover, full (10 Nov)
- **Rules that bite next:** 87 (options sheets for the faults that survived three passes), 89, 41 (hands).
- **Done (build chat 6, Opus high):** the rest of pass 2 fixed (Link's shrug lower with elbows in, his side-view ear
  over the hair; Zelda's shy face, bold gold trim; Malon's hair to the waist; Saria's ocarina shown clear of her hand;
  Ruto's head a flat-topped fish head with fan ear-fins, a thicker neck, cocked shoulder and one leg out; the gunman's
  smooth mask with a respirator, rifle raised to his eye, near arm on the trigger hand; KG's machine gun in his war
  pose, tapered feathered side wings, a diving swoop, a long pointed side tail, distinct hype/glee/show faces).
  Pass 3 by a new helper: 31 faults (ledger). Cast sheet sent to Sam with crest 3 (layered; he hadn't picked).
- **Three-pass survivors (rule 87, options sheets next):** Link's shrug; Ruto's head reads as a hat; Malon's bottle
  height; the gunman's aim; KG's faces alike; KG's crests (Sam's pick). **New in pass 3:** Link's side view shows no
  shield; Zelda's shy head level; Saria's ocarina reads as a pouch; Ruto's fins float, no weight shift; the gunman's
  eyes show and trousers plain; KG's fold reads as a hug, gesture repeats wide, gun on talons, side bandana over the
  eyes, neck grip covers his face; Navi's wings-down points up; the Goron's cone reads as a hat, smiles, loose sleeves.
- **Sam's look (cast sheet): "It looks excellent."** Fixed his two notes: the gunman glares (brows pulled down hard,
  heavy lids); the Goron's neckline is a deep round scoop clear of his goatee. His yes settles the six three-pass
  survivors (no options sheets); crest 3 stays unless he says otherwise.
- **Next:** Build, Opus high: the clear pass-3 faults (Link's side view shield; Navi's wings-down; KG's side bandana
  on his brow; the gun held in his wings, not on his talons), then the sets (forest, camp, town square), each alone
  and critiqued (rule 89).
- **Needs Sam:** the recording of line 6 ("Oh my god!"), the only
  one missing; bleep "shit" in line 13 or let it be heard (Claude: heard, like "god-damn").
- **Recordings filed** (Sam, 10 Nov): `source/audio/remakes-01..14.m4a` with 13 split into 13 and 13b; no 06 yet;
  no duplicates; lengths and syllables match the script (`voices.py`). Link's takes are quieter (-23 to -26 LUFS).
- **Read:** `guides/job-packs.md` Build; this file's references; `notes/ledger/remakes_cast/round-1.txt`; both MAPs.
- **Open rule requests:** none (pass 3 suggested two checklist lines: "no empty cells", "a line-up against Link").
- **For Claude:** pass 3 spec `source/data/critique/remakes_cast/r1-p3.spec.json`, panels in `panels-p3/` (git-ignored).
  Possible false alarms to weigh before fixing: the swoop "body level" (it tips 58 degrees), Malon "bottle at belt"
  (hand at y 170). Gunman mask `remakes_cast.gun_mask`; KG gun `remakes_creatures.kg_gun/_gun_over`; side wings
  `_kg_wing(taper=True)`; KG glee lower lid `low`.

## Build chat 6 handover (archived 11 Nov by build chat 7)
- **Rules that bite next:** 89 (each set alone and critiqued), 41 (hands), 38 (only the views the shots use).
- **Done (build chat 6, Opus high):** pass 2's faults fixed; critique pass 3 recorded (31 faults, ledger); cast sheet
  sent; **Sam: "It looks excellent"** (settles the three-pass survivors; crest 3 stays); his notes fixed: the gunman
  glares, the Goron's neckline is a round scoop. 13 of 14 recordings filed (13 split into 13 and 13b); dialogue
  changes to lines 1, 7, 13 in the brief and acting list (slam now on "Now").
- **Next:** Build, Opus high: the clear pass-3 faults (Link's side-view shield; Navi's wings-down; KG's side bandana
  on his brow; the gun in his wings, not on his talons), then the sets (forest, camp, town square), each critiqued.
- **Needs Sam:** line 6's recording ("Oh my god!"); "shit" heard or bleeped (Claude: heard).
- **Read:** `guides/job-packs.md` Build; this file's references and shots; `notes/ledger/remakes_cast/round-1.txt`.
- **Open rule requests:** none (pass 3 suggested two checklist lines: "no empty cells", "a line-up against Link").
- **For Claude:** pass 3 in `source/data/critique/remakes_cast/r1-p3` (git-ignored); maybe false alarms: swoop "level",
  Malon "bottle at belt". `remakes_cast.gun_mask`; `remakes_creatures.kg_gun/_gun_over`, `_kg_wing(taper=True)`.
