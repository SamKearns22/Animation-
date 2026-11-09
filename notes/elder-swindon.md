# Elder Scrolls: Swindon (parody of the Elder Scrolls VI: Sentinel name-reveal teaser)

## Where things stand
- **Rules that bite next:** 56 (a fault of a kind: every mini, every sign), 59 (no animatic without a clean pre-flight; fix the hang), 67 (one full pre-flight per round).
- **Done:** animatic 1 sent; Sam's notes 1-11, then 12-18 (shot-6 people and vehicles, framing, the sign) saved below. A duplicate build from another chat merged out (see "More notes").
- **Spent against the estimate:** 6.0 of 9.0 (plus about 1.4 for notes 12-16 if Sam agrees).
- **Next:** Opus, medium effort, NEW chat: "Fix Elder Scrolls Swindon notes 1-18 – read notes/elder-swindon.md". Order: notes 1-18 in one round (clips first), the pre-flight hang, full pre-flight, check sheet, animatic 2 offer.
- **Needs Sam:** Y/N early evening (note 11); Y/N scroll glow (note 9); Y/N people drawn up to 4 times real size in shot 6; budget about 10.4%.
- **Read:** this file (Where things stand, Brief checklist, both "Notes on animatic 1" sections); guides/satire.md (Before every render, Render).
- **Lost / Added:** Lost: the CLOSING DOWN sign. Added: scroll glow, shopping bag, early evening (pending Y); people up to 4x size (pending Y).
- **Open rule requests:** none.
- **For Claude:** `source/elder_swindon.py` (cam_for, aerial_flat, _estate, traffic, title, burn, scene, checks); shot-6 extras to port in `source/elder_swindon_extras.py`. Animatic: `python3 source/elder_swindon.py final OUT.mp4 --small --no-lock`, then `source/finish.py`. Pre-flight hang: workers freeze after frame ~332; try `OMP_NUM_THREADS=1` and a worker-free run first.

