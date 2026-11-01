# Flying Whales: old handovers (newest first)

## Handover of 1 Nov (end of the film file, paths, water burst, clips (a) and (b))
- **Rules that bite at the next stage (rule 48):** 15 (every new effect listed in `EFFECTS` and shape-tested: the
  fireball lumpy, never a star; smoke in separate clumps; no motion lines); 32 and 33 (falling pieces land in the sea
  and sink, never float or balance on a point; test them on short close clips first); 5 (nothing passes through
  anything: `paths.py contacts` flags any unplanned touch); 25 (each hit readable for at least 0.3 s, a one- or
  two-frame freeze on contact); 8 (the rig's three rehearsal clips before the rest); 29 (clips carry the time stamp:
  automatic); 40 (tick Showstoppers 1-18 at the rig clips); 26 (no sound effects until Sam says yes).
- **Done (1 Nov, building, Opus high):** (1) the film file `source/flying_whales.py` (from the template; no cast; two
  shots, 'under' 0-5.6 s and 'rig' 5.6-17.6 s; 24 fps, not the house 12, because the camera swing and fast whales
  strobe at 12; `check` clean). (2) Clip (a), the swing (1.2-4.0 s), sent: the camera now eases its aim onto the lead
  so side-on the lead whale is whole in the frame (it was cut off by the right edge; the camera sits 5 m further back
  there). (3) The rig scene's whale paths in metres, `source/flying_whales_paths.py` (see "Rig scene: the whale paths"
  below): five tracks, the two loops round the rig, hits pinned, speeds checked never to drop into a hit, every
  contact planned (`contacts`). (4) The water burst, `source/flying_whales_fx.py`, and `whale.draw(cut_z=0)` (the
  body hidden below the sea); shape-tested (`EFFECTS`). (5) Clip (b), the rise, cut and the rig scene's first second
  (4.0-6.6 s), sent. (6) `R.draw(extra=...)` sorts whales in among the rig's pieces by distance. Kit catalogue updated
  (paths, burst, `cut_z`, `extra`). Showstoppers U1-U15 ticked at clips (a) and (b) (U8: the brow reads, but small).
- **Next (fresh chat, Opus high, building):** the effects in `source/flying_whales_fx.py`: the hits themselves (each
  piece in `paths.HITS`/`KNOCK_ONS` knocked loose at its contact time with `R.draw(xf=...)`, thrown the way the whale
  was going, falling under gravity, splashing (small spike splashes, lumpy) and sinking; `PARENT` pieces fall with
  what they hang on; a 1-2 frame freeze and camera shake on each contact); fireball with black smoke (Blaze's two hits,
  Bib's helideck), deck fire, steam, dust, the flare's smoke ribbon (Showstopper 3), the crown splash and foam rings;
  the finale (from 7.6 s: the deck tips left end first as one block, slides into the sea, the tower last). Then the
  rig's three clips: (c) Inky through the legs (rig 2.2-3.2 s = film 7.8-8.8); (d) Blaze through the cellar deck with a
  fireball (film 8.4-9.4); (e) the final tip and splash. Clips need no yes; push-notify each. Start the new chat with:
  "Flying Whales: read the handover in notes/flying-whales.md and carry on (the hits and effects, then the rig's three
  clips)".
- **Watch at the next clip:** the blowhole puffs seen from behind may read as white balloons on sticks (judge in
  motion; Showstopper 5); the burst trips the star test only in its first two frames (a wide flat blob) and at 0.7 s
  (scattered spray, tested as spray at 1.1 s instead): named, not changed.
- **Tool gap:** `source/hook_text.py` can't draw colour emoji yet (the Hook Text has 🔥🔥🔥); Noto Color Emoji is
  installed; add it before the first animatic (small, Opus medium). Placed with `--y 352`, on for the whole video.
