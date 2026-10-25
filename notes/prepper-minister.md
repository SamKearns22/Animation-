# Notes for PREPPER MINISTER (one file, numbered; mark each done as it is fixed)

Brief: `prompts/prepper-minister.md` (Sam, 24 Oct). Plan in metres: `source/prepper_plan.py` (sketch:
`python3 source/prepper_plan.py sketch OUT.jpg`). References: `references/prepper-minister/`. Sound effects Sam sent:
`source/audio/prepper/sfx-*.mp3`.

## Where things stand (handover, 25 Oct, notes 37-64 chat: all applied, clips sent, waiting for Sam)
- **Done:** Sam's notes 37-64 on animatic 3 all applied (table below says what and why), plus his mid-round notes
  (kick straight at the lens, no double foot, no knee bits, legs match; hand detached in shot 2; no neck line; hand
  behind back; blade blob; sparks for all robots). Five clips sent (scratch files): wave + reach, kick + glance,
  crossbow/pistol/close-ups/swipe, belt/plasma/fire, tin + holds.
- **Timing changed:** shot 11 is now 5 s (grip held 1 s, robot 5's stare-down held 1.2 s), so shot 12 runs 53-64 s;
  the film is 64 s + black. Close-ups inside shot 9 at 32.84 and 34.54 (`CU9`).
- **Shared-kit changes (every film):** `views.py`: a leg kicked up in front is drawn over the torso (`raised`), a film
  may draw a leg itself (`j['hide_legs']`). The collision audit for this film now has every wall (cut round its
  openings) and the living-room furniture (`WALL_BOXES`, `SOLID_BOXES`).
- **Changes Sam should know about (losses / my calls):** stool 2 moved to the island's east end (it stood where Andy
  kneels and robot 1 falls); C and D's bodies cut from shot 12 (his ask: loss of continuity, they lay outside the
  window); the crossbow now lands at (4.35, 2.6), further out; Wes stands one step into the room in shot 8 (5.05); he
  fires facing 258 (not square on: his back hid the whole gun); robot 6 10 cm north; the look-down sound is his
  robot-scan (my pick).
- **Rules:** Sam approved the Prepper review's rules (25 Oct): `guides/film-quality-rules.md` 12-31,
  `guides/rule-register.md`. Earlier handovers: `notes/archive/prepper-minister-handovers.md`.
- **Checks:** audit clean over the whole film; every frame draws; mouths: only the known shot 12 shouting and line 4's
  syllable count; the rest as before (glasses line weight, short captions, Alexa 200%, long shots 9 and 12).
