# Notes for Flying Whales (working name; untitled; one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/flying-whales-handovers.md)
- **Rules that bite at this stage (rule 48):** 40 (the opening scene is new: its Showstopper list goes to Sam before
  anything is built; "looping" whales would change the approved list); 1 (the opening scene gets its own plan in
  metres: depth, where the surface is, the camera's path); 22 (my additions on a sheet and named: the clouds, the sun
  just set left of frame); 8 and 33 (rehearsal clips of the risky moves before the rest); 39 (the opener's camera moves
  round the whales: the whale is already a model, the underwater set is painted layers).
- **Done (1 Nov, building, Opus): Sam said yes to the whale ("Things look great so far"). The dusk sky and sea**
  (`source/flying_whales_sea.py`, in `guides/kit-catalogue.md`): the film's camera `CAM` (8 m up, 120 m from the rig,
  pitch 6, focal 1400; horizon at y 1107); sky bands purple to orange swelling over a sun just set left of frame (my
  choice: the rig stays side-lit, not a black silhouette); seven clouds lit from below (my addition); the sea
  mirroring the bands; ripple strokes on a slow swell drifting with the wind; a twinkling glitter path; low wave
  caps in front; `glow()` for the sea under fires (stand-in fireballs on the sheet). About 0.2 s a frame. Sheet
  `review/flying-whales-sea-sheet.jpg` and a 4 s clip of the sea moving sent. Self-review: three rounds of my own
  (spiky band edges, box-shaped glow, caps off-screen and paper-thin: all fixed).
- **Sam sent the opening scene (1 Nov):** checklist below ("Opening scene brief"). Sam answered all the questions
  (Decisions, "Opening scene answers"): he records the Attenborough line; about 5 s; whales swim at us on a slight
  diagonal, camera swings round alongside, they race up to the surface on "imagined"; same five whales; Hook Text on
  the whole video; two whales loop the loop and come back for a second hit (Showstopper 17, approved); a heavy low
  brow on every whale (approved change to the whale).
- **Next (fresh chat, Opus high):** plan the opening scene (planning, Opus high: Showstopper list, plan in metres, composition sheet); then the
  rig (building, Opus high: `source/flying_whales_rig.py`, about 30 breakable parts, JACKDAW board, rig sheet on the
  sea painting with a whale at real size, using `flying_whales_sea.CAM`); then the three rehearsal clips. Still to
  do: copy `source/satire_template.py` to `source/flying_whales.py` (no cast).
- **Tool gap:** `source/hook_text.py` can't draw colour emoji yet (the Hook Text has 🔥🔥🔥); Noto Color Emoji is
  installed; add it before the first animatic (small, Opus medium).
- **Losses and my additions Sam should know about:** additions: clouds; the sun just set left of frame; the glitter
  path; plus the earlier ones (below). No losses.
- **Rule requests and proposals not yet in a guide:** none (searched this file).
- **Usage budget (rule 44):** 28% of the week used at the start of the sky-and-sea chat (Sam, 1 Nov); about 24% at
  the end of the whale stage. Ask again at the start of the next chat.
- **Files to open:** this file; `guides/satire.md`; `guides/film-quality-rules.md` 1, 8, 22, 33, 39, 40;
  `guides/kit-catalogue.md`; `source/flying_whales_sea.py` docstring; `source/whale.py` docstring.

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

## References as checklists (`references/flying-whales/`)
| reference | what it shows | ours matches? |
|---|------|------|
| whale-side-painting, whale-side-under, fly-glide-side | long chunky body tapering to a thin tail stock; dark slate top, pale belly; small hump and fin two-thirds back; flippers a third of body length, white below, scalloped front edge | |
| whale-throat-grooves, whale-belly-flippers | broad flat head with rows of knobbly bumps; long pale grooves chin to belly | |
| whale-tail-behind, whale-rear-three-quarter, whale-pod-from-above | from behind: wide notched flukes with a ragged back edge, a spine ridge, flippers out to the sides | |
| whale-patterns-below | belly and fluke undersides from nearly all black to nearly all white: one per whale | |
| fly-painting-dive, whale-breach-* | arched body, flipper held out like a wing, water streaming off | |
| rig-jackdaw-* (5) | yellow lattice legs with X bracing; three or four boxy storeys with railings; helipad out to one side over an orange chute; tall crane; yellow name board; grey, white, red, orange, blue accents | |
| rig-night-*, rig-sunset-pipes, rig-legs-walkway-dusk | flare on a long boom with flame and smoke; chimneys; rows of warm lights at dusk; walkway bridge | |
| collapse-rig-tilting, -sinking | deck tips as one block, one end under, the other high; cranes stay attached | |
| collapse-rig-crumpled | one end collapsed: bracing tangled, deck sagging there, the rest standing | |
| collapse-cranes-fireball, collapse-dust | fireballs bursting from the sides, smoke in separate dark clumps above, flying bits; beige-grey dust billows with chunks | |
| fire-* (4) | tall lumpy fireball, yellow core, orange, dark red edge; black smoke mass above; deck fire streaming sideways; white steam at the base; sea orange under the fire | |
| splash-column-ring, splash-crown | a tall white column then a flat foam ring; a crown wall of water with spikes, a dark hollow, ripples and curling waves | |
| dusk-pink-sky-rig, dusk-sunset-waves | purple top, pink, orange at the horizon; streaky clouds lit from below; sea mirroring the sky in bands; warm streaks under the lights | |
Left out on purpose: one photo of the 9/11 attack (Sam's collapse refs); one duplicate dusk photo.

## My additions (flag to Sam; none built yet)
- Whales flying on out of frame after their hit (the brief says "no harm"; it doesn't say where they go).
- A one- or two-frame freeze on each contact, and camera shake.
- Lifeboats popping off and crane whipping (set life in the collapse).
- Sky and sea (1 Nov): seven clouds lit from below; the sun just set left of frame (so the rig is side-lit, not a
  silhouette); a glitter path of gold flecks under the sunset; low wave caps in front (Decisions: "warm wave caps").
- The whales are slate blue-grey, not near-black (so the outline still reads at dusk and the line check can tell skin
  from ink); names for the five patterns (Inky, Blaze, Freckle, Bib, Ghost) are labels on the sheet only.

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | all | | dusk, not day (Sam, 1 Nov: "Changed mind. Dusk.") | done: sky and sea painted at dusk |
| 2 | whale sheet | | "Things look great so far" (Sam, 1 Nov): the whale approved | done |
| 3 | opening | | the opening scene brief (checklist O1-O9) | open: answers in, to plan |
| 4 | rig | | "zooming, looping, attacking whales" (O10) | Sam: yes, two whales loop (Showstopper 17) |
| 5 | all | | angry whales: a heavy low brow (Sam's yes) | open: change whale.py |

Decisions made:
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
