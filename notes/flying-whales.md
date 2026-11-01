# Notes for Flying Whales (working name; untitled; one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/flying-whales-handovers.md)
- **Rules that bite at the next stage (rule 48):** the animatic waits for Sam's clear yes to the check sheet (18 Oct; a
  note is not a yes); unattended, one animatic then stop (25 Oct); 5 (by hand: falling pieces against the pieces still
  standing, and the braces inside the jacket); 25 (the 2-frame freezes and jolts only show in motion); 46 (frames Sam
  names are looked at first); self-review before the send (18 Oct).
- **Done (1 Nov, Opus medium):** Sam on clips (c)-(e): "Clips look good so far" (note 6). No recording for now: the
  Attenborough line runs as subtitles only (note 7; placeholder times 0.42-5.25 s, proofread). The colour emoji in
  `source/hook_text.py` (🔥 saved in `source/fonts/emoji/1f525.png`, Noto fallback; numerals stay with the word before).
  Both brief checklists ticked (O4 marked "changed"; 18, the sign-off, comes at the final). Pre-flight ran (7.5 min):
  6 faults, all named, none fixed: no `audits`, no `LINE_SUBJECTS`, no ROOMS, no plan cameras, no `scene(t)` (these
  are the people-and-rooms checks: this film has no people or rooms; the whales' own checks are `check`,
  `wreck.py check` and `paths.py contacts`, all clean); the rig shot is 12.0 s (Sam's own "12 second shot"). The check
  sheet (19 frames, 0.5-17.4 s) is `review/flying-whales-check-sheet.jpg`, sent to Sam.
- **Animatic sent (1 Nov, Sonnet):** Sam's yes to the check sheet; rendered 9.5 min, then Hook Text + 1.6 s sign-off (`--signoff-speed 1.25`, Sam's request), 19.2 s, 3 MB, `review/flying-whales-animatic.mp4`. Waiting for Sam's notes or a clear yes to the final. PROPOSED, awaiting Sam's yes: rule 'sign-off is 1.6 s on every film' (tiktok-design.md, CLAUDE.md, rule-register, finish.py default).
- **Animatic 1 notes (2 Nov, Opus): notes 8-13 fixed, two clips sent; waiting for Sam on the clips, then the check sheet and his yes for animatic 2 (Hook Text `--until 5.6`, `--signoff-speed 1.25`).**
- **Next (older plan, now partly done; fresh chat, Sonnet: a routine render):** Sam's yes to the check sheet (or his notes, which go back to Opus
  medium). On yes: `python3 source/flying_whales.py final source/data/flying-whales-animatic.mp4 --small` (17.6 s,
  423 frames; time it), then the Hook Text for the whole film: `python3 source/hook_text.py IN OUT "Blue Planet III
  looks 🔥🔥🔥" --y 352 --until 17.6` (the animatic needs no sign-off). Send it with a self-review; push notification.
  Start the new chat with: "Flying Whales: read the handover in notes/flying-whales.md; my answer to the check sheet
  is ..." The animatic stays off GitHub (drafts stay off).
- **Watch at the animatic:** the star test's splash and crown ages (named before: wide white water, not stars); the
  braces brushing a standing leg; the shake and freezes; the blowhole puffs from behind; the subtitles are small and
  low (house style) and now carry the line alone, so check they read on a phone; the whales are small in the rig
  scene (about 20 m from 120 m) and get lost behind the smoke from about 12.6 s; from 16 s the frame is only smoke
  and foam (the planned 0.85 s settle and the scene's end).
- **Sam's question (1 Nov), for the end-of-film audit:** "What's the point in building a rig with over thirty parts if
  most of it slides into the sea in a solid block anyway?" My answer: the parts carry the first 9 s of the rig scene
  (15 thrown, holed decks, bent derrick, snapped crane and flare boom); only the last 3 s are the block. But a few
  parts (inner braces, the far side) are barely seen, and the block finale saved work late. Lesson to weigh at the
  audit: build pieces only to the level the camera shows, and decide how the end looks before splitting the model.
- **Losses and my additions Sam should know about:** unchanged since the last handover (archive, 1 Nov effects stage),
  plus my one small addition today: "III" kept on the same line as "Planet" in the Hook Text.
- **Rule 44 reworded (Sam, 1 Nov: "Yes write into rules"):** usage asked only after a building stage, the animatic and the final; in `film-quality-rules.md` and `rule-register.md`.
- **Lessons I'd propose (16 Oct: say the number and I'll write them in):** (1) `guides/best-practice.md` Part 1 (falling
  things): "A long piece that falls into water or onto a floor lands flat: check its tilt at the moment it lands, and
  choose its spin so it isn't standing on its end." (2) `guides/satire.md` (effects): "Smoke from a moving or
  short-lived fire starts big and grows fast, or the column breaks into a string of beads." Not yet answered.
