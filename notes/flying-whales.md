# Notes for Flying Whales (working name; untitled; one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/flying-whales-handovers.md)
- **Rules that bite at this stage (rule 48):** 3 (benchmark the sky and sea against the dusk refs before Sam sees
  them); 22 (any set dressing of mine shown on the sheet and named); 40 (build only what the approved Showstopper
  list says; tick it at the first clip); 8 and 33 (rehearsal clips of the three risky moves before the rest); 32
  (debris falls into the sea and sinks, never floats or overlaps).
- **New from Sam (1 Nov, during the rig build): no Hook Text in this scene. Another first scene, not yet written,
  comes before this shot** (the whales are seen there too, which is why the whale is a full model). The sky at the
  top of the frame is now free: kept for the smoke.
- **Done (1 Nov, building, Opus): the rig** (`source/flying_whales_rig.py`, in `guides/kit-catalogue.md` and
  `source/catalogue.py`; sizes in `source/sizes.py`). The Jackdaw from the diagonal in 31 breakable parts (4 legs,
  8 bracing panels, cellar and process decks in halves, JACKDAW board, living and process modules, two lifeboats,
  containers, crane pedestal and boom, derrick, chimneys, flare boom with a moving flame, helideck, its truss,
  escape chute, walkway stub), each in real metres drawn flat through the film's one camera (`film_cam()`), the same
  camera the whales use. Why parts in metres and not one painting (rule 39 says 2D for a locked camera): pieces must
  tip, spin and sink the right way, the deck tips as one block, and whales pass between the legs; still no 3D
  library, just boxes and tubes drawn flat. Moving a part (`State.move`) carries what stands on it; `State.whole`
  tips everything as one block; anything below the sea is cut off by itself (the waterline). `composite()` lays
  rig and whales together pixel by pixel by depth (whale.py now gives every whale a `depth_map`; the line check still
  passes). Line check clean (`flying_whales_rig.py check`); benchmark against the three Jackdaw photos all ticked
  (`python3 source/benchmark.py flying_whales_rig OUT.jpg`); mirror test: JACKDAW reads the right way; the helideck
  is on the left as on the composition sheet (we see the opposite corner from the photo, not a mirror). About 1.4 s
  a frame at full size, 0.4 s small. Sheet sent: `review/flying-whales-rig-sheet.jpg` (remake:
  `python3 source/flying_whales_rig.py sheet OUT.jpg`).
- **Sam has not yet answered the whale sheet or the rig sheet.** His notes or yes come first in the next chat.
- **Flag for Sam (rig sheet):** at real size a whale at the rig is small: about 140 x 40 px in the full frame,
  about a quarter of the rig's width, and from this angle the crossed bracing hides much of a whale between the legs.
  The whales are big as they pass the camera. Asked him whether real size stays.
- **Next (fresh chat, Opus high; a new build):** (1) Sam's notes on the whale and rig sheets. (2) The dusk sky and sea
  (`source/flying_whales_sea.py`): pink-purple sky with streaky clouds lit from below, the sea mirroring it in
  bands, sparkle, a slow swell, the rig's reflection and warm streaks under its lights, foam at each leg; benchmark
  against dusk-pink-sky-rig and dusk-sunset-waves (rule 3); replaces `backdrop()` in the rig file. (3) Then copy
  `source/satire_template.py` to `source/flying_whales.py` (held back again: nothing needed it yet; it needs the
  12 s timeline, `scene(t)`, `PROP_SIZES`, `EFFECTS` with the flame, `BENCHMARK` from the rig file, no Hook Text)
  and render the three rehearsal clips (rule 8): the first whale through the legs, a whale bursting through the
  decks with a fireball, the final tip, slide and crown splash.
- **Losses and my additions Sam should know about:** additions: blue and red containers on the process deck, rows of
  lit windows and deck lights, railings on the deck ledges (all on the rig sheet); still standing from the whale
  stage: whales fly on out of frame, a freeze on each contact, lifeboats and crane whip, the whale's slate blue-grey
  and the pattern names. No losses (railings along the roof edges were tried and dropped before Sam saw them: they
  had no outline against the sky).
- **Rule requests and proposals not yet in a guide:** none (searched this file).
- **Usage budget (rule 44):** 24% of the week at the end of the whale stage; not asked at the start of the rig chat
  (missed); asked at this handover.
- **Files to open:** this file; `guides/satire.md`; `guides/film-quality-rules.md` 3, 8, 22, 32-34, 39, 40;
  `guides/kit-catalogue.md`; the dusk references.

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

## My additions (flag to Sam)
- Whales flying on out of frame after their hit (the brief says "no harm"; it doesn't say where they go).
- A one- or two-frame freeze on each contact, and camera shake.
- Lifeboats popping off and crane whipping (set life in the collapse).
- On the rig (built 1 Nov, on the rig sheet): blue and red containers on the process deck; rows of lit windows and
  deck lights; railings on the deck ledges.
- The whales are slate blue-grey, not near-black (so the outline still reads at dusk and the line check can tell skin
  from ink); names for the five patterns (Inky, Blaze, Freckle, Bib, Ghost) are labels on the sheet only.

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | all | | dusk, not day (Sam, 1 Nov: "Changed mind. Dusk.") | open |

Decisions made:
- Sam (1 Nov): no cost-saving cuts; the whales are needed in the prior scene too, so build them from every view.
- Sam (1 Nov, during the rig build): no Hook Text in this scene; another first scene, not yet written, comes first.
- Sam's answers (1 Nov): a prior scene comes first (not written yet); this shot is 12 s; no Hook Text for now;
  the sign reads the real name JACKDAW; no sound for now, visuals only (sound later); whales at real size (14 m);
  five whales.
- No people anywhere: empty rig, no boats or helicopters (Sam, 1 Nov).
- Dusk (Sam's final word, 1 Nov); the pink-purple sky with the calm mirrored sea, warm wave caps in front.
- House satire style; start from `source/satire_template.py`.
- One locked camera, 2D painted layers (rule 39).
- Whales: plain humpbacks, no wings or effects; flippers held out and gently waving; they speed up into each hit.
- References taken for shape and colour only; nothing from the real disasters appears in the film.
