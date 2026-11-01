# Notes for Flying Whales (working name; untitled; one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/flying-whales-handovers.md)
- **Rules that bite at the next stage (rule 48):** 8 and 33 (rehearsal clips of the risky moves before anything else:
  the opener's swing, its rise into the cut, the rig's three hits; any falling piece on a short close clip); 16 (up and
  to the right on both sides of the hard cut); 15 (effect shapes: the water burst, fireballs and splashes are lumpy,
  never regular spikes); 29 (every clip shows the film time and shot in its corner); 32 (pieces land and sink
  properly: nothing floats or balances on a point); 40 (tick the Showstopper lists U1-U15 and 1-18 at the first clips).
- **Done (1 Nov, building, Opus high):** (1) the brow on every whale (`source/whale.py`, on by default, `brow=False`
  for a calm whale): a heavy ridge slanting down towards the snout, standing proud of the head; plus a small white eye
  with the pupil glaring forward (my addition: a dark dot under a dark brow merged into a blob); line check clean.
  (2) The underwater set, `source/flying_whales_under.py`: water bands by direction, the surface from below with the
  gold window, light shafts, specks, bubble streams on the rise, the fish shoal scattering; wired into
  `flying_whales_opener.frame(t)`; benchmarked side by side with Sam's refs (B1-B10 all ticked; the water pushed to the
  refs' vivid blue after the comparison); sheet sent (`review/flying-whales-underwater-sheet.jpg`). (3) The rig,
  `source/flying_whales_rig.py`: 31 breakable pieces at real size through `flying_whales_sea.CAM`, JACKDAW board,
  flare flame, foam at the legs, `PARENT` (what hangs on what), `part_box` (for hit tests); a moved piece is repainted
  in perspective and cut off at the waterline; line check clean; sheet sent (`review/flying-whales-rig-sheet.jpg`:
  whole, numbered pieces, a break test, close-up). Both new sets are in `guides/kit-catalogue.md`; rig sizes in
  `source/sizes.py`.
