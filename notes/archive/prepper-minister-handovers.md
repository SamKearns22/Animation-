# Prepper Minister: earlier handovers (moved from notes/prepper-minister.md, 25 Oct; not read by new chats)

## Earlier handover (25 Oct overnight run, ~03:00: shots 8-11 built, notes 25-36 done, 3 animatics)
- **Done overnight (Sam's overrides for this run: no yes needed for the sheets or animatics; no model switches):**
  shots 8-11 built to the staging plan below; Sam's notes 25-36 (on the first animatic) all applied (table); three
  self-check rounds, each rendered and sent: animatic 1 (shots 8-11 + notes), 2 (shot 9 effects, robot 5's dent made
  visible), 3 (Wes clear of the open door in 8; shot 10's camera moved east of Wes, wider lens).
- **Latest animatic:** `final OUT --small`, 62.4 s, about 1 m 45 s to render (scratch file, sent in the chat). Shot 11 is
  now 3 s (Sam's hold), so shot 12 runs 51-62 s.
- **Checks (pre-flight, last run):** clean for shots 1-11. Left, all from before tonight in shot 12: robot 4's hand and
  shins touching the sink worktop as it climbs in (meant), robots 4 and 5 moving a lot in one frame as they are blown
  apart (meant), Wes and Andy shouting with open mouths during the shot 12 fight (no voice), Andy's glasses' line weight
  (cast check), six short captions, line 4's "I mean, like" syllable count. Prop sizes added to `sizes.py`.
- **Changes Sam should know about:** robots 7 and 8 (shot 12, garden) stop further out, short of dead C and D; robot 3
  falls to the east-south-east (it lay over robot 2); the island's tins moved back ~10 cm and the crossbow placed in
  front (shot 5's camera higher and closer); the dark bowl on the coffee table removed (coffee there now); robot B
  crumples in a heap instead of toppling (its long fall reached Andy and later robots' paths).
- **My additions (Sam can say no):** Wes glances back down the hall between his two sentences; robot 5 looks down at its
  dent before snapping back up; chrome chips from robot B stay on the carpet; robot A's head sparks every 0.6 s.
- **Shots 8-11 as built** (`source/prepper.py`, block "shots 8-11"): 8: camera arrives 1.2 s, Wes kicks the door
  (DOOR8 23.35), lurches to the doorway (2.5, 5.45), machete up; line 8 at 24.25; robot A walks the hall 25.3-26.0,
  turns, bolt 26.6 (hits 26.72), Wes ducks; A knocked to the hall wall, slides down to sit, the bolt kept in its head.
  9: Andy aims at the door, pops to us 29.4, flings the crossbow (lands (3.85, 2.45), stays), Glock from behind his belt
  up by his face, leans in on the shout; robot B rushes in from the opening, winds up, swipes as Andy sidesteps to
  (3.8, 2.95); three rounds (tracers, sparks, chips); B crumples; "Streeting" with a glance at Wes; Wes backs from the
  door, turns to Andy, flinches, runs 42.35 on a path north of B. 10: camera (-1.0, 1.5, 2.6); Wes arrives ~43.8, drops
  the machete (stays), drags the minigun 44.05-44.4, flings the belt (bandana 44.8); C and D walk in along the outside
  wall; snap in on his snarl 45.2 (eyes left); D's plasma over his left shoulder (scorch on the east wall, kept); he
  spins side-on 45.95 and fires 46.1 (flash, tracers, panes burst, glass, cases); C and D hit and fall outside.
  11: low over the island; Andy's left arm grabs the tin 48.45 and pulls out of frame; throw 48.9 from the south side;
  whip to robot 5 walking into the hall door; dent 49.6; it looks down at it, then up; tin on the floor (-1.55, 5.15).
- **Next:** Sam watches animatic 3 and gives notes, or says yes to the final render (about 30 minutes at full size,
  then `python3 source/finish.py CLEAN.mp4 animations/prepper-minister-vertical.mp4 "Andy asks the UK to stockpile"`).
  New chat for notes: Opus medium; for the final render alone: Sonnet. Read only this section, the Notes table, and
  `guides/satire.md`.

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
