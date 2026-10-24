# Notes for PREPPER MINISTER (one file, numbered; mark each done as it is fixed)

Brief: `prompts/prepper-minister.md` (Sam, 24 Oct). Plan in metres: `source/prepper_plan.py` (sketch:
`python3 source/prepper_plan.py sketch OUT.jpg`). References: `references/prepper-minister/`. Sound effects Sam sent:
`source/audio/prepper/sfx-*.mp3`.

## Where things stand (handover, 24 Oct, end of the building chat)
- **Stage done: building** (Opus high). New files, all working together:
  - `source/prepper_set.py`: the house in 3D from `prepper_plan.py` (rooms, walls with real openings showing the next
    room, windows with glass that breaks, both doors that swing, carpet, tiles, panelling, all the furniture, the
    gardens outside the windows, marks that stay). `python3 source/prepper_set.py test OUT.jpg` = every camera.
  - `source/prepper_robot.py`: the Centurion as a real 3D figure (hood, crest, V face, visor slot with the cobalt eye
    sweeping, shoulder plates, ribbed waist, three-toed feet; blade arm or cannon palm; walks, aims, falls, loses its
    head or an arm, bullet holes stay).
  - `source/prepper_cast.py`: Andy (white shirt open at the neck, rolled sleeves, chinos, tan belt, Glock behind it;
    `FEAR` 1-6), Wes (likeness, torn dirty suit, belt bandana), held props (crossbow, Glock, machete, minigun with belt,
    tin). `source/prepper_fx.py`: tins, bottles, crossbow and minigun on the island, the Alexa (whole, smashed, on rod
    legs with a knife), the bolt; sparks, debris that lands and stays, smoke, plasma, tracers, flashes, room flash.
  - `source/prepper.py`: the film (from the template): all 10 recordings by line number, subtitles (p**** bleeped),
    TikTokPM frame, timeline of all 12 shots (57 s + black). Shots 6 and 12 are choreographed in full; shots 1-5 and
    7-11 are blocked out only (people in place, simple gestures) and are the next stage's work.
- **Sent to Sam (24 Oct):** the cast sheet (`python3 source/prepper.py cast OUT.jpg`), and the two rehearsal clips:
  shot 6's bolt move (`final OUT --small --span 14.25 18.6`) and the shot 12 loop (`--span 50.0 57.4`).
  Waiting for Sam's notes and his fear numbers per shot.
- **Changes from the plan, flagged to Sam:** shot 6 starts from Andy's left-front (the plan's start was behind him,
  so we saw his back); the end at the Alexa is as planned. Shot 12: robot 4 crawls in over the sill and stays crouched
  on the sink run firing (stepping down onto the floor put it in the camera's path).
- **My additions, flagged to Sam:** the bolt left stuck in the splashback; robot 3's head lands on the island and
  stays; a knife block, lemons and a coffee machine on the worktop; a mirror, console and coats in the hall; gardens
  and neighbours' houses outside the windows.
- **Known gaps for the next stage:** shots 1-5, 7-11 blocked only; no mouth movement on the end of "DID YOU GET THE
  BEANS?" (check flags 35.75-36.40 s); captions run on across cuts; the bleep's timing needs checking by ear; the
  collision and pop-in audit (`scene(t)`, `audit.py`) and `voices.py --film` are not wired in yet (must be before any
  animatic); sound effects are placed roughly (robot footsteps, crash, bullets on metal, tin clank, crockery still
  wanted from Sam); TikTok description and Hook Text still to come from Sam.
- **Sam's notes 1-11 are in (24 Oct, table below)**: two on shot 6, nine on shot 12. Not yet acted on.
- **Cast sheet approved (Sam, 24 Oct)**: Wes is good; Andy's fear numbers as planned (no question to ask).
- **Next stage: reading Sam's notes and deciding the fixes (Opus, medium effort, fresh chat).** Plan the fixes for
  notes 1-11 (who is which robot, the new 11 s timeline, the slower orbit, camera paths clear of every robot), apply
  them, then send new clips of shot 6 and shot 12 (`final OUT --small --span`; clips need no yes). Then: composition
  sheet of the key shots (rule 11), one still per shot, wire the audits, check sheet, animatic.
- **Files to open:** this file; `guides/satire.md`; `source/prepper.py` (use `python3 source/codemap.py`); the other
  `prepper_*.py` files only for the part a note is about.

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
| 1 | 6 | 14.2 | Andy looks at the camera at the start of the shot, then his head turns (to the sights) and he fires | open |
| 2 | 6 | 17.0-17.6 | We don't actually see the Alexa properly before it explodes: show it clearly in shot before the bolt lands | open |
| 3 | 12 | ~51-53 | The robot in the window clips through a window frame: remove the frames (they are shot out in shot 10 anyway) | open |
| 4 | 12 | | The robot in the doorway (robot 5) is too static: have it walking in and firing | open |
| 5 | 12 | | Add another robot beneath the arch (the wide opening), on the right; a good shot of it firing blue plasma before it is riddled with bullets | open |
| 6 | 12 | | Extend the shot by four seconds (7 s to 11 s) | open |
| 7 | 12 | | One robot comes at Andy with a glowing blue blade; Andy drops to his knees as it swipes and shoots its head off (the blade swipe passes over him) | open |
| 8 | 12 | | The robot in the doorway fires a few times at Streeting before being blown to smithereens (pieces flying, stays wrecked) | open |
| 9 | 12 | | Slow the camera's spin as needed to take all of this in | open |
| 10 | 12 | | More visible damage: bullet holes appearing where the minigun hits (big enough to read); burning scorch marks where the plasma hits; the bean tins and water bottles on the island blowing up, throwing water and baked beans across the worktop; the pendant lights shattering; cupboards splintering; spent cases flying off Wes's minigun | open |
| 11 | 12 | | A couple of times Andy's face looks backwards while his body faces forwards (head and body pointing opposite ways: check his head turn against his body in every frame, and add a check for it) | open |

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