## Plan (8 Nov, redone after Sam's answers)
**Length:** 30.04 s (the teaser's sound, as is) + the 1.6 s sign-off = 31.6 s. No voices.
**Looks:** the ground, light, dust, scroll, can, packet and litter near-real (soft depth of field, warm low sun, real textures):
a first for us (Strictly Crabs is the only near-real build so far). The man in our house style in every shot (Sam, Q3).
From the zoom-out on, everything flat house style.

**Shot list, timed to the sound's hits** (1.07, 2.49, 6.57, 7.37, 7.79, 11.43, 13.86, 15.08, 17.45, 19.86, 21.93, 24.76, 27.19)
| # | time (s) | shot | teaser beat it copies |
|---|---|---|---|
Teaser stills (Sam's recordings, 8 Nov): the camera looks down on the sand the whole way (a ridge half in shadow, sand
streaming); gold glints show through from 7.4 s; the staff lies across the frame, fully out by about 14 s, its blue gem
flares gold arcs at 16.1 s; black at 16.5 s with gold rings blooming; "The Elder Scrolls VI" fades in 18.5-19.5 s with a
thin rule under it; "SENTINEL" burns in letter by letter with glowing edges 22-27 s and cools to dull bronze by 29 s.
Our camera looks down at a slant (70 degrees) in shots 1-3 so his face and the can read, and straight down from shot 4.

| 1 | 0.00-7.37 | Looking down at a slant, warm low sun, dust blowing in gusts (1.07, 2.49, 6.57). From the first frame: the half-buried EXPORT LAGER can in front, the man's splayed arm and limp hand behind it, cigarette butts and a ring-pull. The camera glides along the arm and reaches his drooling face by about 3.5 s; a gust blows dust over him as the drool drips (6.57). Hook Text 0.5 s to about 4 s | sand blowing |
| 2 | 7.37-13.86 | Just past his outstretched hand, a gust strips the soil off the scroll (7.37); the gold catches the sun (7.79); the camera glides along it, spiked tip, carved end cap, the case (11.43) | the staff appearing |
| 3 | 13.86-15.08 | The sandwich packet (EGG MAYO) tumbles end over end past the scroll | (staff, continued) |
| 4 | 15.08-16.50 | Straight down from 1.5 m: the man face down, the scroll by his hand, the can, the packet, litter, on the soil-and-grass patch | (staff, last shot) |
| 4b | 15.30-16.50 | (Sam, 8 Nov) A Staffordshire bull terrier charges in and clamps on his ankle, growling, tugging and shaking his leg; he stays out cold | |
| 5 | 16.50-17.45 | **Showstopper:** the camera rockets straight up to the whole Magic Roundabout, the dog still tugging as he shrinks away, traffic going round; lands on the 17.45 hit | the cut to black |
| 6 | 17.45-30.04 | From above, drifting slowly, traffic going round, to the end (Sam, Q4: no extra shots); the picture dims halfway (the teaser goes to black); gold rings bloom (17.45), "The Elder Scrolls VI" fades in (18.5-19.5), "SWINDON" burns in letter by letter (22-27) and cools (29) | rings, title, held |
| - | 30.04-31.64 | CranbriJoos sign-off | |

## Plan extras: ambition estimate (rules 24, 39, 54, 55, 62)
Sam's budget: **9% of a week**. Compared with MidTerminal (11%), Terfwarts (9%) and Ad-Vanced Notice (estimated 10%). No likeness,
no voices, no lip-sync; one new look. 3D only for the scroll (rule 39: the camera glides along it and the gold's shine must move).

| build or risky move | why (3D? parts the camera sees) | estimate (% of a week) | spent |
|---|---|---|---|
| Near-real ground: soil, patchy grass, stones, cigarette butts, ring-pull, wind-blown dust, warm low sun, depth of field | new look, shots 1-4; started in the composition sheet | 1.4 | 0.4 |
| The Elder Scroll, near-real gold (spiked tips, dark wrapped grips, carved end caps, the case); soil blowing off it | 3D: the camera glides along it and the shine must move; started in the sheet | 1.0 | 0.2 |
| Lager can (dented, half buried), sandwich packet (tumbles) | new props, can as the scroll, packet flat | 0.5 | 0.1 |
| The man in house style: lying.py face down; a new close-up of his face on its cheek (slack mouth, drool) | the kit's face reads poorly face down: the close-up is new | 0.9 | |
| The Staffie (Sam, 8 Nov): from above and at a slant, house style; charges in, clamps, tugs and shakes | new creature | 0.8 | 0.1 |
| The zoom-out: the camera swings to straight down and rises 1.5 m to about 200 m; near-real hands over to flat | Showstopper, risky move | 0.9 | |
| Magic Roundabout from above, flat painting (benchmark below), the soil-and-grass patch on the island, the estate | new set; rough in the sheet | 1.3 | 0.1 |
| Traffic: cars and a bus going round (clockwise round each mini, anticlockwise round the inner ring), giving way | new mover | 0.7 | |
| Title: dim, gold rings, small line, SWINDON burning in letter by letter | new effect; rough in the sheet | 0.5 | |
| Animatic rounds | | 1.0 | |
| **Total** | Sam's budget 9% | **9.0** | **0.9** |

Rehearsal clips first (rule 8): shot 2 (soil sliding off the scroll), shots 4b-5 (the dog and the zoom-out), shot 6 (traffic and the title burn).
Sound effects (rule 26): none; the teaser's sound as is (Sam, 8 Nov: for the animatic; how to treat it later is open). Bleeps: none.

## Showstopper elements (rule 40: approved by Sam, 8 Nov, Q9)
| # | element | how it moves |
|---|---|---|
| 1 | Straight down over the man, the scroll by his hand, the can, the packet, the Staffie on his ankle (Sam, 8 Nov) | the dog tugging and shaking; the climb starts slowly so the dog reads |
| 2 | The soil patch round them, then the island's soil-and-grass patch (Q2), the lamp post's shadow | shrinks away as the camera climbs |
| 3 | The inner ring, then the five mini roundabouts, the arms, the verges and the estate | come into frame as it climbs |
| 4 | Traffic going round | keeps going the whole time, never stops |
| 5 | The near-real look gives way to the flat house style | crossed while fastest (about 16.8-17.1 s) |
| 6 | The climb | slow start, fast middle, eases to a stop on the 17.45 hit |

## The world (rule 1) and benchmark (rule 3)
Benchmark for the Magic Roundabout (8 things that make it, from Sam's two photos):
1. One big central circle: dark paving, a white kerb ring, a tall lamp post in the middle with its long shadow.
2. Five mini roundabouts round it, each a white domed circle with a white ring.
3. Traffic: anticlockwise round the inner ring, clockwise round each mini; dozens of cars (white, black, silver, red, blue), a bus or lorry.
4. Dense white markings: dashed give-way lines, arrows, hatched areas.
5. Raised kerbed islands (long rounded blocks, dark paving) between the minis.
6. Zebra crossings on the approaches.
7. Grass verges with trees round the edges; five roads fanning out.
8. Round it: terraced streets (rows of brown and grey roofs, back gardens), a big white-roofed shed, a car park.
9. (Sam's three new photos, 8 Nov: `magic-roundabout-3-high`, `-4-stadium`, `-5-above`) The County Ground stadium next
   door (pitch, red seats, floodlights).
10. Grass and kerbed islands between the arms: the tarmac is the inner ring, the minis and the arms, not one big disc.

Composition sheet sent: 8 Nov, review/elder-swindon-composition.jpg (`python3 source/elder_swindon_comp.py comp OUT.jpg`; 4 key shots: can and hand with the Hook Text; his face and the scroll; the Staffie as the climb starts; the roundabout with SWINDON)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 1 | Copies the Sentinel teaser beat for beat, using its sound (`music/sentinel-teaser-audio.m4a`, 30 s) | yes: every cut on a hit of the sound (checked); sound as is, peak brought under full scale |
| 2 | Opening: wind over **soil and patchy grass** (not sand), moody and near-real | yes: shots 1-3, gusts on 1.07, 2.49, 6.57, 7.37 |
| 3 | Wind uncovers a golden **Elder Scroll** (keep it a scroll, not a sign); spiked tips, dark wrapped grips, carved end caps, case | yes: shot 2, stripped from 7.37, out by 13.5 |
| 4 | Nearby in the soil: a **discarded can of lager**, half buried | yes: shots 1-4 |
| 5 | A **half-unconscious man sprawled face down, drooling into the soil** | yes: face down; his face on its cheek in shot 1, drool, a drip on 6.57 |
| 6 | A **discarded supermarket sandwich packet** ("maybe", my pick: in) | yes: tumbles past the scroll (shot 3), lies there after |
| 7 | Where the teaser cuts to black: the camera **zooms right out** to the full **Magic Roundabout, Swindon**, traffic moving round it | yes: shot 5 (16.50-17.45), traffic from 16.9 to the end |
| 8 | Title burns in like the teaser: small "The Elder Scrolls VI", big "**SWINDON**" | yes: shot 6 |
| 9 | Our flat cartoon style for the roundabout; the opening as moody and realistic as possible | yes: near-real to 16.8 s, flat from 17.1 s |
| 10 | **The joke:** Swindon is drab, uninspired, full of chavs; every shot after the zoom-out sells that | partly: drab estate, a CLOSING DOWN roof, the drooler and the dog stay in the middle; people too small to read from up there (Sam, Q4: no extra shots) |
| 11 | **Hook Text:** "Elder Scrolls reveals new location!" (exact wording) | yes: `HOOK`, 0.5-4 s, y 1240 (below the can) |
| 12 | Hook Text and the CranbriJoos sign-off (finish.py), as on every film | yes: finish.py on the clean render |
| 13 | (Q2) A patch of soil and grass on the central island, where he lies; the rest of the island paved | yes |
| 14 | (Q3) The man in our usual house style | yes |
| 15 | (Q4) No extra shots after the title: the view from above holds to the end | yes: shot 6 drifts to 30.04 |
| 16 | (Q5) The can reads "EXPORT LAGER"; the packet "EGG MAYO" | yes: label rows moved clear of the buried end (was "RT LAGER") |
| 17 | (Q5) Lager can and splayed arm from the first frame; drooling face soon after | yes: face by 3.5 s |
| 18 | (Q6) Cigarette butts and a ring-pull in the soil | yes |
| 19 | (Q7) The teaser's warm low sun | yes: and its long shadows (the lamp post's crosses his legs) |
| 20 | (Q9) The zoom-out is the Showstopper Shot (elements as listed) | yes: all 6 (see the Showstopper table) |
| 21 | Budget 9% of a week | yes: see the estimate |
| 22 | Animatic: the trailer's sound as it is | yes |
| 23 | (Sam, 8 Nov) A Staffordshire bull terrier angrily attacking the guy's leg as we zoom out | yes: charges in 15.25, clamps 15.72, tugs and shakes to the end |
| 24 | (Sam, 8 Nov) SWINDON burns in letter by letter with a glowing edge, like SENTINEL | yes: 22-27 s, cools to bronze by 29 |
| 25 | (Sam, 8 Nov) The man stays out cold while the dog tugs (only his leg jerks) | yes |
| 26 | (Sam, 8 Nov) The Staffie is brindle (brown, darker stripes, white blaze) | yes |
| 27 | (Notes 1, 18) No CLOSING DOWN sign, no lettering on the building | yes: plain roof |
| 28 | (Note 2) Minis moved out onto the arms; traffic goes round each mini, not the main circle | yes: minis at 56 m (were 42); no car circles the island; cars go mini to next mini |
| 29 | (Note 3) Lamp post readable, its shadow shorter | yes: pole leaning out, double-armed head; shadow 14 m (was 47) |
| 30 | (Note 4) Shot 6 lighter, not dark so fast | yes: dims to 26% (was 55%) over 2.5 s (was 0.85) |
| 31 | (Note 5) "The Elder Scrolls VI" centre-aligned and grander | yes: centred on the frame, 66 px semibold (was 52), rule with diamond ends; SWINDON 132 px so it ends before x 900 |
| 32 | (Note 6) Arm flat on the ground (not curled up), a hoody, vomit nearby; an amalgam of the reference photos, no likeness | yes: arm laid out near straight; grey hoody with the hood down; sick by his face; general traits only (grey hoody, gingery stubble, crop) |
| 33 | (Sam, 8 Nov) "Make him just look like shit in general" | yes: sallow skin, blotchy red cheeks, eye bags, lines, stains on hoody and trackies |
| 34 | (Note 7) The climb slower; the dog attack held long enough to read | yes: climb 16.90-19.86 (was 16.50-17.45), lands on the 19.86 hit |
| 35 | (Note 8) Drool pinned to the mouth and the soil | yes: string from the mouth corner over the cheek to the pool, pool under the face's edge |
| 36 | (Note 9) Swirling magic light round the scroll | yes: gold wisps from 7.6 s, glowing, to the climb |
| 37 | (Note 10) A shopping bag overflowing with rubbish, north of the dog scene | yes: above his head in shot 4 |
| 38 | (Note 11) Early evening: low golden sun, longer shadows | yes: sun 15 deg (was 21), warmer light, bluer shade (lamp shadow kept short: note 3) |
| 39 | (Note 12) Shot 6: people walking on the paths and pavements | yes: pavements, the ring's pavement, a new footpath round the green |
| 40 | (Note 13) Shot 6: two groups of men scuffling on a path | yes: on the footpath, top left |
| 41 | (Note 14) Two hooded teenagers on e-bikes, far too fast, irresponsible | yes: the wrong way round inside the ring, weaving, 14 m/s |
| 42 | (Note 15) A food delivery moped, plain box | yes: one of the traffic, red, no logo |
| 43 | (Note 16) A burnt-out car on the green by the stadium | removed (Sam, animatic 3: it doesn't register) |
| 44 | (Note 17) Framing: the 19.83 s view moved north by 8% of the frame (blue line at the bottom) | yes: END_MY 60 -> 35.1 |
| 45 | (Animatic 2) No pink cheek blotches | yes |
| 46 | (Animatic 2) Shot 1: less time on his face | yes: face reached by 4.4, cut at 6.57 (about 2.5 s on it; was 3.9) |
| 47 | (Animatic 2) Shot 3 a few beats longer; the EGG MAYO packet lands near the scroll | yes: 11.43-15.08 (was 1.2 s, now 3.65 s); lands beside the scroll on the 13.86 hit |
| 48 | (Animatic 2) The dog shot a beat longer | yes: the climb starts 17.45 (was 16.90): 1.7 s of the dog clamped before it |
| 49 | (Animatic 2, and notes 2 before it) The roundabout as in Sam's photo and drone videos: minis inside one grey carriageway round the central island, splitter islands between them, cars on the road round the minis | yes: rebuilt from the video; every car checked on the road, every frame |
| 50 | (Animatic 3) Less greying out of the aerial | yes: dims to 10% (was 26%) |
| 51 | (Animatic 3) Lines in the housing so the terraces aren't one long block | yes: each house its own roof, tone varied, an alley every 7th, chimneys |
| 52 | (Animatic 3) Hold on the aerial view a few more seconds: 5 s more of the track (Sam's second recording) | yes: the film now 35.04 s (+1.6 sign-off); the recording starts at 0:41 of the video, where the first ends; joined with a 20 ms crossfade, faded over the last 0.8 s |
| 53 | (Sam, 9 Nov) Bikes a third smaller, smaller trails, a bit faster | yes: drawn at 2/3 the size, trails shorter and finer, 17 m/s (was 14) |
| 54 | (Sam, 9 Nov) More traffic | yes: 13 cars an arm (was 9), junction limit 14, mix 8: about 38 cars in view (was 28); checked clean |
| 55 | (Sam, 9 Nov) Walkers off the inner circle onto the outer, none next to the road | yes: walkers only on the footpath round the greens (lost: the pavement walkers) |
| 56 | (Sam, 9 Nov) Two women walking with a pram | yes: on the footpath, top right |
| 57 | (Sam, 9 Nov) Pigeons in the central circle | yes: a dozen on the island's paving, pecking |
| 58 | (Sam, 9 Nov) One white van driving like an absolute twat | yes: from 24.1 s: down the centre line past the queue, straight over the mini's dome, weaving inside the splitter, out flat out; never touches anything (`van_faults`) |
| 59 | (Animatic 4) Drool clipped in shots 3 and 4 | yes: from shot 2 the pool lies on the soil under him (drawn before his body); the strand stays on his cheek (shot 1's fix had never reached the other shots) |
| 60 | (Animatic 4) EGG MAYO backwards | yes: the front face was shown from behind; mirrored |
| 61 | (Animatic 4) The shopping bag and items too plain to identify | yes: carrier bag with a stripe and creases, lager can, crisp packet, chicken box with bones, pop bottle, banana skin, coffee cup |
| 62 | (Animatic 4) Pigeons in shots 2-4 so we know what they are from above; they popped in late on the zoom out | yes: four by him from shot 2 (one flies off as the packet lands), a dozen on the island, drawn through every camera and grown smoothly |
| 63 | (Sam, 9 Nov) Pigeon heads had no neck; poor shaping in shot 3; the neck stretch looked weird | yes: rebuilt after a critique (short fixed neck under the body and head, curved body, dark folded wings, feathered wingbeats, grey and eyeless when small); Sam: Y |

## The acting list (rule 74): no lines; every beat, the hit it lands on
| beat | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| can and splayed hand from frame one | DROOLER | 1, slant close: the joke from the start | - | arm flung out, hand limp | 0.0 |
| his drooling face | DROOLER | 1, close: the reveal of the sleeper | eyes shut, mouth hanging open, drool | still (out cold) | by 3.5 |
| a gust, drool drips | DROOLER | 1 | - | - | 6.57 |
| soil stripped off the scroll | SCROLL | 2, close: the teaser's staff | - | - | 7.37; glint 7.79; case 11.43 |
| packet tumbles past | PACKET | 3, wider: the scroll and the packet | - | end over end, lands label up | 13.86-14.95 |
| straight down: all of it | all | 4, from above: the teaser's last staff shot | - | - | 15.08 |
| the Staffie charges, clamps, tugs | STAFFIE | 4-6: angry, braced | eyes narrowed, ears back | legs dug in, head shaking | 15.25, 15.72 |
| his leg jerks with the tugs; he never wakes | DROOLER | 4-6 | - | only the left leg moves | from 15.72 |
| the climb | camera | 5: the Showstopper | - | - | starts 16.50, stops on 17.45 |
| rings, small title, SWINDON burns, cools | title | 6 | - | - | 17.45, 18.5, 22-27, 29 |

## Reference
- Teaser frames: sand blows (0-7 s), golden staff with a blue gem appears (7-15 s), black, gold rings, "The Elder Scrolls VI", "SENTINEL" burns in (15-30 s).
- Roundabout: `references/elder-swindon/magic-roundabout-1.jpg`, `-2.jpg` (one big circle in the middle, five mini roundabouts around it).

## Questions sent to Sam (8 Nov; my pick first) and his answers
1. Does the sound clip have the narrator ("A future lost. A victory undone...")? If Y, the can lands on "A future lost" and the man on "A victory undone".
2. Where the man lies: the real central island is dark paving with a lamp post, not grass. 1 = the island turned into a scruffy patch of soil and grass round the lamp post (a small liberty, so he is dead centre); 2 = a grass verge by a mini roundabout.
3. The man in the near-real shots: 1 = only close parts (cheek in the soil, half-open eye, drool, a limp hand), the whole man (flat, face down, grey tracksuit) seen in the zoom-out; 2 = his whole face near-real (risky).
4. After the title: 1 = aerial with the title to 24.8 s, then two ground-level shots (lads on a moped and a lowered hatchback round a mini; a man in a tracksuit walking a Staffie past the drooler on the island); 2 = the aerial held to the end (3% cheaper; people too small to read from above).
5. The can: 1 = invented brand, "SUPER STRENGTH LAGER 9%"; 2 = plain "EXPORT LAGER". Packet: an invented meal-deal "EGG MAYO".
6. A smirk before 5 s (TikTok rule): 1 = cigarette butts and a ring-pull in the soil in shot 1; 2 = shot 1 kept pure teaser.
7. Light: 1 = the teaser's warm low sun, so it looks real until the reveal; 2 = grey British overcast.
8. Teaser screenshots (YouTube is blocked for me): 4 of them (blowing sand, the staff, the gold rings, the finished title)? Y = you send them; N = I copy your description.
9. The zoom-out as the Showstopper Shot, its 6 elements as listed: Y/N.

Sam's answers (8 Nov): 1 unsure; 2 a soil-and-grass patch on the island, the rest as in the photos; 3 our usual house style;
4 N (no extra shots); 5 EXPORT LAGER, and a joke from the start (can and splayed arm from frame one, face soon after);
6 add them; 7 yes; 8 take stills from the video he sent (only the sound was filed: asked for the recordings again); 9 yes.
Budget 9%. Audio for the animatic: the trailer's sound as it is.

Composition-sheet questions (8 Nov; my pick first). Sam: "Y to all" (1 Y, 2 Y, 3 brindle); no notes on the sheet.
1. The title: SWINDON burns in letter by letter with a glowing edge, as the teaser's SENTINEL does (a glow is outside our house style, like Cortana's). Y/N
2. The man stays out cold while the dog tugs (only his leg jerks). Y/N
3. The Staffie: 1 = brindle (brown, darker stripes, white blaze); 2 = blue-grey.

## Sound for the final (Sam, 8 Nov: "how do we manage the audio?")
The trailer's own recording is what TikTok's automatic matching listens for: any copy of it (cut, sped up, pitched)
is still that recording, and making a copy slip past the matcher is not something I'll do. Proposed, my pick first:
1. **Our own score, built on the same hits** (wind and a low drone; a swell and a bell on the glint, 7.79; deep booms
   on each hit; a big hit as the camera stops, 17.45; a choir-like pad under the title; a metallic shimmer as
   SWINDON burns; the last boom 27.19). Original notes, no tune copied, so nothing to match. About 0.6% of a week
   (the Yuletide trailer's score tool, `horror_trailer_music.py`, as the start).
2. Post with our score, and in the TikTok app swap in the official teaser sound from TikTok's own library, if it is
   there (TikTok licenses its library for use on TikTok): only on TikTok, and lined up by hand on the phone.
3. Keep the trailer's sound in the file: likely muted or blocked by the automatic check.
The animatic keeps the trailer's sound as it is (Sam, 8 Nov) for the timing.

## Decisions (build, 8 Nov)
- 24 frames a second (not the satire 12): the slow glides judder at 12 (as Flying Whales).
- Grass blades live in the world (were re-scattered on screen each frame: they would have shimmered once the camera moved).
- His face in the close shots: the house-style head laid on its cheek over the body (lying.draw's face read poorly face down).
- Shot 2 looks at the scroll from the side, so it lies across the frame as the teaser's staff does.
- The packet comes to rest past the scroll's tip (the wind blows that way); it was by his side on the composition sheet.
- The can's words on two rows near its top end (the buried end cut "EXPORT" to "RT").
- The lamp post's long shadow (low sun) crosses his legs in shot 4 and leads the eye in the climb.
- The roundabout redrawn from Sam's three new photos: grass and kerbed islands between the arms, terraced streets,
  a white-roofed shed (CLOSING DOWN on its roof, inside TikTok's safe area), a car park, the County Ground.
- The title moved left to the middle of TikTok's safe area and made smaller (SWINDON ran under the buttons).
- The dog's charge starts 1.5 m out (it came from 2.3 m and was on screen for only a few frames before it bit).
- Shot 6 is 12.6 s, over pre-flight's 8 s: chosen (Sam, Q4: no extra shots). Named to Sam.
- The trailer's peaks went over full scale by 1.1 dB: brought just under (nothing else changed).
- Pre-flight keeps each drawn frame (`~/.cache/filmcache/elder_swindon-memo/`, keyed by the code): the checks and the
  small animatic share it. Nothing in this film draws through the people checks (no views or burnham people).
- Pre-flight hung twice (8 Nov, 15:47 and before): its four workers locked up after frames 180-332, idle for an
  hour. Sam: "Skip the checks. Proceed to animatic." The quick check (--text) was clean but for shot 6's length;
  the animatic rendered with `--no-lock`. Before the final: find the hang (workers waiting on a pool lock, the parent
  holding OpenMP threads) and run pre-flight in full.

## Decisions (round 1 fixes, 8 Nov: notes 1-18)
- Note 2 read as: the minis sit out on the arms (centre 56 m from the middle, the ring's tarmac to 49 m), and no car
  circles the central island. Cars go: in along an arm, round its mini, along the ring to the NEXT mini, round it,
  out. Rules added so they never jam or pass through each other: at most 10 cars past the give-way lines; cars from
  the ring give way to cars already on a mini; arm cars wait while anything is on or coming to their mini; a slower
  car lets a faster crossing one go. Traffic runs in from -30 s so the minis are busy from the start.
- Note 3 vs note 11: the evening sun would lengthen shadows, but the lamp's shadow is kept short (14 m) as Sam asked.
- Note 7: the climb now 16.90-19.86 (lands on the 19.86 hit); the rings bloom as it lands (were 17.45, mid-climb
  now); the small title fades in 20.3-21.3; SWINDON unchanged (22-27). Shots: 4 to 16.90, 5 to 19.86, 6 to the end
  (10.2 s, over pre-flight's 8 s: Sam's Q4).
- Note 17: the view's centre moved north by 8% of 1920 px at 168 m wide (23.9 m); the title moved down to fit under
  the roundabout (TITLE_Y 1330).
- Note 6 and Sam's photos (re-sent 8 Nov): general traits only (grey hoody, gingery stubble, short crop); the face is
  the house-style head, nobody's likeness. Sam: "make him look like shit": sallow skin, blotchy cheeks, eye bags,
  lines, stains (sick, lager, mud) fixed to his joints.
- The opening camera nudged towards his hand (the arm now lies further out) so his face stays out of shot until the
  glide reaches it; the Hook Text moved to y 1265, x 600 (the can glides through where it was).
- People from above drawn up to 4x real size, mopeds 2x: Sam said Y (8 Nov). Budget raised to about 10.4% of a week: Sam said Y.
- Pre-flight hang found and fixed (8 Nov): linecheck loaded GNU OpenMP into the main process, so the drawing workers forked
  after it froze. linecheck, landmarks and sizes now run in a forked child (`_in_child` in `source/preflight.py`).

## Notes on animatic 2 (Sam, 8-9 Nov) and why the roundabout failed twice
Notes: no cheek blotches; minis inside the grey; shot 1 shorter on the face; shot 3 longer, packet landing by the
scroll; the dog shot a beat longer; the roundabout (third time) with the cars on the pavements. Sam sent his aerial
photo again and two drone videos.
Why it failed: note 2 ("move them further in, onto the arms") was read as moving the minis OUT along the arms, and
neither fix was checked side by side with the photo; nothing checked that cars stay on the road, so cars cut across
the pavement corners where the arms met the ring. Fixed: the layout rebuilt from the video frame (minis at 35 m round a
15 m island inside one 46 m grey, splitters between), routes A (clockwise to the next mini, outside the splitters) and
B (anticlockwise to the mini before, inside them), and `traffic_faults` now fails any car corner off the road.
Rule 84 written (Sam: Y, 9 Nov): a real place is compared side by side with its reference on the check sheet before every animatic. Animatic 3 sent 9 Nov. Animatic 4 sent 9 Nov (36.6 s, the extra track, the van). Animatic 5 sent 9 Nov.

## Notes on animatic 1 (Sam, 8 Nov) — a round, to fix once the model is Opus
1. Remove the CLOSING DOWN sign on the building (Lost: the sign; it doesn't support the joke).
2. The exterior roundabouts sit on the junctions; move them further in, onto the arms. Traffic goes round each mini, not the main circle.
3. The central lamp post is not clear, yet its shadow is huge: make the pole readable, shorten the shadow.
4. Swindon from above goes too dark too quickly: lighter grade.
5. "The Elder Scrolls VI" title: centre-aligned and grander in size.
6. The drunk man looks asleep. His arm is curled off the ground. Give him a hoody and vomit nearby. Two reference photos are for inspiration only: no realistic likeness of either person. (Not copying the faces; a mugshot-style photo of a real person is not a model for a mocked character.)
7. The zoom up from below is too fast; hold the dog attack long enough to read.
8. The drool floats up from the ground and clips through his face: pin it to the mouth and the soil.
9. Give the scroll swirling magic light, as in the trailer (added: a glow, an exception to the house style; pending Y).
10. Added: a shopping bag overflowing with trash, north of the dog scene.
11. Make it early evening (added: low golden sun, longer shadows; pending Y).

## More notes on animatic 1 (Sam, 8 Nov, later chat) — same round
12. Shot 6: foot traffic: people walking on the paths and pavements.
13. Shot 6: two groups of men in a scuffle / fist fight on one of the paths.
14. Shot 6: two teenagers in hoodies on e-bikes, far too fast, riding irresponsibly.
15. Shot 6: a food delivery moped (plain box, no brand).
16. Shot 6: a burnt-out car on the green by the stadium.
17. Shot 6 framing: keep the animatic's angle (19.83 s, `references/elder-swindon/shot6-framing-sam.jpg`), only move the
    view so Sam's blue line (about 92% down the frame, across the stadium's pitch) becomes the bottom of the screen:
    the camera moves north by about 8% of the frame height. Everything else in the angle unchanged.
18. Remove the lettering on the building (the same as note 1: the CLOSING DOWN sign).
How: people and bikes from above drawn up to 4 times real size so they read on a phone (a liberty; tell Sam); walkers,
the fight, e-bikes, moped and burnt-out car are already written for another roundabout in `source/elder_swindon_extras.py`
(`person`, `fight`, `ebike`, `moped`, `burnt_car`, `walkers`): port them onto this film's `aerial_flat`, re-placing
paths and positions on this film's roundabout. Cost: about 1.4% of a week (budget 9 -> about 10.4; ask Sam).
Why a duplicate build happened (8 Nov): a later chat started from the main line, which did not have this branch's work
(`claude/wizardly-goodall-lvk9mb` was never merged back), and rebuilt the roundabout and title; that work is set aside
(only the extras file is kept). Merged 8 Nov.
