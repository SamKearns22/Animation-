# Kit catalogue: everything already built, to reuse before building (rule 28)

Check here first when planning a film. Each line: what it is, its file, and how far it reuses. A film that builds a new
set, person, prop or effect adds it here when its building stage ends, and to `source/catalogue.py`'s list (one line:
section, name, file, how to draw it). See the lot on one sheet: `python3 source/catalogue.py OUT.jpg [Sets People
Creatures Props Effects]` (about 30 s; each tile from its film's own picture, cast sheet or prop code).

## Sets (each built once in 3D, metres, y up; every shot is a camera on it)
| set | file | see it | notes |
|---|---|---|---|
| Any plan's rooms (shared): floors, walls with real openings, the next room through every doorway and window (portal), every thing as a block | `source/sets.py` (the camera and shapes every set uses) | `python3 source/sets.py FILM sketch OUT.jpg` | blocks out a new film's rooms from its `PLAN` for the composition sheet; hands walls, frames, doors and things to the audit |
| London house: living room (green carpet, panelled walls, sofa, TV, drinks cabinet, armchair, grand window), kitchen (island, slate worktops, sink run, window), hallway, gardens | `source/prepper_set.py` (plan: `prepper_plan.py`) | `python3 source/prepper_set.py test OUT.jpg` | walls with real openings, doors that swing, glass that breaks, marks that stay; walls and furniture as collision solids |
| Trafalgar Square (column, lions, fountains, gallery steps), TSG van, interrogation room, custody corridor | `source/power_crime_set.py` | its film's `stills` | crowd seating, banners |
| Casino parlour (oval poker table, panelled walls, chandeliers, armchairs) | `source/poker_mon_room.py` | its film's `stills` | table things from one `THINGS` plan |
| Round Table (The Traitors) | `source/traitors.py` | `traitors.py stills` | slates on stands |
| Hangar and space shots (Roadster) | `source/roadster.py` | `roadster.py cast` | space in Dam's coloured pencil |
| Space, flat cartoon (Halo No-No): planet (bands, dusk and night side, any light direction), the Halo ring small and tilted, the blue galaxy band, nebula, stars; the Halo ring close-up (a true circle projected through `RingCam`: hull panels, ports, lights; the far side's seas, land, cloud) | `source/halo_sets.py` (`space_wide`, `ring_close`, `_planet`, `galaxy_band`, `RingCam`, `ring_point`) | `python3 source/halo_sets.py sheet OUT.jpg` | paintings, rule 39; anything flown along the ring: `halo_no_no._ring_view` (a roadster.View on the ring's axes) |
| Tesla Roadster cabin from the windscreen facing back (white sport seats with ROADSTER plates, glass roof, rear window onto space, red trim, dash) | `source/halo_sets.py` (`cabin_back`, `cabin_front`, `cam_wide`, `cam_close`) | same sheet | one painting, two framings; space through every window; a car drifting past the rear window (`drift`) |
| Israeli TV news studio (invented channel): round floor graphic, huge curved ring desk, mesh chairs, tall swirl screen, navy LED walls, red-edged pillars, newsroom through glass, lighting grid, studio camera | `source/newsdesk_set.py` | `python3 source/newsdesk_set.py test OUT.jpg` | any camera; `render(img, cam, people)`, `put_seated` for anyone at the desk; four cameras in `CAMS`; Hebrew captions only, no real broadcaster |
| Oval Office (gold drapes, blue carpet; MidTerminal): an oval room in metres, three windows onto the garden under a gold swag valance, the Resolute desk with phones, tufted leather chair, photo table, US and President's flags, two gold-seat chairs, deep blue carpet with flower border and the seal, white fireplace with portrait, two shelved alcoves, four pedimented doors, portraits over side tables with busts, cream sofas, flowers table, yellow armchairs, grandfather clock | `source/midterminal_set.py` (`render(img, cam, people)`, `put`, `put_seated`, `wp(a, y)` for any wall point, `CAMS`) | `python3 source/midterminal_set.py test OUT.jpg` | any camera, about 0.5 s a frame; a big floor picture in tiles (`paste_tiled`) draws even with the camera over it |
| Oval Office moves (MidTerminal): a door that swings open onto a corridor and slams with a bounce; someone walking in through a doorway (clipped by the frame while behind the wall), turning front-on at their mark; floating with a bob and a slow wing beat; a see-through hellfire ghost with a flame tail that fades in and out and melts into a flaming skull | `source/midterminal_moves.py` (`door_items`, `door_curve`, `trump_item`, `satan_item`, `epstein_item`, `flames`, `skull`) | `python3 source/midterminal_moves.py sheet OUT.jpg`, `reel OUT.mp4` | about 0.4 s a frame |
| Dusk sky and sea, flat house style, for one locked camera 8 m above the sea (Flying Whales): purple-to-orange sky bands swelling over a just-set sun, clouds lit from below, the sea mirroring the bands, ripple strokes on a slow swell, a glitter path that twinkles, low wave caps in front; `glow()` turns the sea orange under any fire | `source/flying_whales_sea.py` (`paint(t, glows)`, `CAM`, `sea_z`, `horizon_y`, `DUSK_TINT` for whales) | `python3 source/flying_whales_sea.py sheet OUT.jpg`, `reel OUT.mp4 --small` | baked once, about 0.2 s a frame; shake is a shift of the finished frame |
| Open water under the sea at dusk, painted by view direction for ANY moving camera (Flying Whales opener): flat bands deep navy to bright blue with hand-cut edges, a warm glow dome on the sun's side, the surface from below (ripple shapes fixed on the water, the gold window overhead, a hard far edge), swaying light shafts, drifting specks, bubble streams from given points, a fish shoal that scatters from given bodies, `haze(d)` distance fade | `source/flying_whales_under.py` (`compose(cam, t, sprites, blowhole, since, pod_key)`, `set_pod`, `water`, `HAZE`) | `python3 source/flying_whales_under.py sheet OUT.jpg`; `python3 source/benchmark.py flying_whales_under OUT.jpg` | about 1 s a frame at full size (2 s with `ss=2`) |
| Offshore oil rig (Jackdaw-style) in 31 breakable pieces at real size, painted flat through one locked camera: yellow jacket legs and X bracing, three deck storeys each in two halves (open cellar with pipes and lifeboats, clad mezzanine with the JACKDAW board, top deck with lit windows), crane, derrick, stacks, modules, stair tower, helideck on its truss with the orange chute, walkway stub, flare boom with a flickering flame, foam at the legs. A piece moved by `xf` is repainted in perspective; anything below the sea is cut off | `source/flying_whales_rig.py` (`draw(base, t, xf, gone, extra)`: `extra` sorts other sprites (whales) in among the pieces by distance; `PARTS`, `PARENT`, `part_box`, `rot`, `FLARE_TIP`, `flame`, `foam`) | `python3 source/flying_whales_rig.py sheet OUT.jpg` (whole, numbered pieces, a break test, close-up); `check` (line check) | about 8 s to paint the whole rig once, then cached; a moved piece about 0.2 s |
| Flight paths for flying creatures in metres, for one locked camera (Flying Whales rig scene): smooth curves through waypoints, the key moments (surfacing, each hit) pinned to times, speed changing evenly between pins and checked never to drop into a hit; the pose follows the path and banks by the pull of the turn (upside down over a loop); a hit test lists every rig piece each body touches, and when, against a planned list | `source/flying_whales_paths.py` (`KEYS`, `HITS`, `KNOCK_ONS`, `pos`, `vel`, `pose`, `span`, `SURFACE`, `contacts`) | `python3 source/flying_whales_paths.py sheet OUT.jpg` (the paths through the camera and from above, with times), `speeds`, `contacts` | instant; the hit test about 2 s |
| Water burst when a big body breaks the surface, flat house style, in metres through any camera: a froth collar hiding the waterline cut, a column of water thrown up in smooth streaks that fall back as stubby drops, a foam ring on the sea that breaks into floating clumps (never fades); front and back layers so it wraps the body. Pairs with `whale.draw(cut_z=0)` (the body hidden below the sea) | `source/flying_whales_fx.py` (`burst_parts`, `draw_lumps`, `foam_ring`, `draw_foam`, `test_draw` for EFFECTS) | `python3 source/flying_whales_fx.py sheet OUT.jpg` (six ages) | about 0.3 s a burst a frame |
| Fire, smoke and water effects, flat house style, in metres through any camera, each a cropped sprite (fast): a tall lumpy fireball (dark red edge, orange, a yellow core that burns down first, gone in 1 s); smoke, steam and dust as separate clumps each with its own outline, rising and drifting with the wind, never fading (`Puff`); fire tongues leaning with the wind out of a hole; splashes of any size from a falling bit to a crown (a ring of drops, a mound at the foot, a column falling back); flying chunks in any colours; a ragged hole torn in any flat face (spot items, with embers) | `source/flying_whales_fx.py` (`fireball_sprite`, `Puff` + `puffs_sprite`, `fire_sprite`, `splash_parts` + `lumps_sprite`, `chunk_poly` + `pieces_sprite`, `hole_items`, `shape_sprite`; `test_draw(age, what)` for EFFECTS) | `python3 -c` with `test_draw` (each effect alone) | a few ms each |
| A structure wrecked piece by piece (Flying Whales rig): each hit from the hitters' paths knocks pieces loose (thrown the way the hitter went, tumbling, falling, splashing into the sea and sinking under the waterline, never standing on an end), holes others, bends others; pieces ride what they hang on; the whole thing tips and slides under; a 2-frame freeze and a camera jolt on each hit; every effect timed from the hits | `source/flying_whales_wreck.py` (`story`, `rig_state`, `effects`, `shake`, `shift`, `Fall`, `check`) with `flying_whales_rig.draw(swap=...)` | `python3 source/flying_whales_wreck.py table` / `check` | worked out once at start (1.5 s); about 5 s a full-size frame with everything |
| Bunker embrasure with the crew: inside, from the beach, side section; beach backdrop (sea, craft, hedgehogs) | `source/patriots3_bunker.py` (`Crew`, `inside`, `outside`, `side`, `beach_layer`) | | |
| WW2 concrete casemate inside (raw concrete with formwork joints, ribbed steel ceiling, steel door frame, cable run, caged lamp, crates, range card, field telephone, spent cases), the passage behind, the beach or a trench through the openings; the slit's reveal round a lens inside it | `source/patriots3_room.py` (`draw`, `painter`, `foreground`) | | |
| The Normandy coast from the air, painted in moving layers: cliff-face casemates and MG pits firing (tracers, bullets walking across the water), textured black cliffs, shingle, rippled sand, scorched craters, wire, mined stakes, hedgehogs, steel gates, swell and surf, six LCVPs on their own headings with rippling wakes, three kinds of shell burst as soft billows, warships with barrage balloons, a rocket salvo, P-47s with invasion stripes | `source/patriots3_coast.py` (`picture`, `burst`, `craft`) | | |

## People (satire package, `views.person`: any angle; circle hands)
| who | file | notes |
|---|---|---|
| Satan (original: black suit, red tie, red eyes, curved horns, red wings that spread 0-1), Jeffrey Epstein (measured likeness: grey swept hair, dark short-sleeved polo), Donald Trump (rebuilt from measurements, 4 Nov; the Traitors head failed the check) | `source/midterminal_cast.py` (`SATAN`, `EPSTEIN`, `TRUMP`) | every view; moods; `sheet`, `faces`, `head WHO OUT.png`; short sleeves (`short_sleeve=True`) for anyone |
| Andy Burnham (Hope Again; Prepper's white shirt, chinos, belt with Glock) | `source/burnham.py` (`BURNHAM`), `source/prepper_cast.py` | fear levels 1-6 (`FEAR`) |
| Wes Streeting (likeness, torn suit) | `source/prepper_cast.py` (also Hope Again's in `burnham.py`) | |
| Hope Again cabinet (Streeting, Rayner, Healey, Mahmood, Miliband; armour) | `source/burnham.py` | |
| Trump, Putin, Zelensky, Claudia | `source/traitors_cast.py` | likeness heads (that Claudia scored 35% on the likeness check, 1 Nov: use Patriots 4's) |
| The Traitors winner's room (pointed arch, lattice, panelled walls, fire baskets, torches, candles; round table, gold coin pile) painted all round, with a camera that turns on the spot (`PanCam`) | `source/patriots4_room.py` | 2D panorama; sheet: `patriots4_room.py OUT.jpg` |
| A real-camera wide view of that room (pinhole in the plan's metres): people placed at their plan marks at true sizes, a round table and coin pile in true perspective, the painted room behind turned for the camera's offset; a body turned to the table with the face to the lens | `source/patriots4_wide.py` | `patriots4_wide.py OUT.jpg [T]` |
| Romesh Ranganathan, Sebastian "Bash" Croft, Claudia (measured head; black jacket, cream tie blouse, gold chain) | `source/patriots4_cast.py` | likeness heads drawn from `likeness.py` measurements (`layout`, `Face`): a new famous face = its measures in `MEASURED`, its own hair; `head WHO OUT.png [--average]`, `likeness OUT_DIR`; sheet: `patriots4_cast.py sheet OUT.jpg`. Also the Patriot's stare strengths 1-6 and narrowed eyes (`patriot_eyes`) |
| Reform HQ five (Shocking Behaviour) | `source/shocking_cast.py` | likeness heads |
| Benjamin Netanyahu (navy suit, blue or red tie, flag pin) | `source/netanyahu_cast.py` | likeness head; moods incl. shouting; sheet: `netanyahu_cast.py sheet OUT.jpg` |
| Old lady with placard, Met officers (hi-vis, senior officer, armed), protest crowd | `source/power_crime_cast.py` | crowds of 2,000 |
| Poker players, dealer, guards, onlookers | `source/poker_mon_cast.py` | |
| Press secretary and reporters (crowd from behind) | `source/press_secretary.py` | `reporter` |
| Matt Damon | `source/roadster.py` | |
| Elon Musk in Master Chief's Mark V armour, seated at the Roadster yoke (face through a see-through gold visor; yoke turned; glance) | `source/halo_cast.py` (`chief`, `musk_face`, `yoke`) | front on, seated; sheet: `halo_cast.py sheet OUT.jpg` |
| Anime Cortana as a flat hologram (see-through blue, scan lines, slight glow: Sam's exception; forms out of a discharge) | `source/halo_cast.py` (`cortana`, `hologram`; poses appear, point, kawaii, thrust (side), turn (back), stand) | discharge flash and pixel crackle: `halo_no_no.discharge` |
| Darth Maul (black hooded cloak, hood up or down; painted face, horns) with the double-bladed red lightsaber | `source/maul_cast.py` (`MAUL`, `MAUL_HOOD`, `saberstaff`, `pose`) | every view; moods 'neutral' (glare), 'snarl' + talking; poses 'stand', 'present', 'attack', 'strike'; sheet: `maul_cast.py sheet OUT.jpg` |
| News presenter (original man, Israeli evening-news type: navy suit, tortoiseshell glasses, cropped beard, clip mic) | `source/newsdesk_cast.py` (`PRESENTER`) | every view; moods 'neutral', 'grave', 'smile' + shared; sheet: `newsdesk_cast.py sheet OUT.jpg` |
| Anyone lying down (face down, on the back, curled on the side, slumped against a wall) or seen from a high camera | `source/lying.py` | 3D body from the person's own design; `lie`, `draw`, `fall`, `stand`; sheet: `python3 source/lying.py sheet OUT.jpg` |
| The Patriot (balaclava, PP badges) rebuilt on views.person: every view, faces | `source/patriots3_cast.py` (`PATRIOT`) | |
| German WW2 soldiers, June 1944: Gunner and Loader (M40 helmet, tunic, Y-straps, belt kit, boots or gaiters) | `source/patriots3_cast.py` (`GUNNER`, `LOADER`; `stahlhelm`, `tunic`, `kit`) | |

## Creatures and machines
| what | file | notes |
|---|---|---|
| Chrome Centurion robot (3D: blade arm or cannon palm, sweeping eye, walks, falls, loses head or arm, explodes, dents) | `source/prepper_robot.py` | |
| Horse to ride, side-on (bay, chestnut, grey, black, palomino; also pony and donkey): stand, walk, trot, canter, gallop, either direction, with any satire person riding (sits, rising trot, up off the saddle at the gallop; reins, stirrups) | `source/mounts.py` | `python3 source/mounts.py reel OUT.mp4`; checks: `mounts.py check` (hooves never slide, no leg stretches, rider reaches). Side view only so far |
| Dragonite | `source/poker_mon_cast.py` | |
| Tesla Roadster (every angle) | `source/roadster.py` | |
| Crabs (Strictly Crabs) | `source/strictly_crabs_*.py` | realistic, not house style |
| Humpback whale (one model in metres, drawn flat in house style from ANY view and size: side, behind, below, above, head on; five belly and fluke patterns, each its own size; flippers wave, tail beats, climb, dive, arch, blow spray). Real size 14 m | `source/whale.py` (`draw(cam, pose, pattern, t, flap, beat, arch, blow, cut_z)` returns a Sprite to paste; `cut_z=0` hides everything below the sea with no outline along the cut; set `pose.R` directly (columns: nose, left, up) for any orientation; `Cam`, `Pose`, `view_cam`) | `python3 source/whale.py sheet OUT.jpg`, `moves OUT.jpg`, `reel OUT.mp4 --small`; `whale.py check` runs the line check on all five. Flying Whales, 1 Nov; the heavy cross brow and small white eye on by default (`brow=False` for a calm whale) |

## Props (real sizes in `source/sizes.py`)
| what | file |
|---|---|
| Crossbow (3D, flight roll), Glock, oily machete, minigun with ammo belt, tin of beans | `source/prepper_cast.py`, `source/prepper_fx.py` |
| Tins, 2 L bottles, Alexa (whole, smashed, on rod legs with a knife), crossbow bolt, mug on coaster with steam | `source/prepper_fx.py` |
| Poker Mon cards, chips (stacks topple), drinks | `source/poker_mon_cast.py` |
| Placards, banners | `source/power_crime_cast.py` |
| Slates on stands | `source/traitors_cast.py` |
| Chopping board, glazed ham, cleaver (horror trailer) | `source/props.py` |
| Double-bladed lightsaber (either blade on or off, turns with the hand in 3D, flat house-style blades) | `source/maul_cast.py` (`saberstaff`) |
| Curved-back wooden armchair (3D, any angle), blue spotlight pool and shadow | `source/newsdesk_props.py` (`round_chair`, `pool`, `shadow`) |
| MG42 as a 3D solid (any angle), ammo belt, ammo box, firing flash and recoil, falling cases | `source/patriots3_cast.py` (`Gun`, `draw_mg42`, `draw_belt`, `draw_box`, `cases`) |
| Remembrance poppy on a jacket | `source/patriots3_cast.py` (`poppy`) |

## Effects (house style: flat, lumpy, one frame for flashes; no stars, no glows)
| what | file |
|---|---|
| Lumpy flash, muzzle flash, sparks, debris that lands and stays, flat smoke, plasma bolt and scorch, tracers, blade trail, glass bursts, room flash, goopy beans, bullet holes on real surfaces | `source/prepper_fx.py`, `source/prepper_cast.py` |
| Hyper beam (soft glow: Poker Mon only, Sam's exception) | `source/poker_mon_room.py` |
| Thrown things under gravity (bounce, stay) | Poker Mon's `launch` |
| Cut-off body pieces that fall, settle and lie as a 3D pile | `source/lying.py` |
| Hook Text beside a person, three rows (`--w`); 😅 emoji | `source/hook_text.py`, `1f605.png` |
| Story post still (Maul close-up, cranberry lettering) | `animations/maul-icc-story.png` |
| A shell bursting on a bunker's slit: flash, black smoke outside, dust puffs rolling in (drawn in depth order), grit from the ceiling, concrete chips that land apart and stay, the bite left in the lintel, camera shake | `source/patriots3_fx.py` |

## Movement and checks (the kit tools)
`views.py`, `moves.py`, `stage.py`, `filmkit.py`, `perform.py`, `audit.py`, `clipcheck.py`, `voices.py`: see
`guides/satire.md` (Movement; Staging and acting) and `guides/figure-rig.md`. The film-quality checks (25 Oct):
`plan.py` (rule 1), `benchmark.py` (3), `sets.py` (2, 12), `kitchecks.py` (13), `viewchecks.py` (15-18, 20),
`report.py` (19), `catalogue.py` (28); pre-flight runs them all.

| what | file |
|---|---|
| A held 3D prop through any 3D camera with the holder's hands put on its grips where the camera sees them (screen point turned back into a hand target), and the MG42 drawn in true perspective (end on, beside the lens) | now in the kit: `source/held3d.py` (28 Oct); the film's own: `source/patriots3.py` (`hold_gun`, `draw_gun3d`) |
| The salute (an arm swung up round the shoulder in an arc), arms darting about (flapping, pointing round, finger wag), leaning in a doorway (figure tipped onto the post), thrown back against a wall, staggering backwards | `source/patriots3_act.py` (`salute`, `flapping`, `leaning`, `gunner`, `loader`); the salute, flapping and binoculars are now in the pose gallery |
| The pose gallery: arms folded, hands up, pointing, binoculars, salute, hands on a gun (rifle at port arms), flapping (up, pat), each tested from five views; one sheet | `source/posegallery.py`, `guides/pose-gallery.md`, `guides/pose-gallery.jpg` |
| A held 3D prop through the real camera: `through(cam)` (views.project as the camera), `body_point` (world point to hand target), `hold` (hands on the grips, the prop drawn with them, 'wrap' when it is nearer the lens) | `source/held3d.py` |
| A flat person's place through a 3D camera, the tilt measured at the arms' height (no sinking salute close up) | `source/lying.py` (`place`; `stand` uses it) |
| A head turned to its own side whichever way the body is drawn (a front-on body can look either way) | `source/views.py` (`Mirrored`, in `person`) |
| A camera that only turns (a push-in) never changes how people are drawn | `source/sets.py` (`Cam.yaw_of`) |
| The hand check (rule 41): every arm ends in a visible hand, every frame, every view; a check sheet | `source/handcheck.py` (pre-flight runs it) |
| The look check at the shot's own camera (rule 43): each face and its pupils measured as drawn; the sheet of eyes that meet | `source/filmkit.py` (`eyeline(aim=, drawn=, at=)`, `check_eyelines`, `look_sheet`); `views.Eyes` notes each pupil |
| One labelled contact sheet from any film in one command (rule 48) | `source/sheet.py FILM TIMES... [--crop] [--clean]` |
| `--nostamp` for a clip to splice into a final (rule 47) | `source/satire_template.py` (`final ... --nostamp`) |
| Each shared check tested against the fault that taught it (the old version put back, caught; the fix passes) | `source/kittests.py` |
| Pre-flight runs only the checks for what a film contains, and names the ones it skips (rule 58) | `source/preflight.py` (the film's `HAS`) |
| Nothing flips from in front to behind in one frame within a shot (rule 57) | `source/clipcheck.py` (`flip_faults`; the film's `draw_order(t)`, `ORDER_SWAPS`) |
| The render lock: no animatic or final without pre-flight's pass on the code as it is now (rule 59) | `source/film_engine.py` (`lock_fault`, `write_pass`; `--faults-named`) |
| The hiss check heard only between lines (rule 60) | `source/filmkit.py` (`hiss_check(voice=)`) |
| Subtitles from Sam's recordings: a few words at a time, each on the syllable it starts with, made readable when cut (0.8 s minimum, 220 words a minute, two rows); the template's `caption_at` uses it (rule 62) | `subtitles.py` (`line_caption`, `chunk_times`) |
| Running straight at the lens: the front-on gait (low knees, small float) with tucked, forward-pumping arms (rule 63); which poses read from behind (rule 64) | `moves.py` (`GAITS['front_run']`, `front_run_arms`, `READS_FROM_BEHIND`) |
| A mouth with no face to lip-sync (the Sorting Hat): openness 0-1 from the voice's loudness, one syllable at a time (rule 65) | `mouths.py` (`loudness_open`) |
| The quick check in seconds (script, mouths, subtitles, shot lengths) before the full pre-flight (rule 67) | `preflight.py NAME OUT --text` |
