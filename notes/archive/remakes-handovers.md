
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


## Build chat 7 handover (archived by build chat 8)
- **Rules that bite next:** 89 (each set critiqued by a NEW helper), 83 (two camp overlaps to settle), 3 (benchmark).
- **Done (build chat 7, Opus high):** the four pass-3 cast faults fixed and checked at full size (Link's side shield
  now a broad slab; Navi's wing beat sweeps to level; KG's side bandana wraps his brow; the gun up at his chest,
  belt to his side). First draft of all three sets, one painting per camera: forest (up, down, close, edge), the
  camp (gate opens 0-1), town (square, wall), the cast at their marks; BENCHMARK filled. Stopped on cost amber.
- **Next:** Build, Opus high: fix the faults seen on the first look (below), then each set alone beside its
  references, critiqued by a NEW helper (`critique.py pack`, parts S, O), fix, pass 2; file passes in the catalogue.
  Seen: forest up's foot is a flat sage block; forest close's moss blobs read as leaves stuck on; the camp's gate is
  hidden behind KG and the gunmen (move the gunmen aside), tower and shack crowd the right; the Goron too big in the
  line-up (check his scale); setcheck: blue container x crates, orange container x gate.
- **Needs Sam:** "shit" heard or bleeped (Claude: heard). All 14 recordings are in (line 6 filed by another chat).
- **Read:** `guides/job-packs.md` Build; this file's references; `guides/critique-checklist.md` S and O.
- **Open rule requests:** none.
- **For Claude:** `source/remakes_sets.py` (MAP at the top): `alone forest|camp|town OUT`, `one VIEW OUT`; `STAGE`
  marks, `s_for(ppm)`; `with_cast` places KG's feet at y - 240 s (check on the branch).



## Handover to build chat 9 (archived 11 Nov)
- **Rules that bite next:** 89 (pass 3, a NEW helper per set), 83 (setcheck after each move), 3 (benchmark: the shack is out).
- **Done (build chat 8, Opus high):** first-look faults fixed (forest foot, stump moss, camp gate clear, Goron x 0.82
  so about 1.3 x Link, the town camera raised); critique passes 1 and 2 of all three sets, each by NEW helpers; the
  pass-1 faults fixed (list in the commits). Pass 2 still found real faults, so no set is filed in the catalogue yet.
- **Next (Opus, high):** the soft foot shadows (Sam Q3), fix the pass-2 faults below, then pass 3 (`critique.py pack` on
  `spec_r1/2/3.json`, a NEW helper each); a fault surviving three goes to an options sheet (rule 87).
  The faults: "Open notes: the sets' pass-2 faults" below.
- **Sam, 11 Nov (Y Y Y):** 1 carry on with the full version past 15%; 2 KG's ear tufts stay as they are (they match
  refs 01, 02: mark A1 "horns" a false alarm); 3 add a soft shadow under every character's feet (all sets, all shots).
- **Read:** `guides/job-packs.md` Build; `guides/critique-checklist.md` S and O.
- **Open rule requests:** none.
- **For Claude:** `source/remakes_sets.py` (MAP): KG_BEAT poses KG per sheet, gunmen aim (flipped right of centre),
  TOWER, CONTAINERS; packs `source/data/critique/remakes_sets/r1..3-p2/result.md` (git-ignored); ledger remakes_sets.


# 11 Nov (build chat 9, before build chat 10)
## Where things stand (the ONE handover)
- **Rules that bite next:** 89 (pass 3, a NEW helper per set), 83 (setcheck after each move), 87 (a fault surviving 3 passes goes to an options sheet).
- **Done (build chat 9, Opus high; stopped on the amber cost watch):** soft foot shadows under every character (Sam Q3;
  Navi has none: she is a flying light); the forest's and the camp's pass-2 faults fixed (list below, in the commit);
  the set sheet now shows the camp with the gate blown in. setcheck clean.
