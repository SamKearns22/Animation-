# Notes for PREPPER MINISTER (one file, numbered; mark each done as it is fixed)

Brief: `prompts/prepper-minister.md` (Sam, 24 Oct). Plan in metres: `source/prepper_plan.py` (sketch:
`python3 source/prepper_plan.py sketch OUT.jpg`). References: `references/prepper-minister/`. Sound effects Sam sent:
`source/audio/prepper/sfx-*.mp3`.

## Where things stand (handover, 25 Oct, shots 8-11 chat: stopped at 2% budget, NO code changed yet)
- Read the code; nothing built. Current state (sheet seen): shots 8-11 have no people; shot 8 even drops Andy from the
  sofa at its first frame; robot B never shows on screen; no bolt, plasma, tracers or tin drawn; shot 11's camera frames
  the water bottles, not the tin. Sounds for 8-10 are already placed in `sound_events`.
- **Staging plan (ready to build, Opus high):**
  - 8: Andy seated (shot 7 pose, same hand-shake phase: give `andy_sofa` a `u`), head turns over his right shoulder as the
    camera rises; Wes kicks the door at (2.6, 6.0) (`moves.kick`, t_hit DOOR8), lurches to (2.5, 5.15), machete up, fear 5
    (`C.fear` on Wes), glance back east ~25.5; robot A walks the hall (3.9, 6.1)->(2.75, 6.1) 25.9-26.6, turns south;
    bolt from (2.95, 1.45, 2.95) fired 27.1, hits head 27.22 (passes ~0.3 m from lens, clear of Wes); bolt stays in the
    head (keep it in the head's frame); robot slumps back against the hall wall to sit (y -0.55, lean -25, feet forward),
    blue sparks then small bursts every ~0.6 s; Wes ducks 27.12, pops to face north 27.5.
  - 9: Andy aims at the door (355) to 29.4, pops to 180, flings the crossbow left (lands ~(3.85, 2.45), stays), right hand
    behind belt 29.55-29.8, Glock up by his face to 36.6, leans in on the shout; robot B lunges from (0.3, 2.9) to
    (2.05, 2.95) 36.8-37.15, blade swipe 37.1-37.3 (blade_arc); Andy sidesteps to (3.55, 2.95), pops to 270, shoots
    SHOTS9 (tracers, sparks, chips, jolts), B falls west; 9b said in profile guarding the opening, eyes flick to Wes on
    "Streeting". Wes shuffles backwards (gait at negative time) (2.5, 5.15)->(1.75, 4.65) 28.4-30, faces Andy, flinches
    at the lunge, runs at 42.35 on one path [(1.75,4.65),(0.6,3.75),(-0.8,3.55),(-2.7,3.55)] that carries into shot 10.
  - 10: camera to about (-1.15, 1.45, 4.05) looking WSW so Wes at (-2.7, 3.55) (shot 12's spot) faces it with the window
    behind; arrives ~43.7, machete dropped (stays, also drawn in 12), drags the minigun 44.05-44.35, hip 44.4, belt flung
    over his head (animate `belt_to`) bandana on 44.8; C and D step in at x -6.25 (palms outside the glass) 44.4-45.0;
    snarl 45.2 (needs a snarl mouth: russiadent has one); plasma from D 45.6 over his left shoulder and past the lens, a
    scorch on the kitchen side of x=0 at about z 4.5, y 2.2 (add to MARKS); pops to the window 45.95, fires 46.1 (all
    panes, glass burst, room flash, cases); C dies 46.4, D 47.0.
  - 11: camera low close on TIN_SPOTS[2] from about (-2.6, 1.02, 2.3); Andy's LEFT arm in from the left (Glock in his
    right), grab 48.45, pull back out of frame, release ~48.9 from about (-3.0, 1.8, 2.2) to robot 5's chest; camera
    whips to follow; Wes IS in frame during the follow (unavoidable), so draw him firing at the window (~250 deg);
    robot 5 walks (-1.2, 6.3)->(-1.2, 5.9) to meet shot 12; the tin dents, eye dips, tin lands about (-1.55, 5.15) and
    stays (draw it in 12); add minigun sound for 11.
  - Found: dead C and D lie where robots 7 and 8 end their walk in shot 12; move 7/8 end points (a change to shot 12:
    tell Sam).
- **Next:** new chat on Opus high: build the above, contact-sheet check, run the audits, show Sam the check sheet, then the
  animatic after his yes.

## Earlier handover (25 Oct, end of the second notes chat)
- **Done:** notes 14 and 16-24 (table). First full animatic rendered and sent on Sam's "just go" (no check sheet, his
  call): `final OUT --small`. Shot 12's and shot 6's clips also sent.