- **Losses and my additions Sam should know about:** loss: in the opener's side-on stretch the whales are a little
  smaller (camera 26 m away, not 21, so the lead fits). Change from the rig plan: the whales no longer come "from
  behind the camera"; they burst out of the sea in front of it (the opener's cut needs them coming up out of the water).
  Hits moved 0.3 s later than first planned (first hit at 2.56 s: the rig is seen whole a little longer). Additions:
  the foam ring that breaks into floating froth clumps after each burst; each whale puffs its blowhole 0.9 s after
  surfacing; the knock-ons (lifeboats, chimneys, derrick) as whales pass through. Earlier: the small white eye under
  each brow, foam at the legs, the flickering flare.
- **Rule requests and proposals not yet in a guide:** none (searched this file).
- **Usage budget (rule 44):** 34% of the week (Sam, 1 Nov, end of this stage: film file, paths, burst, clips (a) and
  (b) took about 3%). Ask again at the next handover.
- **Files to open:** this file ("Rig scene: the whale paths", the Showstopper list 1-18); `guides/film-quality-rules.md`
  5, 8, 15, 25, 32, 33, 40; the docstrings of `source/flying_whales_fx.py`, `source/flying_whales_paths.py`,
  `source/flying_whales_rig.py` (`draw`, `PARENT`, `rot`, `part_box`), `source/flying_whales_sea.py` (`glow`);
  `guides/kit-catalogue.md` (reuse `prepper_fx` debris and `patriots3_fx` puffs before building new).

## Handover of 1 Nov (end of the opener plan)
- **Rules that bite at this stage (rule 48):** 3 (benchmark the underwater set against "Underwater benchmark" below,
  side by side with the refs, before Sam sees it); 22 (my additions shown and named on the sheet: dusk light under the
  sea, the fish shoal, bubble trails, specks); 39 (the underwater set is 2D, painted by view direction so it turns with
  the camera; the whale is already a model; the rig is one locked camera, painted layers); 16 (up and to the right on
  both sides of the hard cut); 8 and 33 (rehearsal clips of the risky moves before the rest).
- **Done (1 Nov, planning, Opus high): the opening scene planned and approved.** Sam: "all is well and you can
  continue": the opener Showstopper list (U1-U15) approved, and all five recommendations taken (Decisions, "Opener
  answers"). The plan in metres is numbers in `source/flying_whales_opener.py` (pod formation, the lead's track, the
  camera's swing, timings; `comp OUT.jpg` draws the rough sheet); the composition sheet was sent
  (`review/flying-whales-opener-composition.jpg`, once, rule 45). No more references needed: seven of Sam's whale refs
  are underwater (benchmark below).