- **Next:** Sam's notes on the clips (Opus medium), or his yes to the check sheet, then the animatic with the Hook
  Text and sign-off (note 64): `python3 source/prepper.py final CLEAN.mp4 --small` (about 2 min), then
  `python3 source/finish.py CLEAN.mp4 OUT-vertical.mp4 "Andy asks the UK to stockpile"` (routine: Sonnet, new chat).

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail, ticked before the first animatic
| # | from the brief (word for word where it matters) | done? |
|---|------|------|
| 1 | Satire style, from `source/satire_template.py`; follow `guides/satire.md` and `guides/film-quality-rules.md` | |
| 2 | Shock level 3: nothing fully cartoony; a certain gravity | |
| 3 | Weapons have verisimilitude (in our style); the crossbow fires with a meaty thump | |
| 4 | Effects: believable debris, sparks, flames; flat house style, bold hard-edged shapes lasting a few frames, no glows | |
| 5 | Sweat: small flat beads, not cartoony | |
| 6 | The Alexa may be a real Alexa. No other real logos (crossbow's DEMON lettering dropped; beans and water unbranded) | |
| 7 | Upper-middle-class London home, refined yet contemporary; living room and kitchen open through a wide opening | |
| 8 | Door in the living room's back wall to a well-lit entrance hallway; a second door joins hallway and kitchen | |
| 9 | Living room: large modern TV opposite the sofa (shot 1's camera where the TV is) | |
| 10 | Drinks cabinet LEFT of the hallway door; Lake District hills watercolour RIGHT of it | |
| 11 | Plush old-world armchair; forest green carpet; a grand window | |
| 12 | Kitchen: island, modern amenities, slate-effect worktops, a grand window at the back (robots climb through windows) | |
| 13 | Andy: smart casual, white shirt, top button undone; the Hope Again model; stress level set per shot | |
| 14 | Wes: a full politician's suit, ripped and torn as though he has just escaped danger | |
| 15 | Robots: gleaming chrome Cylon-style (2004 BSG); single cobalt eye sweeping horizontally like a searchlight | |
| 16 | Some robots: glowing cobalt blade for one arm; some: arm cannon firing blue plasma; numbered 1-5 in shot 12 | |
| 17 | Alexa: real speaker; its battered remains return in shot 12 on tiny metal rod legs | |
| 18 | Props: crossbow, minigun with a loop of ammo, pistol, oily machete, tins of beans, 2-litre bottles of water | |
| 19 | Shot 1: mid shot, Andy in the middle of the sofa leaning forward to the lens; door behind, cabinet left, watercolour right; small flick of a wave, RIGHT hand; "Hello, Prime Minister here." | |
| 20 | TikTokPM frame from the final Cry Minister on every frame (name and description only) | |
| 21 | Shot 2: as 1, a bit closer; right hand gestures in a circle, LEFT elbow casually on his knee; "So, no biggie." | |
| 22 | Shot 3: extreme close-up; stress lines under the eyes, grin halfway to rictus; slight trembling; "But you need to stockpile, now." | |
| 23 | Shot 4: as 1; more rigid anxiety, tiny sweat beads; imploring, serious urging; "I mean, like, right now." | |
| 24 | Shot 5 (cutaway): mid shot of the island, nobody; items appear on the beat of each word: a few tins of beans, 2L water bottles, a crossbow, a minigun with a loop of ammo; detailed, recognisable; "I don't just mean beans and water. Crossbow. Minigun." No sound effects. | |
| 25 | Shot 6 (cutaway): Andy waist up in the kitchen aiming down the crossbow sights; fires on the second line; camera follows the bolt to the Alexa on the worktop; it shatters; "Test them. Test them on your Alexa."; fragments and components flying, meaty thump, whoosh, sparks | |
| 26 | Shot 7: as shot 2, back on the sofa, NO crossbow in shot; pained, imploring, much sweat; "I can't stress how little time you have." | |
| 27 | Shot 8: one moving shot from shot 7's framing, past Andy's shoulder, round to look at the hallway door; Andy opposite the door just behind the camera, crossbow in hand (never seen) | |
| 28 | Shot 8: door booted open; Wes enters under great duress with an oil-covered machete; "It's too late. They're here." | |
| 29 | Shot 8: robot over his shoulder, eye sweeping; bolt streaks through the camera position, hits its head dead centre; it falls back; blue sparks as it crumples | |
| 30 | Shot 9: wide from shot 1's spot; Andy back to us aiming at the door; Wes shuffles in away from the sparking robot | |
| 31 | Shot 9: Andy spins to the lens, chucks the crossbow, whips a pistol from behind his belt; pale and shocked; "We are already out of time. Did you get the beans? DID YOU GET THE BEANS?" | |
| 32 | Shot 9: robot lunges from the LEFT of the screen, cobalt blade arm; Andy sidesteps neatly, blasts a few holes, drops it | |
| 33 | Shot 9: "Streeting, you pussy, there's a minigun in the kitchen."; "pussy" bleeped (the word gone); subtitle "p****" (one p, four asterisks) | |
| 34 | Shot 9 effects: sweeping blue arc from the blade, pistol blasts, whipping bullets, metal fragments, sparks | |
| 35 | Shot 10: mid shot; minigun on the island, window behind, storage and counter to the RIGHT | |
| 36 | Shot 10: Wes runs up (drops the machete), drags the minigun into his hands, throws the ammo belt over his head like a bandana | |
| 37 | Shot 10: robots at the window behind him; he snarls (face only, no sound); plasma burst shoots in past him; he turns and blasts them | |
| 38 | Shot 10 effects: glass shattering everywhere, thick plasma bolt, muzzle flashes, bullets, sparks | |
| 39 | Shot 11: close-up on a tin of beans on the island, then follow it; Andy's hand grabs, pulls back, launches it; it dents harmlessly against a robot coming through the hallway-to-kitchen door | |
| 40 | Shot 12: 7 s, one 360-degree loop round Wes and Andy, pale and freaking out, either side of the island; hard cut to black | |
| 41 | Shot 12: Wes fires manically at robots 1 and 2, who walk in from the lounge, blade arms extended | |
| 42 | Shot 12: Andy dodges plasma from robots 3 and 4 and fires at them; robot 3 approaches Andy firing; Andy shoots its head off | |
| 43 | Shot 12: robot 4 crawls in over the back window sill; robot 5 fires plasma in from the hallway door and misses | |
| 44 | Shot 12: the damaged Alexa climbs to its feet on tiny metal rod limbs, holding up a sharp kitchen knife, scuttles towards Wes | |
| 45 | Shot 12: each finished action flows into aiming at a new target; Wes never stops firing; his eyes follow his targets; anything he shoots breaks and shatters | |
| 46 | Shot 12 effects: room flashing with minigun fire; plasma, blade and pistol effects; wood, ceramic and tiling erupting | |
| 47 | Continuity: every shot starts where the last left off (except 5-6); anything broken, dropped or killed stays so | |
| 48 | Sam records Andy (shots 1-7, 9) and Wes (shot 8); snarl in 10 is silent | |
| 49 | Hook Text later from Sam; CranbriJoos sign-off via `finish.py` | |

## References as checklists (guides/satire.md): what each photo shows
| reference | what it shows | use |
|---|------|------|
| robot-1-front-left, robot-2-three-quarter, robot-3-front-corridor | Cylon Centurion, waist up: chrome, hooded head with a raised central crest, narrow visor slot with one eye (red in the show; ours cobalt), segmented neck, big curved shoulder plates, chest plate with a centre ridge, slim ribbed waist, long arms with plated forearms, jointed fingers | robot design (front, three-quarter) |
| beans-in-sauce (Sam, 24 Oct) | beans in a ladle over a pan: many small plump oval beans, pale cream to light tan, each with a bright highlight, packed together half sunk in a thin glossy orange-red to brick sauce that runs and drips | the burst tins in shot 12 (note 14) |
| robot-blade-arm | concept art, not a Cylon: forearm opens into a long curved glowing blade, white and pale blue | the blade arm's shape and how it sits on the forearm |
| wes-1 (podium, straight on, talking), wes-2 (Question Time, three-quarter), wes-3 (Downing St, three-quarter smile), wes-4 and wes-5 (walking, full length, front and side) | short dark hair, side parting, faded sides, high forehead; round face, full cheeks; dark navy suit, white shirt, burgundy tie; poppy (not used); stocky build | Wes's likeness and build |
| kitchen-1 | wood island with dark (slate-like) top, grey bar stools, black pendants, marble splashback, wood beams, herringbone wood floor | island, stools, pendants, worktop colour |
| kitchen-2 | grey island, white top, brass pendants, wood stools, white shaker units, American fridge, shuttered windows, herringbone floor | modern amenities, island layout |
| living-1, living-2 | cream modern sofas, marble fireplace, panelled walls, tall glazing, big monochrome painting, leather armchair, wall-mounted TV over a low wood unit, round wood coffee tables | living room furniture, TV wall, refinement |
| crossbow | pistol crossbow, folding stock, red-dot sight, short limbs and string, grey camo, DEMON lettering (dropped: no logos) | the crossbow |
| minigun-1, minigun-2 (the second sent twice) | six-barrel rotary gun, top carry handle, rear grips, ammo belt in a loop to a backpack frame | the minigun and its ammo loop (no backpack in the film) |
| pistols | top: Browning Hi-Power; bottom: Glock 17 | the pistol: the Glock (Sam, 24 Oct) |
| machete (sent twice) | long blade with a hooked tip, black handle, brass rivets | Wes's machete (oiled) |
| alexa | Echo Dot (5th gen): charcoal fabric sphere, black base, blue light ring, two buttons on top | the Alexa |

| robot-4-full-front-and-back | statue of the 2004 Centurion, full length, front and back: long thin legs, reverse-angled shins, plated thighs, three-toed feet; back: hood falls to a spine ridge, ribbed back, hip plates | full length, legs, feet, back view |
| robot-5-side-profile | right figure: the 2004 Centurion in profile (hood crest, long jaw-like visor, plated upper arm, tall); left figure: an older-style Cylon (not ours) | side view (right figure only) |
| robot-6-eye-closeup | the visor slot from below: a dark band across the face, one bright eye inside it, chrome ribbing under the chin | the eye (ours cobalt, a flat shape, no glow) |
| robot-7-walking-back-three-quarter | an older-style Cylon from behind, walking: box backpack, exposed pistons in the legs | how the leg joints move only; not its body |
| robot-cannon-palm | a robot arm whose open palm holds a glowing core | the cannon: plasma fires from the open palm |
| andy-white-top | Andy now: dark rectangular glasses, grey-flecked dark hair, white short-sleeved zip-neck polo | face and glasses check; the outfit stays the brief's white shirt |
| water-bottle-2l | 2-litre bottle, ribbed sides, blue cap, pale blue label with hills (Tesco: dropped) | the water bottles, plain blue label |
| beans-tin | Heinz tin: turquoise label, keystone panel (Heinz: dropped) | the beans: a turquoise tin with a plain band reading BAKED BEANS and a few beans drawn on it |

**References: all in (24 Oct).** Sam: no caricature of Wes needed; the hallway and furniture are kept simple (we barely
see the hallway; he may change his mind on the furniture), so no photos for them.

## The world (rule 1): `source/prepper_plan.py` is the plan; summary
- Plan view: x east, z north (away from shot 1's camera). Living room 6 x 5.4 m (forest green carpet), kitchen 5.6 x
  5.4 m to its west (grey stone tiles), hallway 1.6 m wide behind both (stairs; front door at its east end).
  Ceilings 2.8 m. Wide opening 2.8 m in the living room's west wall (screen left in shots 1 and 9).
- Hallway door in the living room's north wall straight behind the sofa, hinged on its left; kicked open it bangs the
  wall beside the drinks cabinet. Kitchen door in the kitchen's north wall at its east end.
- Grand windows: living room east wall (by the armchair); kitchen west wall over the sink run.
- Cameras, people and robots: the sketch, and `CAMS`, `PEOPLE`, `ROBOTS` in the plan file.

## Stress level per shot (1 = calm, 6 = hysterical)
| shot | Andy | Wes |
|---|---|---|
| 1 | 1 friendly, collected | |
| 2 | 1, a touch too breezy | |
| 3 | 3 stress lines, grin halfway to rictus, slight tremble (deliberate: listed in `allow`) | |
| 4 | 4 rigid anxiety, a few small sweat beads | |
| 5 | voice only | |
| 6 | 3 grim focus down the sights (an earlier moment) | |
| 7 | 5 pained, much sweat | |
| 8 | unseen | 5 great duress |
| 9 | 6 pale, shocked, shouting | 5 |
| 10 | | 5, snarl |
| 11 | hand only | |
| 12 | 6 pale, terrified | 6 pale, manic |

## Reuse before building (guides/satire.md, Movement)
- Andy: the Hope Again Andy through `views.py` (any angle), new outfit (shirt, trousers, belt). Seated poses:
  `moves.py` sitting. Spins, throws, aims, sidestep: `moves.py` poses and combat, `filmkit.Beats`.
- Wes: the Hope Again Streeting rebuilt to the likeness method from the new photos; ripped suit as `body_props`.
- The house: one 3D set with `Cam3`, built like `poker_mon_room.py` (every shot a camera on the same room).
- Flying things (Alexa parts, glass, tiles, tins, robot parts): Poker Mon's `launch` physics (bounce, stay put).
- Robot falls: `moves.py` falling in stages.
- TikTokPM frame: `cryminister.py` (handle, description) and `tiktok_overlay.py`.
- **New builds** (nothing fits): the Cylon robot (five views, blade and cannon arms, sweeping eye); the crossbow, minigun
  with its belt, pistol, machete, Alexa (whole, smashed, on rod legs); flat effects (muzzle flash, plasma bolt, blade
  arc, sparks, debris, glass); the 360-degree loop (people and robots swap between their drawings as the camera goes
  round: the rehearsal clip shows whether that holds up).

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | 6 | 14.2 | Andy looks at the camera at the start of the shot, then his head turns (to the sights) and he fires | done: he looks at the lens on "Test them.", his head snaps to the sights on the second "Test them" |
| 2 | 6 | 17.0-17.6 | We don't actually see the Alexa properly before it explodes: show it clearly in shot before the bolt lands | done: the Alexa was being painted behind the units (never showed); now drawn over them, the camera locks on it, the bolt flight 0.8 s |
| 3 | 12 | ~51-53 | The robot in the window clips through a window frame: remove the frames (they are shot out in shot 10 anyway) | done: from shot 10 (0.8 s after the glass goes) the kitchen window has only its outer surround; robot 4 climbs through the hole |
| 4 | 12 | | The robot in the doorway (robot 5) is too static: have it walking in and firing | done: robot 5 walks in from the hall in three stages, firing |
| 5 | 12 | | Add another robot beneath the arch (the wide opening), on the right; a good shot of it firing blue plasma before it is riddled with bullets | done: robot 6 (new, cannon) under the wide opening, on the right as the camera looks east; fires twice, riddled by Wes |
| 6 | 12 | | Extend the shot by four seconds (7 s to 11 s) | done: shot 12 runs 50-61 s; the film is now 61 s + black |
| 7 | 12 | | One robot comes at Andy with a glowing blue blade; Andy drops to his knees as it swipes and shoots its head off (the blade swipe passes over him) | done: robot 1 (blade) comes at Andy; he drops to one knee, the blade sweeps over him, he shoots its head off from his knee (seen from the west, Andy nearest). Robot 3 keeps its plasma attack but is shot in the chest (its head-off moved to robot 1) |
| 8 | 12 | | The robot in the doorway fires a few times at Streeting before being blown to smithereens (pieces flying, stays wrecked) | done: robot 5 fires five times at Wes, then is blown apart (head and plates flying, legs left, toppling; pieces stay) |
| 9 | 12 | | Slow the camera's spin as needed to take all of this in | done: one loop in 11 s (was 7); it starts south-east so each beat is faced |
| 10 | 12 | | More visible damage: bullet holes appearing where the minigun hits (big enough to read); burning scorch marks where the plasma hits; the bean tins and water bottles on the island blowing up, throwing water and baked beans across the worktop; the pendant lights shattering; cupboards splintering; spent cases flying off Wes's minigun | done: bigger bullet holes (5-8 cm), plasma scorches that burn ~3 s, tins and bottles blown up by robot 6, two pendants shattered by robot 5, cupboards splintering, spent cases off the minigun that land and stay |
| 11 | 12 | | A couple of times Andy's face looks backwards while his body faces forwards (head and body pointing opposite ways: check his head turn against his body in every frame, and add a check for it) | done: the cause was his hands and pistol drawn over his back when seen from behind; fixed in views.py for every film; new check prepper.facing_check (every frame of shots 6 and 12) |
| 12 | 12 | | Wes has the same fault as Andy: the minigun drawn over his back when seen from behind | done: any held thing counts now (the minigun draws its own fists); both arms go behind his back too |
| 13 | 12 | | The effects clip through Andy (debris drawn over him) | done: Andy and Wes are drawn on their own layers; every effect behind one of them is cut away where they stand (`Behind`). Robots don't do this yet |
| 14 | 12 | | Baked beans are more goopy and liquid | done: burst tins throw wobbling clumps of glossy sauce with cream beans; they land as flat splats and stay; five run off the island's edge (`prepper_fx.goop`). |
| 15 | 6, 12 | | Make the Alexa 100% bigger | done: `prepper_fx.ALEXA_K = 2.0` (200 mm across), its remains in shot 12 too |
| 16 | 12 | 0:03, 0:04, 0:09 of the clip | Gun and body still wrong: Wes seen from behind AT AN ANGLE (three-quarter back) has the minigun and both fists drawn over his back, an arm bent across his back | done: the real cause was that the minigun (it draws its own fists) never counted as held, so the rule never fired for Wes; props now mark `own_fists`, and `views.py` hides held things from three-quarter back too. |
| 17 | 12 | ~51-54 | Robot 4 (in the window): they both fire at it for some time, so it should visibly take hits (holes, sparks, a jolt per burst) and then EXPLODE (like robot 5), not slump. Add two more robots (7 and 8) advancing across the garden outside the window; they never reach the window before the camera turns away | done: Wes's rounds now rise to the chest of the robot he aims at (robot 4 had taken none); 18 of his and 3 of Andy's, a jolt each; it blows apart at 2.75 s (`BLOWN`), while still in shot; robots 7 and 8 stalk the garden (`GARDEN`, my timing). |
| 18 | 12 | | Bullet holes hang in empty space (hits on the empty window frame) | done: `WALLS` with their openings in `ray_hit`; `marks_check` (every mark on a real surface) in `check`. |
| 19 | 6 | ~17.75 | "I don't know what this yellow detail is" | done: it was the bowl of lemons (building chat's addition) standing where the Alexa sits, popping into view when it smashed: removed from the set (Sam: no lemons in shot 12 either). Also the star flashes replaced everywhere (note 20). |
| 20 | all | | Cartoon star flash is bad, too cartoony, against our style rules; investigate how it got through | done: every impact and muzzle flash is now a lumpy uneven burst, one frame (`prepper_fx.flash`, `prepper_cast.muzzle_flash`). How it got through: the building chat read "bold hard-edged shapes" as stars, no check looks at effect shapes, and the note 19 plan even proposed another star. Rule proposed to Sam, not yet approved |
| 21 | 12 | ~54 | Wes looking at Andy, not at what he's shooting | done: after robot 4 blows he swings the long way round (never past Andy) onto robot 3 (`WES_AIM`) |
| 22 | 6 | end | The arrow needs to be sticking out of the wall | done: `BOLT6_STUCK`: through the Alexa, nearly level into the splashback; also drawn in shot 12 |
| 23 | | | Sounds: robot walk, crockery, robot explosion. A small crockery slice only when crockery is hit, one per impact, in frame | done: `SLICES` in prepper.py; my addition, a dish rack on the sink run (`X.CROCK_AT`) smashed by robot 4's blast, one crockery sound, `crockery_check`; footsteps for robot 1, robot 5 and robot A; explosions for robots 4 and 5 |
| 24 | | | Hook Text: "Andy asks the UK to stockpile" | done: `HOOK` |
| 25 | 1-4, 7 |  | Andy's front-on sitting pose looks squat on the sofa rather than sat down | done: on the sofa his legs are seen through the camera's real tilt (`_sofa_leg`): knees apart and nearer, shins down to feet set forward, hips up on the cushion |
| 26 | all |  | Andy's sleeves: the wrists look embedded in the sleeve instead of coming out of it | done: the bare forearm is its own limb from the elbow, the sleeve stops there under a fat rolled cuff; the hand comes out of skin (`prepper_cast._arm`) |
| 27 | 1-7 |  | The crossbow on the table doesn't read as a crossbow: show its distinctive features (limbs, string, stock, grip, rail) | done: bolder crossbow (curved limbs, white string in a V, stirrup, rail with a loaded bolt, grip, red-dot sight, stock), mid grey; lies in front with its limbs across the frame; tins moved back a little; shot 5's camera higher and closer |
| 28 | 9 |  | The robot coming in from the left must take a swipe (or attempt one) at Andy before it is taken down; it is slightly out of frame | done: robot B rushes in from the opening, winds up and swipes across where Andy stood as he sidesteps, takes three rounds and crumples in frame |
| 29 | 10 |  | The two robots outside the window just appear: they must walk, slide or sidle into view | done: C and D walk in along the outside wall from either side of the window and turn to the glass |
| 30 | 11 |  | Beans throw: hold on the robot who is hit a second longer and give it a dent where the tin lands; Andy throws from the other side of the kitchen island (where he is at the start of shot 12) | done: shot 11 runs a second longer (shot 12 now 51-62 s); the tin leaves a dent in robot 5's chest (kept in 12), it looks down at it, then up; Andy throws from the south side of the island (his shot 12 spot) |
| 31 | 1-4, 7 |  | The black object on the table in front of the sofa is unclear: make it clearer | done: it was a dark bowl; removed (the coffee stands there now). Loss: the bowl |
| 32 | 1-4, 7 |  | Give Andy a steaming cup of coffee on a coaster on the table | done: a brick-red mug on a cork coaster, steam wisps (`prepper_fx.coffee`) |
| 33 | 9 | ~40.3 | The word 'you' in 'you pussy' is cut off | done: the bleep now starts in the silence after "you" (1.6 s into the recording, was 1.45); the caption comes up on "you" |
| 34 | 8 |  | The robot hit by the crossbow bolt just vanishes: it collapses against the wall and stays in frame | done: robot A is knocked back to the hall wall and slides down to sit, the bolt in its head, sparking every 0.6 s; it stays |
| 35 | 8 |  | Door opening: speed it up once the camera gets there; it lingers a beat too long | done: the camera arrives in 1.2 s (was 1.5) and Wes boots the door as it does; his line follows 0.9 s later (was 0.9 s of empty doorway then the line) |
| 36 | 10 |  | Streeting's first minigun burst and the window shattering need proper effects; snarl face to camera, eyes to the left, then he spins and fires | done: snap in on Wes's snarl (bared teeth, eyes sliding left), plasma over his left shoulder, he spins side-on and fires: big muzzle flash, tracers, every pane bursting (glass out into the garden and onto the sink run), cases pouring, C and D take hits and fall |
| 37 | 1 |  | Andy needs a better wave: it only comes up level with his torso | done: the hand goes up above his head, palm to us, three flicks, then down (`WAVE`) |
| 38 | all |  | Right sleeve: the cuff detail looks detached compared with the left, in every shot | done: the sleeve was tapering to ~19 at the elbow under a 27-wide cuff over a 22-wide forearm; a wider sleeve now ends flush under the cuff (`prepper_cast._arm`) |
| 39 | 2 |  | Arm move: reaching forward to the camera, 'hey, here's an interesting fact for you' | done: he leans in and his right hand comes forward and up in front of his chest towards us, a push on 'no biggie'; the hand drawn a touch bigger as it nears the lens (`REACH2`, `near_hand`). Also (Sam, mid-round): the hand had floated off a forearm pointed straight at the lens; the forearm now stays in view |
| 40 | all |  | Subtitles must be centred (they drift a bit to the left) | done: captions were placed at 470 px, now the screen's centre (540) |
| 41 | 1-4, 7 |  | No coaster shows under the mug and it isn't steaming (both asked for in note 32) | done: square cork coaster, 12 cm, 6 mm edge (the round one hid under the mug); steam a soft grey (white on the white wall was invisible) |
| 42 | 8 |  | First frame of Wes kicking the door: the kicking leg seems wrapped behind his body | done: Wes's own kick, facing us: knee up, the leg driven straight out at the door, drawn foreshortened (widening trouser leg, sole facing us) over his body, held 0.35 s after the door flies open, the knee snaps back, foot down. Shared fix in views.py: a leg kicked up in front is drawn over the torso (`raised`), and a film may draw a leg itself (`hide_legs`). Mid-round fixes from Sam: no three-quarter turn, straight forward, no double foot, no knee bits, both legs match when down |
| 43 | 8 |  | His elbow clips the side of the doorway as he steps forward | done: the kick's fighting guard put his left elbow out into the frame (arm now down for balance); he steps one step into the room (5.05) and his machete elbow is kept in; the walls audit now confirms he is clear |
| 44 | 8 |  | No duck at the crossbow shot (clear line of sight): he glances that way, shocked | done: no duck; as the bolt hits his head snaps over his left shoulder to the robot, shocked (brows up, mouth dropped), then he turns to face it |
| 45 | 8 |  | When he turns, the machete faces behind his back, wrapped round his torso: a recurring weapon fault, needs a rule for future films | done: the machete was a fixed angle on the screen, so when Wes turned it lay across his back; it now points in his body's own 3D frame (`machete(aim3=...)`, like the Glock). Rule proposed (not yet added) |
| 46 | 8 |  | Blue sparks on robot A's wound are so small they're barely noticeable | done for every robot (Sam: all robots): sparks twice as thick, half as many again, living longer; robot A's bursts also flash blue |
| 47 | 9 |  | Wes clips backwards through the doorframe; fix, and find out why the collision check missed it | done: he backs straight out of the doorway, then angles off. Why it was missed: the collision audit knew only four kitchen units and the wall cupboards; no walls, door frames or living-room furniture were ever given to it. Now every wall (cut round its doors, windows and the opening) and the furniture are solids (`WALL_BOXES`, `SOLID_BOXES`); it immediately found the elbow (43), robot A's head in the hall wall, robot B's hand in the coffee table, Wes's hand on the opening's edge: all fixed |
| 48 | 9 |  | The crossbow is wrapped round Andy's right shoulder: it should point forward (out of frame) | done: from behind the crossbow is nearly end on, hidden by him (only the limb tips at his sides); it also drew its fists over his back (it never counted as held: `own_fists`, like the minigun) |
| 49 | 9 |  | He throws the crossbow away more convincingly (it seems to just drop from him) | done: he winds it across to his right, then flings it across in front of him with a sweep of his left arm; a higher, faster arc to (4.35, 2.6), where it stays |
| 50 | 9 |  | The flying crossbow is a flat 2D line in mid-air | done: it was the flat lying-down drawing seen edge on; in flight it now turns face on to us (`crossbow3(roll=)`), flat as it lands; it was also drawn twice once down (fixed) |
| 51 | 9 |  | Andy holds the pistol in two hands at the grip, low, in a ready position while he talks to us | done: the Glock in both hands at the grip, low, at the ready, through the line and the sidestep (it had popped up to one hand by his face) |
| 52 | 9 |  | New shots: zoom in to Andy's face on each "Did you get the beans?", more distressed each time; then back to the wide shot for the robot charge | done: hard cuts in to his face on each 'Did you get the beans?' (32.84 and 34.54, the second closer), fear 5 then 6, then 6 with more sweat and a tremble; back to the wide shot at 36.4 for the charge (`CU9`) |
| 53 | 9 |  | After the swipe the blue effect comes out of the sword tip like a wavy ribbon, then vanishes (the beats before and after look right) | done: the trail is the last 0.15 s of the tip's path, smoothed, and ends where the sweep has crossed (after that the blade turns down at us and the trail hooked into a ribbon, then a blob) |
| 54 | 9 |  | 'you' still lost. Sam did not say 'pussy' in the recording: he left a gap for the bleep | done: 'you' is at 1.72-1.90 in the recording and Sam's gap at 1.92-3.0; the bleep had been placed over 'you' (1.6-1.98). Now 2.0-2.42, in the gap, and the mouth says 'pussy' under it |
| 55 | 10 |  | The ammo belt hangs off the table | done: the loop is smaller and tucked in beside the gun, on the worktop |
| 56 | 10 |  | The belt wraps itself round his head: he doesn't use his hands (check the holding rules) | done: his left hand leaves the gun, grabs the belt, lifts it up over his head and pulls it onto his forehead, then goes back to the gun; the belt's end is in his hand throughout, the gun stays at his hip (`minigun_hip(left=...)`) |
| 57 | 10 |  | After the snarl the view changes and the blue bolt goes through Wes's head: not the path it had in the frame before | done: robot D is on the screen's left of Wes; the shot went over his left shoulder (screen right) so it crossed his head. It now passes over his right shoulder, on D's side all the way, in the close-up and the wide view |
| 58 | 10 |  | He turns round completely to fire (now facing left, the gun clips through the table) | done: he turns to face the window (258: square on, his back hid the whole gun from this camera) and fires along the island's north side, onto C then D |
| 59 | 10 |  | During the snarl his eyes look the opposite way to the one we need | done: the eyes slid right (away from D); now left, to D |
| 60 | 11 |  | The bean pick-up has many frame-to-frame inconsistencies: analyse. Sam's detail: there are beans; the beans disappear; a hand suddenly appears with no beans; then the hand is holding the beans. The hand must come in smoother and the tin must be one consistent object on screen; analyse why it happened | done. Why: (1) the tin left the island at 48.30 but the hand grabbed at 48.45; (2) the arm was only drawn from 48.20, mid-frame; (3) the tin in the fist was drawn 2 cm higher and over the fist; (4) the arm stopped being drawn at a fixed time. The contact check was never pointed at this tin. Now the hand drives the tin: the arm slides in from the frame's edge, the tin stays until the fist closes, then moves only with it, drawn under the fingers |
| 61 | 11 |  | Once the tin is gripped, hold a second more | done: the grip holds a second (48.45-49.45) before he pulls back; shot 12 now starts at 53.0 |
| 62 | 11 |  | Hold a beat as robot 5 stares down at itself, with a sound for the look down (from Sam's robot sounds if none fits) | done: robot 5 stares down at the dent 1.2 s (51.35-52.55), then snaps back up; Sam's robot-scan sound on the look down (the same one as robot A's head turn in shot 8) |
| 63 | 12 |  | Delete the dead robots in the garden (out of frame), so robots 7 and 8 can advance menacingly with weapons drawn | done: C and D's bodies cut from shot 12 (loss: they no longer lie outside the window there); robots 7 and 8 advance to just outside the window, cannons raised on Wes |
| 64 | all |  | The next animatic has the Hook Text and the sign-off | in hand: the next animatic goes through finish.py (Hook Text and sign-off) |

Sam, 24 Oct, on the shot 12 clip: "really good first pass ... Excellent work though". On the cast sheet: "Wes is good,
happy with your recommendations for Andy": the cast is approved, and Andy's fear per shot is settled as planned
(shot 1: 1, 2: 1, 3: 3, 4: 4, 6: 3, 7: 5, 9: 6, 11: 6, 12: 6; `FEAR_AT` in prepper.py already holds these).

Decisions made (kept so a new chat never has to rediscover them):
- 24 Oct: the 360 loop and shot 6's bolt move are rehearsed as clips alongside the cast sheet (brief 9.3).
- 24 Oct: the bleep is made in code (a 1 kHz tone over the word); no sound file needed.
- 24 Oct, Sam's answers: house layout yes; Andy's outfit yes (white shirt, top button undone, sleeves rolled, navy
  chinos, tan belt with the pistol behind it, brown shoes); pistol: Glock; crossbow as the photo without DEMON; robots
  2.1 m and duck through doors; Wes torn and dirty, no blood; robots hit show sparks, flat grey smoke, torn wiring, no
  fluids; arms as planned (A cannon, B blade, C and D cannon, 1-2 blade, 3-5 cannon; the shot 11 robot is robot 5); the
  ammo belt round Wes's forehead like a bandana, loose end to the gun; TikTok description: later; length: judge on the
  animatic.
- 24 Oct, shot 8 (Sam): the hallway door is just behind Andy, slightly left; the camera passes over his shoulder and
  arrives at the doorway. Door moved to x 2.13-2.97 (the sofa's centre is 3.0); the camera passes over his right
  shoulder; Andy stands up unseen and fires from just behind the camera; shot 9 finds him standing in front of the
  sofa, back to us. The coffee table moved 0.25 m towards the TV to give him room.