- **Next (Opus, high):** the town's pass-2 faults (below), then critique pass 3 of all three sets, a NEW helper each
  (rule 89, parts S and O). The spec files are git-ignored and gone with the old container: write
  `source/data/critique/spec_r1/2/3.json` again (one panel per set: the `alone` sheet as `img`, refs 01/17/19/20,
  23/24, 21/22, parts "SO"), then `critique.py pack` each.
- **Read:** `guides/job-packs.md` Build; `guides/critique-checklist.md` S and O.
- **Open rule requests:** none.
- **For Claude:** `source/remakes_sets.py` (MAP): `foot_shadow`, SHADOW_W, ON_HIGH; `kg_on_branch` (tail behind the
  branch); STUMP_DOWN/STUMP_SEED (one stump for S2, S4/S6); `_near_yard`, `_tower_box` (lookout in the tower),
  `_camo_net`, `_tyres`, BARRELS, WALL_TINS; view `camp_open` (gate=1). Watch in pass 3: the ammo belt in the near
  yard, the stump's plank-like roots, the S1 trunk's moss.


## Where things stand (build chat 11, archived 10 Nov)
- **Rules that bite next:** 85 (cost watch: Sam, 10 Nov: the week is at 69%, over budget since 58%; get to the
  animatic ASAP, no more critique passes or options), 87 (Sam's picks from the options sheet), 83 (setcheck).
- **Done (build chat 11, Opus high):** note 29: KG's beak is his mouth (hinged lower half, opens per syllable from the
  recording; every mood front and side; clip sent in chat (`python3 source/remakes_creatures.py talk OUT.mp4`); Lost: the wide smiling mouth and
  tongue). KG stands on the ground in camp and town (no float). All pass-3 Fix items fixed (list in the commit).
  Options sheet for the six survivors sent in chat (`python3 source/remakes_sets.py options OUT.jpg`) (A = my pick). setcheck clean.
- **Next (Opus, medium): the animatic before the week hits 100% (Sam, 10 Nov: at 75%).** Picks are set (all A;
  Sam may swap a letter: one line in OPT/SPIT). Build the shots from "Shots and the acting list" with the simplest
  staging that tells each beat (holds and cuts over full moves; no rehearsal clips, no critique passes: name
  faults, pre-flight `--faults-named`); check sheet, Sam's yes, one animatic. Watch the cost after every step;
  hand over on amber.
- **Needs Sam:** nothing (letters optional).
- **Named, not fixed:** in S8-S9 the near gunman's rifle passes in front of the far one (layered right).
- **Open rule requests:** none.
- **For Claude:** CR.kg(talk=0-1, stand=True); CR.beak_open/BEAK; CR.talkclip; RS.OPT/SURVIVORS/options();
  _flag_rows, _lantern, _gate_fallen/_gate_debris, _lean_to, _statue_robed/_statue_bird, EDGE_OPTS.


## Where things stand (shots chat, archived 10 Nov)
- **Rules that bite next:** 85 (cost watch: the week near 76%; no extra rounds), 59 (render lock: run pre-flight,
  then render with `--faults-named`), 75 (Hook Text checked by finish.py).
- **Done (shots chat, Opus):** the film file built, all 14 lines, 14 shots (S12 split in two, under 8 s), about 44 s
  plus sign-off; simplest staging (holds, cuts, one move per beat); voices with both f-words bleeped; MG42, neck crack
  and Navi's blast. Brief checklist ticked. Check sheet sent to Sam (Hook Text moved below KG's face).
- **Next (Opus, medium): Sam's notes on the animatic** (sent 10 Nov, 3.3 MB; render 1 min 37 s + finish 38 s); clips for
  movement notes, one full animatic after; no final until Sam's clear yes.
- **Needs Sam:** his notes on the animatic.
- **Named, not fixed (all told to Sam):** pre-flight's 16: the syllable counter misreads "R1", "9", "Ok?" and capitals
  (5); a 30-degree prop-turn test on Malon and Saria, who never turn (8); no scene(t) for the pop-in test (1); "I
  don't think I can do this." 1.5 s on screen (1); no critique round (Sam: none) (1). Staging: Link slides in with a
  bob, hands at his ears (not a crouched run); no hands to cheeks in S6; KG rises behind the gunman (no swoop); KG's
  wings cross Link's chest at the wall; near gunman's rifle over the far one (S7-S8).