- **Biggest gap (told Sam):** shots 8-11 (24-50 s) have NO people: `actors()` only draws Andy and Wes in shots 1-4, 6,
  7 and 12. Wes's entrance (8), Andy's spin and pistol and robot B's lunge (9), Wes and the minigun (10), Andy's throw (11)
  are all still to build, to the brief rows 27-39. Shots 1-5 and 7 have simple gestures only.
- **Also open:** `scene(t)` and `mouths_seen(t)` are now written (audit and voices can run) but neither audit has been
  read yet; pre-flight's shared checks showed 11 faults before it was stopped for the render (not read). Wire
  `audits()` to `audit.check(film)`. Captions across cuts; bleep timing by ear.
- **Proposed rule for Sam (not added):** guides/satire.md, The look: "Flashes and bursts are lumpy, uneven blobs, never
  stars or regular spikes; before any send, list each effect's shape against the off-style list."
- **Next:** wait for Sam's notes on the animatic; then build shots 8-11 (Opus, high effort: new acting), fresh chat.

## Earlier handover (24 Oct, end of the first notes chat)
- **Stage now: apply Sam's notes 14 and 16-19, then the animatic** (Opus, medium effort, fresh chat). Sam's words: "correct
  problems and then create animatic".
- **Done in the notes chat:** notes 1-13 and 15 (table below, each says what changed). Shot 12 is 11 s (film 61 s + black),
  timed beat by beat in `source/prepper.py` under "shot 12" (the comment block there says which robot does what and when,
  and when the camera faces each part of the room). New clips of shot 6 (`--span 14.25 18.6`) and shot 12
  (`--span 50.0 61.4`) were sent; Sam's notes 16-19 came back on them.
- **Open, in this order:** note 16 (Wes three-quarter back: `views.py`, shared kit), 18 (bullet holes in empty openings:
  `ray_hit`), 17 (robot 4 takes hits and explodes; robots 7 and 8 in the garden), 19 (shot 6 impact flash), 14 (goopy
  beans from `references/prepper-minister/beans-in-sauce.jpg`).
- **Then, before the animatic (CLAUDE.md, guides/satire.md, guides/film-quality-rules.md):**
  1. Send new clips of shots 6 and 12 (no yes needed) with the self-review lines; run up to three critique-fix rounds.
  2. The known gaps from the building chat still stand: shots 1-5 and 7-11 are blocked out only (people in place, simple
     gestures) and need their acting and movement to the brief; no mouth movement at 35.75-36.40 s (end of "DID YOU GET
     THE BEANS?", `check` flags it); captions run on across cuts; the bleep's timing to check by ear; `scene(t)` for
     `audit.py` and `voices.py --film` not wired in (both needed before any animatic); sound effects placed roughly.
  3. Tick the brief checklist below against the film; run `python3 source/preflight.py prepper-minister OUT_DIR`.
  4. Show Sam the check sheet and wait for a clear yes (a note in reply is not a yes), then render the animatic
     (`final OUT --small`, about 1 s a frame across all cores: roughly 4-6 min for 61 s; push notification when done).
- **Still wanted from Sam:** an explosion sound (robots 4 and 5 blow up; none in his sound effects), the 5 sounds asked
  for at planning (robot footsteps, robot crash, bullets on metal, tin clank, crockery), the TikTok description and
  Hook Text.
- **My additions to flag again with the animatic:** robot 3's head-shot moved to robot 1 (robot 3 now shot in the
  chest); robot 4 dies on the worktop (to become an explosion, note 17); Andy also shoots robot 5; robot 6's plasma
  bursts the tins and bottles; robot 5's plasma shatters two pendants.
- **Unsure:** Andy's knee-drop (56.5-57.5 s) is partly hidden by the island; robots don't hide effects behind them yet
  (only Andy and Wes do: `Behind` in prepper.py).