- **Next (fresh chat, Opus high: new builds are needed for the clips):** (1) copy `source/satire_template.py` to
  `source/flying_whales.py` (no cast), wire the opener shot (`flying_whales_opener.frame`) and render rehearsal clip
  (a), the swing, 1.2-4.0 s (`final OUT --small --span 1.2 4.0`); (2) plan the rig scene's whale paths in metres (the
  burst out of the sea up and to the right, the five tracks, the two loops) and build the water burst, then clip (b),
  the rise and cut, 4.0-5.6 s plus the rig scene's first second; (3) the effects (fireball and black smoke, deck fire,
  steam, crown splash and foam rings, spike splashes, dust; the flare's smoke ribbon, Showstopper 3) and the rig's
  three clips: the first whale through the legs; a whale through the decks with a fireball; the final tip and splash.
  Clips need no yes; push-notify each. Start the new chat with: "Flying Whales: read the handover in
  notes/flying-whales.md and carry on (film file, clip (a), then the rig scene's whale paths)".
- **Tool gap:** `source/hook_text.py` can't draw colour emoji yet (the Hook Text has 🔥🔥🔥); Noto Color Emoji is
  installed; add it before the first animatic (small, Opus medium). Placed with `--y 352`, on for the whole video.
- **Losses and my additions Sam should know about:** additions: the small white eye under each brow (flagged, above);
  foam slapping round the legs; the flare's flame flickers. Not visible from our camera (not losses, just hidden): the
  helideck's orange chute (behind the stair tower) and most of the walkway stub (behind the decks). No losses.
- **Rule requests and proposals not yet in a guide:** none (searched this file).
- **Usage budget (rule 44):** 28% of the week at the start of this stage; ask Sam for the figure now.
- **Files to open:** this file; `guides/satire.md` ("Render", "Before every render"); `guides/film-quality-rules.md`
  8, 15, 16, 29, 32, 33, 40; the docstrings of `source/flying_whales_opener.py`, `source/flying_whales_under.py`,
  `source/flying_whales_rig.py`, `source/flying_whales_sea.py`, `source/whale.py`; `source/satire_template.py`.

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

## The brief as a checklist (CLAUDE.md, 18 Oct): ticked before the first animatic
| # | from the brief or a note (word for word) | done? |
|---|------|------|
| 1 | "a team of flying humpback whales is going to use their massive bodies to destroy an oil rig" | |
| 2 | "we see the Jackdaw Oil Field from a diagonal direction" | |
| 3 | "close enough to see details but not so far away that anything is distant" | |
| 4 | "The whole building is in shot" | |
| 5 | "from the camera side, flying humpback whales" | |
| 6 | "gently waving their flippers and shooting sea spray" | |
| 7 | "float towards them like determined fat torpedoes" | |
| 8 | "Don't have the whales slow down. If anything, they speed up the closer they get." | |
| 9 | "Like a hand smashing through a jenga tower, except its whales and a gas field." | |
| 10 | "They all begin to collide with the structure, bashing through it, smashing it apart" | |
| 11 | "with no harm to the whales" | |
| 12 | "eventually bringing the whole thing sliding into the sea" | |
| 13 | "causing some explosions in the process" | |
| 14 | "I don't want people on it, it's only funny if people don't die." | |
| 15 | "Dusk." (changed from day; Sam's final word, 1 Nov) | |
| 16 | "House satire" style | |
| 17 | Rig built from Sam's Jackdaw references (yellow jacket legs, boxy decks, helipad, crane, flare boom) | |
| 18 | CranbriJoos sign-off at the end (CLAUDE.md) | |
| 19 | "Let's do the 12 second shot" | |
| 20 | Sign: "Jackdaw" (the real name) | |

## Opening scene brief (Sam, 1 Nov; a checklist, ticked before the first animatic)
| # | from the brief or a note (word for word) | done? |
|---|------|------|
| O1 | Hook Text: "Blue Planet III looks 🔥🔥🔥" | |
| O2 | "Humpback whales zooming through the sea." | |
| O3 | "They come towards the camera, which moves around to follow alongside them." | |
| O4 | David Attenborough's voice: "This series, we will see animal behaviour we could scarcely have imagined." | |
| O5 | "As he reaches the end of the sentence, the whales are swimming upwards towards the surface." | |
| O6 | "Hard cut to Jackdaw scene" | |
| O7 | "In the opening scene, the whales are still beneath the waves." | |
| O8 | "Near the end of the scene, they start to shoot towards the surface." | |
| O9 | "In the Jackdaw scene, we see them flying." | |
| O11 | The joke (Sam, 1 Nov): "the new behaviour we are seeing is that the animals are so angry about climate change they are defying physics to destroy infrastructure" | |
| O10 | Sam (1 Nov, about the rig scene): "five whales smash their way through this rig, making it tumble and explode and break into parts in an orgy of effects and destruction and zooming, looping, attacking whales" | |

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
  (24, 27, 0); 3.4 s (92, 21, -1); 4.2 s (98, 21, -2); 5.6 s (112, 24, -10). Never above 1.5 m under the surface.
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
- The whales are slate blue-grey, not near-black (so the outline still reads at dusk and the line check can tell skin
  from ink); names for the five patterns (Inky, Blaze, Freckle, Bib, Ghost) are labels on the sheet only.

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | all | | dusk, not day (Sam, 1 Nov: "Changed mind. Dusk.") | done: sky and sea painted at dusk |
| 2 | whale sheet | | "Things look great so far" (Sam, 1 Nov): the whale approved | done |
| 3 | opening | | the opening scene brief (checklist O1-O11) | set built (flying_whales_under.py); clips next |
| 4 | rig | | "zooming, looping, attacking whales" (O10) | Sam: yes, two whales loop (Showstopper 17) |
| 5 | all | | angry whales: a heavy low brow (Sam's yes) | done: whale.py brow (+ small white eye, flagged) |

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