- **Rule requests and proposals not yet in a guide:** none from Sam (searched this file); the two lessons above are mine.
- **Usage budget (rule 44):** 37% (Sam, 1 Nov, after the check sheet: this stage cost under 1%).
- **At the end of this film (Sam, 1 Nov; do these after the final is sent, before closing the film):** (1) an audit of
  the project for what can be streamlined and made more efficient (include Sam's rig-parts question above); (2) an
  audit of how my messages to Sam can be shorter, clearer and more useful. Keep this item in every handover until both
  are done.
- **Files to open:** this file; `guides/preflight.md` (render lines); the check sheet.

## Plan extras (film-quality-rules 24-26)
**Ambition estimate (rule 24):** one long locked shot, but everything in it is new.
- New builds (all 2D, rule 39: one locked camera, so one painted picture in layers; no 3D):
  1. Humpback whale, seen from behind and above (rear three-quarter) at any size, plus a side view: flippers that
     wave, a tail that swishes, blow spray, five different belly and tail patterns (ref whale-patterns-below).
  2. The rig (Jackdaw-style) in about 30 breakable parts: yellow jacket legs and bracing, three deck storeys,
     helipad, crane, derrick, chimneys, flare boom with flame, walkway stub, lifeboats, name board.
  3. Dusk sky and sea painting (pink-purple sky, mirrored bands on the sea, sparkle, the glow under the fires).
  4. Effects: fireball with a black smoke column, a deck fire sheet, white steam at the waterline, crown splash and
     foam rings, small spike splashes for falling pieces, dust.
  5. The sea drawn in front of the rig as it sinks (the waterline cutting it off).
- Reused kit: `prepper_fx.Piece`/`burst` (debris under gravity; here it lands in the sea and sinks), `prepper_fx.flash`
  and `sparks`, `patriots3_fx.puffs` (smoke and dust) and `shake`, `satire_style` shapes. The sea in
  `patriots3_bunker.beach_layer` is a grey daytime sea and does not fit dusk: new.
- Risky moves (rule 8 rehearsal clips, before the rest): (a) the first whale through the legs; (b) a whale bursting
  through the decks with a fireball; (c) the final tip, slide and crown splash with the waterline cutting the rig off.
- Share of a week: about a third (estimate; ask Sam for the week's figure at each handover, rule 44).
- Slow tools (rule 36): none expected; all 2D.

**Holds per beat (rule 25; no eyelines: no people):** opening rig alone about 1.5 s; each hit readable for at least
0.3 s (a one- or two-frame freeze on contact, then the follow-through); finale tip and splash about 2.5 s; the smoke
and foam settle about 1 s before the sign-off.

**Sound effects (rule 26; none until Sam says yes):** asked in the first questions. Proposed: sea and wind bed; whale
calls as they come in; blowhole puffs; a steel crunch and clang on each hit; three or four explosions; a long metal
groan as it tips; the big splash; then the CranbriJoos slurp (standing).

## The world (rule 1)
Sizes in metres (real ones; check against `source/sizes.py` when building and add any missing):
- Humpback: 14 m long, flippers about 4.5 m each, tail flukes about 5 m across.
- Rig (Jackdaw-like normally unmanned platform): deck block about 50 m long, 35 m deep, three storeys about 25 m
  in all; jacket legs about 25 m from water to deck; crane boom about 35 m; flare boom about 45 m out.
- Camera: locked, about 120 m from the rig's nearest corner, low (about 8 m above the sea), looking at the rig
  diagonally, the whole rig in frame with room above for the smoke; slight drift and a shake on each hit.
- Whales come from behind the camera, low, and rise towards the rig, speeding up as they close.

Composition sheet sent: 1 Nov, review/flying-whales-composition.jpg

## Showstopper list (rule 40: Sam approves or trims before anything is built; ticked at the first rehearsal clip)
| # | element | why |
|---|------|------|
| 1 | The rig whole, from the diagonal, at dusk, close enough for detail (railings, lit windows, lifeboats, name board) | the brief: "close enough to see details", "whole building in shot" |
| 2 | Calm sea with pink and orange bands, sparkle, a slow swell; the rig's legs with foam at the waterline | dusk refs; the sea is half the frame |
| 3 | The flare burning before anything happens, with its ribbon of smoke | the dusk refs; it makes the rig live before the attack |
| 4 | Five humpbacks, each its own size and markings, entering from behind the camera at different heights and times | "a team"; told apart at a glance |
| 5 | Each whale waves its flippers gently and puffs spray from the blowhole as it comes | the brief |
| 6 | Each whale speeds up the closer it gets; no slowing on impact | Sam's note: like a hand through a Jenga tower |
| 7 | Hits spread over the rig, one after another: legs, lower deck, top deck and crane, helipad, flare boom | the rig comes apart in stages and each hit reads |
| 8 | Whales come out the far side unhurt and fly on, out of frame | "no harm to the whales" |
| 9 | Debris thrown the way each whale was going, falling under gravity, each piece splashing into the sea | rule 32 and the satire guide |
| 10 | Bracing crumpling, the deck sagging at the broken end while the rest stands | ref collapse-rig-crumpled |
| 11 | Deck fires after the first hits; three or four fireballs with black smoke columns in the middle hits | refs fire-*; "some explosions" |
| 12 | The crane and derrick whipping and toppling; lifeboats popping off | ref collapse-cranes-fireball; life in the collapse |
| 13 | The finale: the whole deck tips as one block and slides into the sea, the far end rising, the tower last | refs collapse-rig-tilting, -sinking |
| 14 | A crown splash, white steam at the waterline, foam rings spreading, the sea glowing orange under the fire | refs splash-crown, splash-column-ring, fire-dusk-glow |
| 15 | Camera shake on each hit, bigger at the finale | weight |
| 16 | Nobody on the rig, no boats, no helicopters | Sam: "it's only funny if people don't die" |
| 17 | Two whales loop the loop after their first hit and come back for a second smash (Sam's yes, 1 Nov) | "zooming, looping, attacking whales"; the defying-physics joke |
| 18 | Every whale wears a heavy, low, cross brow over each eye (Sam's yes, 1 Nov; a change to the approved whale) | the joke: they are angry about climate change |

Ticked at the rig clips (c), (d), (e), 1 Nov: 1, 2, 3 (the smoke ribbon, now built), 4, 6, 7, 8, 9, 11 (four fireballs,
three deck fires), 13, 14, 16, 17, 18 yes; 5 yes (the puffs from behind still to judge in motion); 10 partly (the braces
snap off whole rather than crumple; the sag is the first moment of the finale's tip); 12 partly (the crane's boom whips
and topples, the lifeboats pop off; the derrick whips and stays bent, so it can go under last); 15 built (a jolt on each
hit, the biggest at the crown; judge in motion).

## The brief as a checklist (CLAUDE.md, 18 Oct): ticked before the first animatic
| # | from the brief or a note (word for word) | done? |
|---|------|------|
| 1 | "a team of flying humpback whales is going to use their massive bodies to destroy an oil rig" | yes: five whales smash the rig apart (sheet 6.6-15.6) |
| 2 | "we see the Jackdaw Oil Field from a diagonal direction" | yes: the rig seen corner-on, two faces showing (5.8) |
| 3 | "close enough to see details but not so far away that anything is distant" | yes: the whole rig fills the middle third, decks readable (5.8) |
| 4 | "The whole building is in shot" | yes: legs to flare tip in frame until it sinks |
| 5 | "from the camera side, flying humpback whales" | yes: they burst out of the sea in front of the rig, nearest us (5.8-6.6) |
| 6 | "gently waving their flippers and shooting sea spray" | yes: flippers wave (paths), blowhole puffs and spray (6.6-7.6) |
| 7 | "float towards them like determined fat torpedoes" | yes: fat bodies, straight noses-first runs (7.6) |
| 8 | "Don't have the whales slow down. If anything, they speed up the closer they get." | yes: paths speed up into each hit (`paths.py`) |
| 9 | "Like a hand smashing through a jenga tower, except its whales and a gas field." | yes: they go through the legs and decks and out the far side (8.6-12.6) |
| 10 | "They all begin to collide with the structure, bashing through it, smashing it apart" | yes: every whale hits; 15 pieces thrown loose (`wreck.py`) |
| 11 | "with no harm to the whales" | yes: they fly on out of frame unhurt |
| 12 | "eventually bringing the whole thing sliding into the sea" | yes: the rig tips and slides under, all under at 15.6-16.6 |
| 13 | "causing some explosions in the process" | yes: four fireballs plus deck fires (9.6-12.6) |
| 14 | "I don't want people on it, it's only funny if people don't die." | yes: nobody on the rig, no boats or helicopters |
| 15 | "Dusk." (changed from day; Sam's final word, 1 Nov) | yes: pink-purple dusk sky, sun-glow on the sea |
| 16 | "House satire" style | yes: flat colour, one ink outline (house look) |
| 17 | Rig built from Sam's Jackdaw references (yellow jacket legs, boxy decks, helipad, crane, flare boom) | yes: yellow jacket legs, boxy decks, helideck, crane, flare boom |
| 18 | CranbriJoos sign-off at the end (CLAUDE.md) | at the final: `finish.py` adds it (not in the animatic) |
| 19 | "Let's do the 12 second shot" | yes: the rig scene is 12.0 s (5.6-17.6) |
| 20 | Sign: "Jackdaw" (the real name) | yes: JACKDAW on the deck sign (5.8) |

## Opening scene brief (Sam, 1 Nov; a checklist, ticked before the first animatic)
| # | from the brief or a note (word for word) | done? |
|---|------|------|
| O1 | Hook Text: "Blue Planet III looks 🔥🔥🔥" | yes: `HOOK`, upper band y 352, whole video; emoji now drawn (added by `finish.py`) |
| O2 | "Humpback whales zooming through the sea." | yes: the pod speeds through open water (0.5-3.6) |
| O3 | "They come towards the camera, which moves around to follow alongside them." | yes: they come at us on a diagonal, camera swings to their side (0.5-4.6) |
| O4 | David Attenborough's voice: "This series, we will see animal behaviour we could scarcely have imagined." | changed (Sam, note 7): subtitles only, no voice; placeholder times (0.3-5.0) |
| O5 | "As he reaches the end of the sentence, the whales are swimming upwards towards the surface." | yes: they tilt up on "imagined" (4.2-5.4) |
| O6 | "Hard cut to Jackdaw scene" | yes: hard cut at 5.6 |
| O7 | "In the opening scene, the whales are still beneath the waves." | yes: all under water until 5.6 |
| O8 | "Near the end of the scene, they start to shoot towards the surface." | yes: they race for the bright surface (4.6-5.4) |
| O9 | "In the Jackdaw scene, we see them flying." | yes: flying in the rig scene |
| O11 | The joke (Sam, 1 Nov): "the new behaviour we are seeing is that the animals are so angry about climate change they are defying physics to destroy infrastructure" | yes, by the action (no words state it): angry brows, they wreck the rig |
| O10 | Sam (1 Nov, about the rig scene): "five whales smash their way through this rig, making it tumble and explode and break into parts in an orgy of effects and destruction and zooming, looping, attacking whales" | yes: five whales, loops (Showstopper 17), fire, pieces, the sinking |

## Opening scene: Showstopper list (rule 40: approved by Sam 1 Nov; ticked at the first rehearsal clip)
| # | element | why |
|---|------|------|
| U1 | Open blue water, no sea bed: deep navy below, lighter teal towards the surface, fading to blue about 45 m off | Blue Planet's open-ocean humpback shots; nothing to distract from the whales |
| U2 | The surface seen from below: a bright, wavy, rippling ceiling, warm gold at dusk where the sun is | O5, O8: the whales race "towards the surface", so it must be there to aim at |
| U3 | Light shafts slanting down from the surface, swaying slowly | the Blue Planet look; makes it read as "under the sea" at a glance |
| U4 | Specks drifting in the water (marine snow) | the only fixed things in open water: without them the camera's swing can't be seen |
| U5 | The same five whales (Inky leads; Blaze, Freckle, Bib, Ghost), same patterns and sizes as the rig scene | Sam: "the same five whales" |
| U6 | A loose, staggered pod (different depths, a length or two apart; each follows the lead's path, so they tilt up one after another) | "a team"; never marching in step (rule 9) |
| U7 | Each whale's flippers waving, tail beating; they speed up all scene (6 to 8 m/s, then 13 m/s on the rise) | O2 "zooming"; the rig brief: they speed up, never slow |
| U8 | The heavy low brow on every whale, readable on the lead's close pass (moment 2) | the joke seeds here: they are angry |
| U9 | The camera: in front as they come at us on a slight diagonal, then swinging round to their right side and pacing them | O3; Sam's answer (diagonal, swing round alongside) |
| U10 | Freckle passing low under the lens on our side | a foreground layer (rule 4) and a sense of size |
| U11 | On "imagined": they tilt up 40 degrees and race for the surface, trailing bubbles; the camera drops below them and tilts up | O5, O8 |
| U12 | Hard cut just before the lead breaks the surface; they burst out in the rig scene heading up and to the right | O6; rule 16 (direction holds: up-right in both) |
| U13 | The Hook Text on from the first frame, in the upper band (y 245-460), clear of the whales | O1; Sam: Hook Text on the whole video |
| U14 | A shoal of small silver fish that scatters as the pod charges through (my addition; Sam: yes) | Blue Planet life; shows the speed |
| U15 | No divers, boats or people; nothing above the surface shows (the rig is a surprise) | Sam: no people; the cut must surprise |

## Opening scene: the plan in metres (rule 1; the numbers live in `source/flying_whales_opener.py`)
- World: whale.py's axes (x right, y away from the first camera, z up). Sea surface z = 0; open water; you can see
  about 45 m. The pod swims along +x (screen right once the camera is beside them).
- The lead (Inky) starts 14 m down. Formation behind the lead along its path (back, to its right, up; m): Blaze
  (-9, -6, +3), Freckle (-15, +5, -5: our side, low), Bib (-21, -11, -1), Ghost (-28, -3, +4).
- Speed: 6 m/s rising to 8 m/s up to "imagined" (4.2 s); then 13 m/s within 1 s, pitching up 40 degrees over 0.6 s.
  The lead is about 6 m under the surface at the cut.
- Camera (one lens, focal 1400, the rig scene's): placed round a point 7 m behind the lead (2 m once they rise), by
  angle from straight ahead of the pod towards its right, distance and height: 0 s (20 deg, 44 m, +1); 1.8 s
  (24, 27, 0); 3.4 s (92, 26, -1); 4.2 s (98, 26, -2); 5.6 s (112, 27, -10). Never above 1.5 m under the surface.
  The aim eases from 7 m behind the lead onto its middle as the camera swings round (1.8-3.4 s), so side-on the lead
  is whole in the frame (clip (a), 1 Nov: aimed 7 m behind it, the lead's head was cut off from 2.5 s on).
- Timing (placeholder until Sam's recording; re-pin to his word times): line 0.3-5.0 s; "imagined" 4.2 s; cut 5.6 s.
  The whole film: about 5.6 s + 12 s + 2 s sign-off = about 20 s.
- Holds (rule 25; no people, so no eyelines): the pod's approach about 1.8 s; the lead's face and brow readable for at
  least 0.5 s around 2.0 s; side-on alongside about 0.8 s (3.4-4.2 s); the rise about 1.4 s, cut on the motion.
- Hook Text (rule 10): the band y 245-460 of 1920 (`--y 352`), the same band as the rig composition; whales kept
  below it (moment 4 is the closest: the lead's head at about y 640).
- Risky moves (rule 8, clips before the rest): (a) the swing round, 1.2-4.0 s (does the turn read; do the specks
  sell it; does Freckle's pass under the lens look right); (b) the rise and the cut into the rig scene, 4.0-5.6 s plus
  the rig scene's first second (direction across the cut; the surface ceiling; the Hook Text clear).
- Ambition (rule 24): new builds: the underwater set (2D, painted by direction: the bands, surface and shafts turn
  with the camera; no 3D model, rule 39), bubbles, specks, the shoal if wanted. Reused: `whale.py` (any view, the
  five patterns), the camera class. About a tenth of a week on top of the rig scene's third.
- Sounds (rule 26; Sam: sound later, so not asked yet): the Attenborough line (Sam records); proposed for later: a
  low underwater hum, humpback song under the line, a rush of bubbles on the rise.

## Rig scene: the whale paths in metres (rule 1; the numbers live in `source/flying_whales_paths.py`, 1 Nov)
- Clock: the rig scene's own (0 = the hard cut at film 5.6 s). Camera locked at (0, -120, 8). Each path is a smooth
  curve through waypoints; the moment each breaks the surface and each hit are pinned to a time, and the speed changes
  evenly between pins and never drops into a hit (checked: `paths.py speeds`).
- The burst (U12, rule 16): all five break the surface 35-60 m from the lens, low in the frame and clear of the rig,
  left to right in the order of their targets (Bib, Freckle, Inky, Blaze, Ghost) at 0.65, 0.35, 0.0, 0.2, 0.5 s, nose
  up and heading away to the right, so on screen they rise up and to the right as they left the opener. 16 m/s out of
  the water. The burst is `source/flying_whales_fx.py` (a collar of froth hiding the waterline cut, a column of water
  thrown up and falling back as drops, a foam ring breaking into clumps).
- The hits (first touch, from `paths.py contacts`; at least 0.4 s apart): Inky through the legs' front low X brace
  2.56 (and the back brace 2.98); Blaze through the right cellar deck 3.03 (both right lifeboats); Bib through the
  stair tower 3.71 (helideck truss, helideck, the left mezzanine's corner); Freckle through the left top deck into
  the crane house 4.25 (then both chimneys); Ghost through the flare boom 5.02; Blaze again, the right top deck 6.45
  (and the derrick 6.80); Bib again, the front left leg low 7.59 (and the braces round it): the finale starts.
- Speeds at the hits: 32-54 m/s on the first pass; 75 m/s (Blaze) and 56 m/s (Bib) coming out of the loops.
- The loops (Showstopper 17): up behind the rig, over its top and down in front, so the rig sits inside the loop;
  widened sideways so each shows as a ring on screen (Blaze anticlockwise on the right, round the derrick; Bib
  clockwise on the left); tops at 69-70 m, just under the Hook Text band. They bank by the pull of the turn, so they
  are upside down over the top.
- Off frame after their last hit: Inky 4.6 s (right), Ghost 6.5 (top right), Freckle 6.6 (left), Blaze 7.8 (right),
  Bib 9.4 (left). The finale (about 7.8-10.7) has no whales in it; smoke and foam settle 10.7-12.
- Every contact is planned (`paths.py contacts` flags any other).

## Underwater benchmark (rule 3; Sam's refs: whale-side-under, whale-side-painting, whale-rear-three-quarter, whale-pod-from-above, whale-belly-flippers, whale-throat-grooves, whale-tail-behind)
| # | what makes it read as under the sea | ref | ours? |
|---|------|------|------|
| B1 | Open water, no sea bed: bright blue up top, deep navy below | rear-three-quarter, pod-from-above | yes (benchmark sheet, 1 Nov) |
| B2 | The surface from below: a bright wavy ceiling broken into ripple shapes | side-under, side-painting | yes (benchmark sheet, 1 Nov) |
| B3 | Light shafts fanning down from the surface | side-painting | yes (benchmark sheet, 1 Nov) |
| B4 | A trail of bubbles behind a whale | pod-from-above | yes (benchmark sheet, 1 Nov) |
| B5 | Distance fades whales into the blue (the far one paler, less contrast) | pod-from-above, rear-three-quarter | yes (benchmark sheet, 1 Nov) |
| B6 | Lit from above: backs bright, bellies in shade, white flippers glowing | side-under, belly-flippers | yes (benchmark sheet, 1 Nov) |
| B7 | Small specks and bubbles hanging in the water near the surface | side-under | yes (benchmark sheet, 1 Nov) |
| B8 | Near the surface: its underside as a hard line, the whale's back just under it | tail-behind, throat-grooves | yes (benchmark sheet, 1 Nov) |
| B9 | Whales blue-grey under water (never black), white flippers and bellies the brightest thing | all | yes (benchmark sheet, 1 Nov) |
| B10 | Ours is dusk (Sam's yes): the same layout, the surface glowing warm gold, the water deeper teal | (our choice) | yes (benchmark sheet, 1 Nov) |

## Opener questions (sent to Sam 1 Nov; each with my recommendation; all answered, see Decisions)
1. Underwater references (rule 3): none yet. Recommend: Sam sends 4-6 (Blue Planet humpbacks in open blue water from
   the front and side; the surface from below; light shafts), or says "find them" and I find them.
2. Light under the sea: recommend dusk (deep blue-teal water, the surface glowing warm gold), the same evening as the
   rig scene, over a bright midday blue.
3. Hook Text: recommend moving it from the middle (y 880) to the upper band for the whole video, since the middle is
   where all the action is for 20 s.
4. The fish shoal (U14, my addition): recommend yes (small, cheap, very Blue Planet).
5. Bubble trails from the blowholes on the rise (my addition): recommend yes.

Composition sheet sent (opener): 1 Nov, review/flying-whales-opener-composition.jpg

## References as checklists (`references/flying-whales/`)
| reference | what it shows | ours matches? |
|---|------|------|
| whale-side-painting, whale-side-under, fly-glide-side | long chunky body tapering to a thin tail stock; dark slate top, pale belly; small hump and fin two-thirds back; flippers a third of body length, white below, scalloped front edge | |
| whale-throat-grooves, whale-belly-flippers | broad flat head with rows of knobbly bumps; long pale grooves chin to belly | |
| whale-tail-behind, whale-rear-three-quarter, whale-pod-from-above | from behind: wide notched flukes with a ragged back edge, a spine ridge, flippers out to the sides | |
| whale-patterns-below | belly and fluke undersides from nearly all black to nearly all white: one per whale | |
| fly-painting-dive, whale-breach-* | arched body, flipper held out like a wing, water streaming off | |
| rig-jackdaw-* (5) | yellow lattice legs with X bracing; three or four boxy storeys with railings; helipad out to one side over an orange chute; tall crane; yellow name board; grey, white, red, orange, blue accents | yes (rig sheet 1 Nov); the chute is there but hidden behind the stair tower from our camera |
| rig-night-*, rig-sunset-pipes, rig-legs-walkway-dusk | flare on a long boom with flame and smoke; chimneys; rows of warm lights at dusk; walkway bridge | yes, except the flare's smoke ribbon (comes with the effects); the walkway is a stub, mostly hidden |
| collapse-rig-tilting, -sinking | deck tips as one block, one end under, the other high; cranes stay attached | |
| collapse-rig-crumpled | one end collapsed: bracing tangled, deck sagging there, the rest standing | |
| collapse-cranes-fireball, collapse-dust | fireballs bursting from the sides, smoke in separate dark clumps above, flying bits; beige-grey dust billows with chunks | |
| fire-* (4) | tall lumpy fireball, yellow core, orange, dark red edge; black smoke mass above; deck fire streaming sideways; white steam at the base; sea orange under the fire | |
| splash-column-ring, splash-crown | a tall white column then a flat foam ring; a crown wall of water with spikes, a dark hollow, ripples and curling waves | |
| dusk-pink-sky-rig, dusk-sunset-waves | purple top, pink, orange at the horizon; streaky clouds lit from below; sea mirroring the sky in bands; warm streaks under the lights | |
Left out on purpose: one photo of the 9/11 attack (Sam's collapse refs); one duplicate dusk photo.

## My additions (flag to Sam)
- Whales flying on out of frame after their hit (the brief says "no harm"; it doesn't say where they go).
- A one- or two-frame freeze on each contact, and camera shake.
- Lifeboats popping off and crane whipping (set life in the collapse).
- Sky and sea (1 Nov): seven clouds lit from below; the sun just set left of frame (so the rig is side-lit, not a
  silhouette); a glitter path of gold flecks under the sunset; low wave caps in front (Decisions: "warm wave caps").
- A small white eye under each brow, the pupil glaring forward (1 Nov; the dark eye merged with the dark brow).
- Foam slapping round the rig's legs; the flare's flame flickers (1 Nov).
- The wreck (1 Nov): holes torn in the decks with embers; dust from each holed deck; the gas burst where the flare boom
  snaps (fourth fireball); the flame riding the falling boom, out in steam; the helideck spinning like a plate; the
  crane's boom snapping off on its own; flying bits from every hit; froth along the waterline in the finale.
- The whales are slate blue-grey, not near-black (so the outline still reads at dusk and the line check can tell skin
  from ink); names for the five patterns (Inky, Blaze, Freckle, Bib, Ghost) are labels on the sheet only.

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | all | | dusk, not day (Sam, 1 Nov: "Changed mind. Dusk.") | done: sky and sea painted at dusk |
| 2 | whale sheet | | "Things look great so far" (Sam, 1 Nov): the whale approved | done |
| 3 | opening | | the opening scene brief (checklist O1-O11) | set built; clips (a) and (b) sent 1 Nov |
| 4 | rig | | "zooming, looping, attacking whales" (O10) | Sam: yes, two whales loop (Showstopper 17) |
| 5 | all | | angry whales: a heavy low brow (Sam's yes) | done: whale.py brow (+ small white eye, flagged) |
| 6 | rig | | clips (c)-(e): "Clips look good so far" (Sam, 1 Nov) | done: approved as they are |
| 7 | opening | | "I can't record right now so just use subtitle" (Sam, 1 Nov) | done: Attenborough line as subtitles only, no voice; placeholder times stand |
| 8 | rig | 10.17 | "a whale clips through the helicopter pad" (Sam, 2 Nov, animatic 1) | done: Bib only nudged it (0.36 of its speed) and caught it up; now batted off its path, out to our left and up (`HELI_SIDE`, `HELI_UP`); clip sent |
| 9 | rig | 15.36 | "the building clips through its own smoke" | done: in the finale the smoke is wholly behind the rig (it was sorted half in front, half behind); clip sent |
| 10 | rig | | Blaze's loop: "make him arc higher; most of his journey is blocked by the smoke" | done: the loop's top 70 m to 95 m (about y 490 to y 190), down in front of the smoke; speed at the second hit 75 to 98 m/s; contacts the same; clip sent |
| 11 | rig | 15.25 | "the spray of water clips behind the Jackdaw sign" | done: finale splashes and bits drawn over the whole rig; clip sent |
| 12 | rig | | "even bigger throw up of spray and debris" when the rig hits the water | done: crown splash bigger (size 13 to 19 m, 34 to 52 lumps, height x1.4) plus 46 big bits of debris; clip sent |
| 13 | all | | "The hook text should disappear in the rig scene, it blocks the view" | done: Hook Text off at the cut (`--until 5.6`; `HOOK` in flying_whales.py) |

Decisions made:
- Opener answers (Sam, 1 Nov: "all is well and you can continue"): Showstopper list U1-U15 approved; no more
  references (seven underwater refs already in); dusk light under the sea; the Hook Text in the upper band (y 245-460)
  for the whole video; the fish shoal yes; bubble trails on the rise yes.
- Opening scene answers (Sam, 1 Nov): Sam records the Attenborough line himself (an impression; remind him: a second
  of silence after, Voice Isolation off); about 5 s, then a hard cut to Jackdaw; the whales swim at us "but at a
  slight diagonal", the camera swings round to their side and swims alongside, and on "imagined" they tilt up and race
  for the bright surface; the same five whales (same patterns) in both scenes; the Hook Text stays on for the whole
  video; two whales loop the loop and come back; a heavy low brow on every whale; the sky-and-sea additions (clouds,
  sun just set left, glitter path) not objected to.
- Sam (1 Nov): no cost-saving cuts; the whales are needed in the prior scene too, so build them from every view.
- Sam's answers (1 Nov): a prior scene comes first (not written yet); this shot is 12 s; no Hook Text for now;
  the sign reads the real name JACKDAW; no sound for now, visuals only (sound later); whales at real size (14 m);
  five whales.
- No people anywhere: empty rig, no boats or helicopters (Sam, 1 Nov).
- Dusk (Sam's final word, 1 Nov); the pink-purple sky with the calm mirrored sea, warm wave caps in front.
- House satire style; start from `source/satire_template.py`.
- One locked camera, 2D painted layers (rule 39).
- Whales: plain humpbacks, no wings or effects; flippers held out and gently waving; they speed up into each hit.
- References taken for shape and colour only; nothing from the real disasters appears in the film.