- **Sam's working rule from this chat:** when he says "hold responses until all my notes are through", send NO replies
  at all until he says the notes are done (his plain "hold" = reply to each note with the plan, change nothing).
- **Files to open:** this file (this section and the Notes table); `guides/satire.md`; `source/prepper.py` (code map
  first: `python3 source/codemap.py source/prepper.py`); `source/views.py` around `held_behind`; the other
  `prepper_*.py` files only for the part a note is about.

## Earlier handover (24 Oct, end of the building chat)
- **24 Oct, notes chat:** notes 1-13 and 15 applied (table below); new clips of shot 6 (`--span 14.25 18.6`) and shot 12
  (`--span 50.0 61.4`) sent to Sam. Shot 12 is now 11 s (film 61 s + black), six robots (robot 6 new), the beats in
  `prepper.py` under "shot 12" (one comment block says which robot does what, when). Shared-kit fixes: `views.py` (held
  things seen from behind), `prepper_set.py` (window frames shot out, broken pendants). Waiting for: Sam's notes on the
  clips, and his baked-beans reference photo (note 14). Unsure: Andy's knee-drop is partly behind the island, and robot 5's
  blast has no explosion sound (none in the sounds Sam sent: ask for one). The handover below is the building chat's.
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
| 14 | 12 | | Baked beans are more goopy and liquid | done: burst tins throw wobbling clumps of glossy sauce with cream beans; they land as flat splats and stay; five run off the island's edge (`prepper_fx.goop`). Was: photo in (`references/prepper-minister/beans-in-sauce.jpg`). Burst tins throw clumps of thin glossy orange-red sauce with pale cream beans in it; they land as flat glossy splats with beans sitting in them and stay; some sauce runs off the island's edge |
| 15 | 6, 12 | | Make the Alexa 100% bigger | done: `prepper_fx.ALEXA_K = 2.0` (200 mm across), its remains in shot 12 too |
| 16 | 12 | 0:03, 0:04, 0:09 of the clip | Gun and body still wrong: Wes seen from behind AT AN ANGLE (three-quarter back) has the minigun and both fists drawn over his back, an arm bent across his back | done: the real cause was that the minigun (it draws its own fists) never counted as held, so the rule never fired for Wes; props now mark `own_fists`, and `views.py` hides held things from three-quarter back too. Was: extend the `views.py` rule (`held_behind`) from 'back' to 'three_back' too: gun, fists and forearms drawn before the torso, only what sticks out past his side shows; extend `facing_check` to flag it from any rear angle |
| 17 | 12 | ~51-54 | Robot 4 (in the window): they both fire at it for some time, so it should visibly take hits (holes, sparks, a jolt per burst) and then EXPLODE (like robot 5), not slump. Add two more robots (7 and 8) advancing across the garden outside the window; they never reach the window before the camera turns away | done: Wes's rounds now rise to the chest of the robot he aims at (robot 4 had taken none); 18 of his and 3 of Andy's, a jolt each; it blows apart at 2.75 s (`BLOWN`), while still in shot; robots 7 and 8 stalk the garden (`GARDEN`, my timing). Was: robot 4's blast replaces its slump (pieces stay on the worktop and floor); robots 7 and 8 (cannon) walk across the garden while the camera looks west, still well short of the window when it turns away; flag their timing as my call |
| 18 | 12 | | Bullet holes hang in empty space (hits on the empty window frame) | done: `WALLS` with their openings in `ray_hit`; `marks_check` (every mark on a real surface) in `check`. Was: `ray_hit` treats the whole west wall as solid, window hole included. Rounds through any opening (kitchen window once shot out, wide opening, hall door) fly on (a mark only on a real surface beyond, or none); robots 7 and 8 can catch sparks. Add a check that every mark sits on a real surface |
| 19 | 6 | ~17.75 | "I don't know what this yellow detail is" | done: it was the bowl of lemons (building chat's addition) standing where the Alexa sits, popping into view when it smashed: removed from the set (Sam: no lemons in shot 12 either). Also the star flashes replaced everywhere (note 20). Was: an upright star flash facing the camera, one frame only, plus a short spark spray and the pieces; check the impact frame full size |
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