- **Read:** pack "Checks and animatic" in `guides/job-packs.md`.
- **Open rule requests:** none.
- **For Claude:** source/remakes.py (MAP at top); timing from _L gaps; SNAP/GATE/BOOM/SLAM beats; LIFT wing pose;
  bleeps in recording seconds in _L.


### Archived 10 Nov (before the notes round, part 1)
- **Rules that bite next:** 30 (note 1 is a repeat-kind fault: find why the cap broke before changing it), 8
  (rehearsal clips of the 4 risky moves before the full animatic), 85 (week at 71%; estimate below).
- **Done:** animatic 1 sent 10 Nov (3.3 MB). Sam's notes on it are below in "Open notes: animatic 1".
- **Next (Opus, medium): all of "Open notes: animatic 1"**, in its order. Clips (`final OUT --small --span T0 T1`) of
  each moved beat, sent as made (no yes needed); one critique round of the changed shots; check sheet; Sam's yes;
  animatic 2. Then the final only on Sam's clear yes.
- **Needs Sam:** nothing until the check sheet.
- **Estimate (Sam asked, 10 Nov):** about 6% of a week to finished (range 5-7%): this round 3-3.5, check sheet and
  animatic 2 0.5, one more round of Sam's notes 1.5, final and posting 0.5. Hand over on amber.
- **Read:** pack "Notes round" in `guides/job-packs.md`; source/remakes.py MAP.
- **Open rule requests:** none.
- **For Claude:** source/remakes.py (MAP); camp marks in RS.STAGE['camp']; KG side view CR.kg(view='side'); the cap
  in the S1/S3 foreground is RS forest_front 'up' with OPT['up']='cap' (RS._link_cap).



### Handover replaced 10 Nov (notes round part 2)
- **Rules that bite next:** 8 (clips of the snap and the wall lift before animatic 2), 89 (one critique round of
  every changed shot before the check sheet), 85 (this chat handed over on amber).
- **Done (10 Nov, notes round part 1):** notes 30, 31, 32, 37, 37b fixed (table below). Clip of the camp and a
  picture of 30 and 31 sent to Sam. Not rendered since: no full animatic.
- **Next (Fable, medium; Sam asked for Fable, 10 Nov): notes 33-36, 37c, 38, 39, 40** in order, a clip of each moved
  beat sent as made; one critique round of all changed shots (camp included); check sheet; Sam's yes; animatic 2.
  Type: "Remakes: read notes/remakes.md Where things stand and Open notes: animatic 1. Do the notes not marked DONE."
