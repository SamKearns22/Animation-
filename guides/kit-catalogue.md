# Kit catalogue: everything already built, to reuse before building (film-quality rule 28, Sam 25 Oct)

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

## People (satire package, `views.person`: any angle; circle hands)
| who | file | notes |
|---|---|---|
| Andy Burnham (Hope Again; Prepper's white shirt, chinos, belt with Glock) | `source/burnham.py` (`BURNHAM`), `source/prepper_cast.py` | fear levels 1-6 (`FEAR`) |
| Wes Streeting (likeness, torn suit) | `source/prepper_cast.py` (also Hope Again's in `burnham.py`) | |
| Hope Again cabinet (Streeting, Rayner, Healey, Mahmood, Miliband; armour) | `source/burnham.py` | |
| Trump, Putin, Zelensky, Claudia | `source/traitors_cast.py` | likeness heads |
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

## Creatures and machines
| what | file | notes |
|---|---|---|
| Chrome Centurion robot (3D: blade arm or cannon palm, sweeping eye, walks, falls, loses head or arm, explodes, dents) | `source/prepper_robot.py` | |
| Horse to ride, side-on (bay, chestnut, grey, black, palomino; also pony and donkey): stand, walk, trot, canter, gallop, either direction, with any satire person riding (sits, rising trot, up off the saddle at the gallop; reins, stirrups) | `source/mounts.py` | `python3 source/mounts.py reel OUT.mp4`; checks: `mounts.py check` (hooves never slide, no leg stretches, rider reaches). Side view only so far |
| Dragonite | `source/poker_mon_cast.py` | |
| Tesla Roadster (every angle) | `source/roadster.py` | |
| Crabs (Strictly Crabs) | `source/strictly_crabs_*.py` | realistic, not house style |

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

## Effects (house style: flat, lumpy, one frame for flashes; no stars, no glows)
| what | file |
|---|---|
| Lumpy flash, muzzle flash, sparks, debris that lands and stays, flat smoke, plasma bolt and scorch, tracers, blade trail, glass bursts, room flash, goopy beans, bullet holes on real surfaces | `source/prepper_fx.py`, `source/prepper_cast.py` |
| Hyper beam (soft glow: Poker Mon only, Sam's exception) | `source/poker_mon_room.py` |
| Thrown things under gravity (bounce, stay) | Poker Mon's `launch` |

## Movement and checks (the kit tools)
`views.py`, `moves.py`, `stage.py`, `filmkit.py`, `perform.py`, `audit.py`, `clipcheck.py`, `voices.py`: see
`guides/satire.md` (Movement; Staging and acting) and `guides/figure-rig.md`. The film-quality checks (25 Oct):
`plan.py` (rule 1), `benchmark.py` (3), `sets.py` (2, 12), `kitchecks.py` (13), `viewchecks.py` (15-18, 20),
`report.py` (19), `catalogue.py` (28); pre-flight runs them all.

## Added 26 Oct (Netan-Yahoo!)
| what | file |
|---|---|
| Israeli TV news studio (3D set), horseshoe layout, plan in metres | `source/newsdesk_set.py`, `source/netan_yahoo_plan.py` |
| News presenter (bearded, own three-quarter head), curved wooden chairs | `source/newsdesk_cast.py`, `source/newsdesk_props.py` |
| Benjamin Netanyahu (surprised and impressed faces, strength 1-6) | `source/netanyahu_cast.py` |
| Darth Maul, double-bladed saberstaff, leap and strikes | `source/maul_cast.py` |
| Cut-off body pieces that fall, settle and lie as a 3D pile | `source/lying.py` |
| Hook Text beside a person, three rows (`--w`); 😅 emoji | `source/hook_text.py`, `1f605.png` |
| Story post still (Maul close-up, cranberry lettering) | `animations/maul-icc-story.png` |

## Added 27 Oct (Patriots 3)
| what | file |
|---|---|
| The Patriot (balaclava, PP badges) rebuilt on views.person: every view, faces | `source/patriots3_cast.py` (`PATRIOT`) |
| German WW2 soldiers, June 1944: Gunner and Loader (M40 helmet, tunic, Y-straps, belt kit, boots or gaiters) | `source/patriots3_cast.py` (`GUNNER`, `LOADER`; `stahlhelm`, `tunic`, `kit`) |
| MG42 as a 3D solid (any angle), ammo belt, ammo box, firing flash and recoil, falling cases | `source/patriots3_cast.py` (`Gun`, `draw_mg42`, `draw_belt`, `draw_box`, `cases`) |
| Bunker embrasure with the crew: inside, from the beach, side section; beach backdrop (sea, craft, hedgehogs) | `source/patriots3_bunker.py` (`Crew`, `inside`, `outside`, `side`, `beach_layer`) |
| WW2 concrete casemate inside (raw concrete with formwork joints, ribbed steel ceiling, steel door frame, cable run, caged lamp, crates, range card, field telephone, spent cases), the passage behind, the beach or a trench through the openings; the slit's reveal round a lens inside it | `source/patriots3_room.py` (`draw`, `painter`, `foreground`) |
| The Normandy coast from the air, painted in moving layers: cliff-face casemates and MG pits firing (tracers, bullets walking across the water), textured black cliffs, shingle, rippled sand, scorched craters, wire, mined stakes, hedgehogs, steel gates, swell and surf, six LCVPs on their own headings with rippling wakes, three kinds of shell burst as soft billows, warships with barrage balloons, a rocket salvo, P-47s with invasion stripes | `source/patriots3_coast.py` (`picture`, `burst`, `craft`) |
| A shell bursting on a bunker's slit: flash, black smoke outside, dust puffs rolling in (drawn in depth order), grit from the ceiling, concrete chips that land apart and stay, the bite left in the lintel, camera shake | `source/patriots3_fx.py` |
| A held 3D prop through any 3D camera with the holder's hands put on its grips where the camera sees them (screen point turned back into a hand target), and the MG42 drawn in true perspective (end on, beside the lens) | now in the kit: `source/held3d.py` (28 Oct); the film's own: `source/patriots3.py` (`hold_gun`, `draw_gun3d`) |
| Remembrance poppy on a jacket | `source/patriots3_cast.py` (`poppy`) |
| The salute (an arm swung up round the shoulder in an arc), arms darting about (flapping, pointing round, finger wag), leaning in a doorway (figure tipped onto the post), thrown back against a wall, staggering backwards | `source/patriots3_act.py` (`salute`, `flapping`, `leaning`, `gunner`, `loader`); the salute, flapping and binoculars are now in the pose gallery |

## Added 28 Oct (Build list 27 Oct: the kit lessons and the new checks)
| what | file |
|---|---|
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