- **Next (fresh chat, Opus high, building):** (1) the brow on every whale (`source/whale.py`, note 5: heavy, low,
  angled down to the middle over each eye; readable on the lead's close pass at about 2.0 s); (2) the underwater set,
  new: `source/flying_whales_under.py` (water bands by direction, the surface from below, light shafts, specks,
  bubbles, the fish shoal), drawn for `flying_whales_opener.camera(t)`; benchmark sheet beside the refs (rule 3) and
  a sheet to Sam; add it to `guides/kit-catalogue.md`; (3) the rig (`source/flying_whales_rig.py`, about 30 breakable
  parts, JACKDAW board, rig sheet on the sea painting using `flying_whales_sea.CAM`); then rehearsal clips: the
  opener's swing (1.2-4.0 s) and its rise into the cut (4.0-5.6 s), then the rig's three. Still to do: copy
  `source/satire_template.py` to `source/flying_whales.py` (no cast).
- **Tool gap:** `source/hook_text.py` can't draw colour emoji yet (the Hook Text has 🔥🔥🔥); Noto Color Emoji is
  installed; add it before the first animatic (small, Opus medium). It is placed with `--y 352` (the upper band) and
  stays on the whole video (`--until` the full length).
- **Losses and my additions Sam should know about:** additions (opener, all said yes): dusk light under the sea; the
  fish shoal; bubble trails on the rise; drifting specks. Earlier ones below. No losses.
- **Rule requests and proposals not yet in a guide:** none (searched this file).
- **Usage budget (rule 44):** 28% of the week (Sam, 1 Nov, end of the opener plan). Ask again at the next handover.
- **Files to open:** this file; `guides/satire.md`; `guides/film-quality-rules.md` 3, 8, 16, 22, 33, 39;
  `guides/kit-catalogue.md`; the docstrings of `source/flying_whales_opener.py`, `source/flying_whales_sea.py`,
  `source/whale.py`; the seven underwater refs (one combined sheet).

## Handover of 1 Nov (end of the whale build)
- **Rules that bite at this stage (rule 48):** 40 (build only what the approved Showstopper list says; tick it at
  the first clip); 8 and 33 (rehearsal clips of the risky moves before the rest: the first hits, the finale);
  32 (debris settles properly; here it falls into the sea and sinks, never floats or overlaps); 22 (any set
  dressing of mine shown on the sheet and named); 34 (mirror test before the whale sheet goes out).
- **Done (1 Nov, planning, Opus):** 34 references filed (`references/flying-whales/`); brief checklist; Showstopper
  list (16 items, sent to Sam; he asked no trims); ambition estimate about a third of a week; rough composition sheet
  sent (`review/flying-whales-composition.jpg`); Sam's answers in (see Decisions). Sam turned DOWN the cost-saving
  package: build everything as planned (whale from every view, rig in about 30 parts, lifeboats and crane whip kept,
  three rehearsal clips).
- **Done (1 Nov, building, Opus): the humpback** (`source/whale.py`, in `guides/kit-catalogue.md`; size in
  `source/sizes.py`). One model in metres drawn flat in the house style, so it works from any view and size (rule 39:
  seen from 3+ angles and in the prior scene, so a model, like the Roadster). Side, rear three-quarter, below, above,
  front three-quarter, head on; five patterns from ref whale-patterns-below (1 Inky, 2 Blaze, 3 Freckle, 4 Bib,
  5 Ghost; sizes x0.95-1.06); flipper wave, tail beat, climb, dive, arch, blow spray. Line check clean on all five
  (`whale.py check`); mirror test done (side view from its left has the nose to the left; from below its left is on
  screen right, as in the ref). Sheet sent: `review/flying-whales-whale-sheet.jpg`. Draw time about 0.4 s a whale at
  540 wide; a 12 s shot with five whales should render in under 10 minutes.
- **Next (fresh chat, Opus high; the rig is a new build):** Sam has not yet said yes to the whale sheet; his notes or yes come first (step 3). Then (same stage, Opus high): copy
  `source/satire_template.py` to `source/flying_whales.py` with no cast (step 1, held back: nothing needed it for the
  whale); the rig (`source/flying_whales_rig.py`): Jackdaw from the diagonal, about 30 breakable parts, JACKDAW name
  board; rig sheet beside a whale at real size (`whale.draw` with the film's camera). Then the dusk sky and sea, then
  the three rehearsal clips.
- **Losses and my additions Sam should know about:** additions listed below (whales fly on out of frame, a freeze on
  each contact, lifeboats and crane whip; the whale's slate blue-grey and the pattern names). No losses.
- **Rule requests and proposals not yet in a guide:** none (searched this file).
- **Usage budget (rule 44):** 24% of the week used at the end of the whale stage (Sam, 1 Nov). Ask again at the start of the rig chat.
- **Files to open:** this file; `guides/satire.md`; `guides/film-quality-rules.md` 8, 22, 32-34, 39, 40;
  `guides/kit-catalogue.md`; the references.



## Handover, 1 Nov (end of the sky-and-sea build; before the opener plan)
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

## Handover, 1 Nov (end of building: brows, underwater set, rig)
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
- **Usage budget (rule 44):** 31% of the week (Sam, 1 Nov, end of the build stage: brows, underwater set, rig took
  about 3%). Ask again at the next handover.
- **Files to open:** this file; `guides/satire.md` ("Render", "Before every render"); `guides/film-quality-rules.md`
  8, 15, 16, 29, 32, 33, 40; the docstrings of `source/flying_whales_opener.py`, `source/flying_whales_under.py`,
  `source/flying_whales_rig.py`, `source/flying_whales_sea.py`, `source/whale.py`; `source/satire_template.py`.