- **Needs Sam:** nothing until the check sheet (any reaction to the camp clip or the "Ok?" face is a note).
- **Read:** pack "Notes round" in `guides/job-packs.md`; source/remakes.py MAP.
- **Open rule requests:** none.
- **For Claude:** camp: _kg_camp / _link_camp / _scuttle_pose / _kg_draw, times KG_T BURST1/2 G3_IN G2_IN, marks
  RS.STAGE['camp'] + RS.CAMP_MARKS, S7 cam B.Cam(1.4, 565, 790). The corner Link: RS._link_cap (the cast's back view).
  'sceptical' in RC.MOODS (each=, lows=, turn=). For 34: KG is drawn BEHIND the gunman in s5_edge, so the grip
  hands must be drawn again over him; the gunman's neck base is (gx, gy - 928 * k). For 35: SIDE_WINGS['swoop'].



### Animatic 1 notes finished 10 Nov (moved from notes/remakes.md)
| # | note | plan | result |
|---|---|---|---|
| 30 (Sam 1) | Link's image bottom left in S1 and S3 is completely fractured | the foreground cap (RS._link_cap): find why it breaks up (rule 30), redraw it whole and readable as the back of Link's capped head | **DONE 10 Nov:** new kind; why it broke (rule 30): the corner head was a separate hand-drawn set piece (a cap dome, 12 loose outlined hair spikes, an ear not joined to anything), not Link. Now the cast's own Link from behind (head, ears, cap tail, shoulders, sword hilt). Critique line: A2 (reads at phone size) |
| 31 (Sam 2) | Link's face at "Ok?" far more sceptical and concerned | a stronger 'sceptical' for S4: one brow high, the other low and pinched, eyes side-on to KG, mouth pulled to one side; face sheet first | **DONE 10 Nov:** Sam's steer mid-round: "a look that conveys: uuuuuh, okay?" (bemused and uneasy, not hostile). One brow hiked high, the other tilted up at its inner end, eyes wide and slid sideways, head a little off, an awkward hitched half-smile |
| 32 (Sam 3) | camp staging wrong: the men are behind KG | KG storms in through the gate; he shoots the tower lookout on his way in, turning towards him; victim 2 comes in from camera lower left; the grenade victim from camera middle right; no gunman behind KG; Link follows him in through the gate, aghast (crouched, front-on scuttle). Lost: the three gunmen standing in the yard behind him | **DONE 10 Nov:** KG stamps in through the gate, stops and leans back to shoot the tower lookout, storms on to his mark, turns the gun on a man who runs in lower left; Link runs in through the gate behind him; the last man runs in middle right, level with KG, and is Navi's. Camera moved in on the action (the cast were small over an empty yard). Two gun bursts, not one. Lost: the three gunmen standing behind him; the wide view of the whole yard |
| 33 (Sam 4) | at the wall: KG lifts his face so his expression and beak are seen; Link side on | KG's head raised (face and beak clear, talking and spit visible); Link drawn side on (yaw 90) facing KG, lifted, back near the wall; no bandana in S12, S12b, S13 (bandana only in the camp). Lost: the bandana at the wall || **DONE 10 Nov:** KG's head tips up at Link (his eye, brow and open beak clear, spit flying; a new glaring face, since the old narrowed eye read sleepy once tilted); Link side on facing him, hands on the wings, feet kicking; no bandana; the pair moved right so Link is off the frame edge, and the two closer shots reframed on the faces. Lost: the bandana at the wall; Link's front-on crying face in the last shot (he is in profile now) |
| 34 (Sam 6) | the execution wings don't make accurate contact with the neck | KG's wing tips land on the gunman's neck and jaw (both sides) before the twist; check by the hand points against the neck || **DONE 10 Nov:** why it missed (rule 30): the wings were aimed at the top of his helmet, and were drawn behind him. Now one wing hand closes on the back of his neck and one under his jaw, drawn over him, held from "MOVE", wrenched across on the snap, then flung open. Checked by the hand points (s5_contact) |
| 35 (Claude 2) | KG swoops in behind the gunman (not a rise) | a short swoop down from top right into place behind him || **DONE 10 Nov:** he dives in side on from top right, wings swept back, and lands behind the gunman facing us |
| 36 (Claude 2) | Link's hands to his cheeks on "Oh my god!" | S6 arms up, palms to cheeks || **DONE 10 Nov:** both palms fly up onto his cheeks as he says it |
| 37 (Claude 2) | the near gunman's rifle over the far one | goes with note 32's restage | **DONE 10 Nov:** no rifles overlap now (32) |
| 37b (Claude 2) | Link scuttles in crouched, front-on, running (not a slide with a bob) | a crouched front-on run cycle (`GAITS['front_run']`, low) through the gate behind KG (with note 32) | **DONE 10 Nov:** crouched front-on run cycle, hands over his ears, aghast, through the gate behind KG |
| 37c (Claude 2) | at the wall KG's wings grip Link's collar, not cross his chest | wing tips closed on the collar at his neck, both sides; check by the hand points against the collar (with note 33) || **DONE 10 Nov:** both wing hands closed on his collar under his chin; checked by the hand points (wall_contact) |
| 38 (Claude 4) | "I don't think I can do this." on screen 1.5 s | split into two readable pieces or hold longer || **DONE 10 Nov:** held longer: 1.9 s on screen. Added: 0.45 s of pause before "R2 FOR GRENADES" (film now 44.5 s) |
| 39 (Claude 6) | the line-up reacts more on "ROMANCE" | Zelda shrinks, Malon steps forward with the bottle, Ruto preens, the Goron drools more, Saria winks || **DONE 10 Nov:** Zelda hunches and edges back, Malon hops forward and thrusts the bottle up, Ruto lifts a hand to her head-fin with her chin up, the Goron's drool doubles, Saria winks. KG's presenting wing kept lower so it clears Malon |

## Handover replaced 11 Nov (Fable r3 fixes, part 1)
## Where things stand (the ONE handover)
- **Rules that bite next:** 30 (Fable's "Sam N" findings: check against that note before changing; note 65's lesson),
  87 (a fix that fails twice goes to an options sheet), 89.
- **Done (11 Nov):** notes 46-49, 53, 54, 56, 60-65 fixed, clips sent; critique r3 two passes; note 59's Fable cold
  critique: 48 findings, ranked, in `notes/ledger/remakes-fable-r3.md` (Sam has seen 36 of them). Sam: Y, fix them first.
- **Next (Opus, medium): fix Fable's 48 findings, worst first** (a taste call or anything removing what Sam has seen:
  ask first, numbered, pick first); clips of moved beats; then open the Sonnet chat (medium): check sheet (show the
  subtitles, Hook Text, sign-off and sound Fable could not judge), Sam's yes, animatic 3. Note 59's 5-line comparison
  comes after Sam's notes on animatic 3.
- **Needs Sam:** nothing until the clips.
- **Read:** pack "Notes round" in `guides/job-packs.md`; `notes/ledger/remakes-fable-r3.md`.
- **Open rule requests:** none.
- **For Claude:** _explosion/_hit/_puff/_shake (camp fx); BLAST, INCOMING, _g2() (G2_X); _kg_camp_face; CR.kg(gun_aim=);
  RS.town_reverse (+_street_side, _swag_wall, STREET_LEV); s13_pinned (S13_TRACK, mouth_k); LINEUP_Z/C; G3's fall in
  _camp's gunman() (note 65). Clips are drafts in clips/ (not on GitHub; gone after a container restart).
3:## Where things stand (the ONE handover)
4-- **Rules that bite next:** 30 (a "Sam N" finding: check that note before changing), 87, 89.
5-- **Done (11 Nov, Fable r3 part 1):** 17 of the 48 fixed, the worst first: 1-9, 18, 21-23, 26, 31, 33, 40 (what each
6-  did: `notes/ledger/remakes-fable-r3.md`, "Fixed"). No clips yet (the next chat sends one sheet of all moved beats).
7-- **Next (Opus, medium): the other 31 findings, worst first** (10-17, 20, 24, 25, 27-30, 32, 34, 36-39, 41-48; skip
8-  19, 35, 45 till Sam answers); one clip per moved beat; then open the Sonnet chat (medium): check sheet (subtitles,
9-  Hook Text, sign-off, sound), Sam's yes, animatic 3.
10-- **Needs Sam (questions, pick first):** 1 KG's bib keeps three ring spots (Fable: refs show two; two dots read as
11-  breasts in pass 2): Y/N. 2 The R1/R2 labels can't go higher (the app's top bar): leave them over the crest and flag
12-  (pick) or move them aside: Y/N. 3 Link's ball hands and tube arms stay (house rule): Y/N.
13-- **Read:** pack "Notes round" in `guides/job-packs.md`; `notes/ledger/remakes-fable-r3.md`.
14-- **Open rule requests:** none.
15-- **For Claude:** _flash(dirx=) muzzle cones; G2_MUZZLE (the gunmen's muzzle); S8_CX_MAX; S5_DX, _rifle_fall; GRAB,
16-  PIER_GAP, _pier (the wall); RC._Flip/_Squash/UNHAPPY (talking mouths); 'doubt' mouth; CAMP_MARKS link (-1.25, 5.0).
17-
18-## Open notes: animatic 1 (Sam, 10 Nov; Sam's numbers 1-6, then Claude's list Sam asked to be done)

## (replaced 11 Nov, barrel fix)
- **Rules that bite next:** 8 (Sam's reaction to the animatic is a note), 89 (critique round 3 pass 2 left open: named),
  62 (captions on the voice).
- **Done (11 Nov, Sonnet):** animatic 3 rendered with no check sheet (Sam, 11 Nov), finished with the Hook Text and
  sign-off, watched and listened once (note 40), sent (45 s, 4.8 MB, small render 540 x 960). A stale build (from before
  notes 66-74) was sent first by mistake and replaced with this one.
- **Next:** wait for Sam's look; his reaction is notes. Then a notes round (Opus, medium) and one more animatic; the final
  only on his clear yes.
- **Needs Sam:** his look at animatic 3.
- **Faults named (rendered with --faults-named):** critique round 3 pass 2 (29 faults, 65 can't tell, open); PROP TURN on
  Malon's bottle and Saria's ocarina at 30 degrees (line-up is front-on only); syllable counter misreads "R1", "9", "Ok?",
  capitals (5); caption "I don't think I" 0.9 s for 4 words (the voice's pace); "you s***." 1.45 s early is the checker
  misreading the take (one breath, "it" bleep at 34.06 s proves it).
- **Fixed in this chat:** line 13's subtitle pieces were 0.9 s early (PIECE_FIX in remakes.py).
- **Read:** pack "Checks and animatic" in `guides/job-packs.md`; source/remakes.py MAP.
- **Open rule requests:** none.
- **For Claude:** `remakes.py final source/data/remakes-clean.mp4 --small --faults-named`, then `finish.py ... --film remakes
  --faults-named`. ALWAYS merge origin/claude/create-claude-md-oe8z4g first (a stale copy cost a wasted render).


## (replaced 11 Nov, rules written)
- **Rules that bite next:** 8 (Sam's reaction to a clip is a note), 56 (a fault of its kind: check every case), 62
  (captions on the voice; re-check at 1.1x if Sam says yes).
- **Done (11 Nov, Opus medium):** barrel fix. Link (S7, 18.1-18.9 s) ran in a straight line through both barrels and
  was drawn over them while behind them (confirmed on stills). Now he runs down the clear lane right of the barrels and
  the lean-to's post, then curves left in front of them to his mark; same start, same ease, same arrival. Every other
  camp mover checked: KG, the lower-left gunman clear; the tower man and the kneeling man don't move; S8's debris is in
  the air. New check `camp_paths` (in `remakes.py check`) walks every mover against the camp's solid things each frame;
  it flags the old route. Clip of 17.8-19.9 s sent. Lost: none. Added: none (Link half behind KG's crest mid-run: KG
  is nearer, so that is the right order).
- **Next:** wait for Sam's look at the clip and his numbers (1.1x rule; trim round still wanted?). Then the trim-the-pace
  round (Opus, medium: notes/trim-speedup-handover.md) or, if 1.1x replaces it, a 1.1x animatic (Sonnet).
- **Needs Sam:** his look at the clip; his numbers on the 1.1x rule.
- **Read:** pack "Notes round" in `guides/job-packs.md`; source/remakes.py MAP.
- **Open rule requests:** 1.1x delivery for EVERY film (Sam, 11 Nov: no rule is one film's); wording proposed, awaiting his Y.
- **Captions (11 Nov, Sam):** Gotham Black look, white, black outline and shadow; Montserrat Black (free, OFL, in source/fonts) stands in for the paid Gotham.
- **Also done (11 Nov, Sonnet):** stone-wall thump (`_thump`) on the first push (SLAM), softer on each re-slam; Sam's yes. Trim round dropped (Sam).
- **For Claude:** `LINK_ROUTE`/`LINK_LANE_X` (-0.5) in remakes.py; `RS.SET_FEET` (camp footprints, 'under'/'over');
  `camp_paths()` in `checks()`. ALWAYS merge origin/claude/create-claude-md-oe8z4g first.
