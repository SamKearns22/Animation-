# Satire-style film: the one page to read

For a full Satire-style TikTok film (more than two people talking, or any action). For two people talking, use
`guides/quick-video.md` instead. Open `guides/best-practice.md` Part 2 only for a kind of scene this page doesn't cover.

## Start
1. Copy `source/satire_template.py` to `source/NAME.py`; set `NAME`, and change only its STORY section (title, cast,
   where people stand, who looks at whom, lines, shots, actions as beats). Everything else is already wired in.
   **A remake** of an older film starts from the template too (bring over only the story, recordings and timing, never
   the old code), and keeps the original's camera angles, shot order and timing unless Sam says otherwise.
   **References (Sam, 16 Oct):** when Sam sends reference photos, say which are still missing for the best quality (the
   room from several angles incl. empty and from above, the person front and side, props), before drawing.
   **A likeness pack for anyone famous (18 Oct):** ask at the start for one straight-on photo, one three-quarter, one
   smiling or talking, and one or two caricatures Sam likes (the caricatures show what to exaggerate).
   **Reuse before building (18 Oct):** the plan names the kit part for each person, movement and prop (views, moves:
   walks, runs, falls in stages, combat; stage; perform; props falling under gravity); build new only where nothing
   fits, and say so. Shocking Behaviour hand-built its trip and lost six rounds to it.
   **Length and opening line:** settle them early; judge the length on the first animatic with the real voice (the
   Press Secretary film was cut from 75 s to 57 s only after seeing it in motion).
2. Read Sam's brief (`prompts/_brief-skeleton.md` is the shape; `prompts/russiadent-evil-template.md` a finished one).
   Ask all questions in ONE message, each with a recommended answer. Notes go in `notes/NAME.md` (`notes/_template.md`).
   Remind Sam: leave about a second of silence after each line before stopping the recording, and turn off the
   iPhone's Voice Isolation mic mode (takes stopped mid-hiss, chopped by the phone's clean-up, crackled in Cry Minister).
   In code, look lines up by their number, never their position, so cutting a line never breaks the shots after it.
3. `python3 source/NAME.py cast OUT.png`: the cast sheet. Sam approves it before anything moves. It shows **every view**
   each character appears in (from above, a close-up, mid-action), not only the default one; and for the film's key
   reaction, a **numbered strength sheet** (1 = slight, 6 = huge) for Sam to pick a number from.
4. `python3 source/NAME.py stills OUT_DIR T T ...`: one still per shot. Sam's notes come back in one batch.

## Getting it right first time (18 Oct: Sam's review of Shocking Behaviour's rounds)
- **Never draw blind (Sam, 20 Oct):** if a reference can't be had (a site blocked, a photo missing), stop and ask Sam
  for it; never draw from memory. (Power Crime Action: the photo sites were blocked and the cast was started from
  memory: brown card instead of white, tall helmets nobody wore.)
- **A reference is a checklist.** Before drawing anything from a photo, write down what it shows: how many, colours,
  positions, which way they face, brands, proportions. Then `python3 source/compare.py REF OURS OUT.jpg` (side by
  side, same height, guide lines across) and tick each one off before sending. (The scooters took three goes.)
- **Likeness method.** Measure the face on the straight-on photo with compare.py's guide lines: face width to height,
  where the hairline, brows, eyes, nose base, mouth and chin sit, eye size and spacing, mouth width, the lines and
  creases. Build the head to those numbers (in the house style), then put it beside the photo and list every
  difference yourself before Sam sees it. Exaggerate what the caricatures exaggerate. (Farage took six passes.)
- **Real sizes.** Every prop and set piece is drawn at its real size in metres through the scene's camera (sizes
  from `source/sizes.py`; add a missing one after looking it up), and listed in the film's `PROP_SIZES` so
  preflight checks it. A new prop goes on the cast sheet beside a person (`sizes.scale_ref`). (The paper, pens, lift
  and doorway came out the wrong size.)
- **Body landmarks.** The cast sheet draws the waist, hips, knee and ankle lines (`landmarks.draw`); every garment
  edge is listed in `OUTFIT` and checked: skirts start at the waist, suit jackets end below the hips, a knee-length
  hem sits at the knee. Each person's height is set to their real one, relative to the others. (Skirts first started
  at the knee; Jenrick came out squat.)
- **Line work** is checked by `source/linecheck.py` on each of the cast alone (`LINE_SUBJECTS`): every outside edge
  inked, no edge between two colours without a line, one line weight. It saves one marked picture to look at.
- **Natural performance by default** (`source/perform.py`): overlapping action (hands and head arrive after the body),
  a knee bounce on the beat, faces that vary every two beats; the whole upper body sways as one piece (the neck
  stays on). (The first dance faces were robotic and the moves stiff.)
- **Song joins** are checked by `source/musiccheck.py` (the film's `SPLICE`): no beat skipped or doubled. (The old
  bridge skipped two beats; Sam heard it twice.)
- **The Hook Text never covers a sign or readout** listed in `KEEP_CLEAR` (`source/hookcheck.py`, with the film's
  `HOOK` set exactly as finish.py is given it). (It once sat over MILLBANK TOWER.)
- **`source/housestyle.py`** (run by preflight) says if the template's style is off (the smoother limbs, the arm
  checker, the general audit) or a check is missing what it needs from the film.

## The look (all built in: `source/satire_style.py`)
Flat colour, one outline weight, no gradients or glows; lumpy, hand-cut shapes (`blob`, `rough`), never perfect ovals
or ruler-straight boxes; every copy different (colours, sizes, facing); circle hands with props laid over them; deadpan
faces; hard cuts; a close-up for the reaction that matters; no title by default (Sam, 15 Oct); the Cranberry Title style (on 2 s) only when asked for.
**Crowds seen from behind are never one repeated block** (Sam, 15 Oct: it 'screams drawn with AI'): each person
gets their own shoulder width, slope and a higher shoulder, a lumpy head, a haircut with a low nape, and real clothing
detail (collar, seams, creases, ribbed knit, a flat shadow side, sometimes pinstripe, check or tweed). See
`press_secretary.reporter`. **No off-style cartoon shorthand** (sweat drops, anger veins, stars, motion lines...) in any film unless Sam asks (16 Oct): show a
feeling with the face and body. No blank surfaces: every building, wall and window in view gets windows, doors, signs, drainpipes or posters (a blank
flat wall reads as unfinished or computer-made). Signs and posters are neutral and true to the place (an EXIT sign,
a CAUTION label); **never add a joke Sam hasn't approved** (Sam, 16 Oct: a 'DAYS WITHOUT AN INCIDENT: 0' board slipped
into Roadster unasked). Suggest a sign gag as a question with the cast sheet, and add it only on his yes.

## Movement: walking, turning, poses, sitting, combat, cars (built to order)
- `views.py`: anyone from any angle (front, three-quarter, side, three-quarter back, back; facing left is mirrored),
  posed on a hidden 3D skeleton: say where a hand or foot goes and the elbow or knee is solved. Side and back views are
  worked out from the front design (hair and beard by kind, clothes by outfit).
- `moves.py`: gaits (stroll, walk, brisk, run, sprint: Williams' tempos, runs float), `travel` along a path in metres
  (body and face the way they go, planted feet never slide), `pace` (straight-180 turns at the ends); poses (standing
  styles, gestures, things held); sitting down and standing up (four phases); combat (punch, kick, sword, taking a blow,
  falling in stages); driving and getting in or out of a car (the car drawn per film). Each has checks.
- `stage.py`: people on a perspective floor (series.Room): size follows distance, feet on the floor, nearer drawn over.
- **Turns are a straight 180** (Sam's standard): one drawing to the other, held poses either side.
- **Big moves are held key poses**, never a slide through an in-between nobody makes; gestures keep their direction.
- **Hands on the face are drawn in front of it** (`j['on_face']`, props at the face `j['face_props']`): facepalm over
  the eyes with the elbow out, head in hands = the head drops forward into palms on the cheeks, a sip = cup rim at the lips.
  Arms hang clear of the jacket, never tucked in; a shrug opens the arms well out. One prop per hand (the 'cup' hand draws its cup).
- **Bending forward shortens the jacket hem to the hips** (no long tail when sitting down); a steering wheel stands
  nearly upright facing the driver (25 degrees back), never flat like a plate. (Sam, 14 Oct)
- **Runs (Sam's side-on photo refs, 14 Oct):** in flight the legs open into a long split: the back leg pushed out long
  behind, foot just off the floor; then the heel folds up under the seat; the knee drives forward with the shin hanging;
  the foot lands just ahead of the hips. Elbows at a right angle, an even swing: back elbow well behind the body,
  front fist at chest height. The OPPOSITE arm comes forward with each leg (a bug had it on the same side). Side heads: long hair covers the back of the skull, and only the
  face's edge is re-inked over the hair; back views hide hands that are in front of the body. (Sam, 14 Oct)
- **Heads from every angle (Sam, 14 Oct):** draw the head's outline first and the hair over it, inked, so a skull line
  never shows through hair. From behind there is no chin or jaw crease: the neck rises straight into the back of the
  skull, under the nape hair, and no bits of the far face (nose, cheek, beard) poke out. Every part has an outline.
- **Hair is one shape with one outline** (Sam, 16 Oct: 'a second haircut hiding behind'): locks and crown are outlined first,
  then filled together; nothing sits behind them that can peek out.
- **An eye is one opening between two lids** with the iris cut to it, so no line ever crosses the white; the lowered lid
  is a curve sagging over the iris, never a straight bar. See `press_secretary.eye`.
- **Lettering on signs and logos** is drawn once at high resolution and scaled smoothly to a fixed width (`stamp_text`), so
  it never pulses or spills out of its plaque or seal.
- **No blink may land on a key face** (Sam, 15 Oct: her eyes were shut on the punchline word): blinks are kept out of
  every expression window and just around it.
- **Eyes and jokes snap; bodies and feelings ease** (Sam, 16 Oct: 'let's try it'). Glances, a strange smile switching on, hard
  cuts: instant. A head or shoulders moving, a sigh, settling into a new feeling: eased in and out.
- **A big change of pose eases like the sigh** (Sam, 15 Oct: the sigh was 'the smoothest expression so far'; the head
  snapping up for the last line was not): glances still jump, but a head lifting into a new held pose blends from
  the exact old pose to the new one over about 0.7 s, eased in and out.
- **Pace a little slower** (Sam, 14 Oct): hold each pose about a second, let actions play at about 0.8 speed; walks
  and runs keep their real tempo (slowing a gait reads as slow motion). Reel labels sit on a dark band at the top.
- `python3 source/reel.py reel OUT.mp4` shows all of it; `reel.py sheet OUT.jpg` every pose on one sheet.
- `walker.py` (Cry Minister's walk) is retired for new films; Cry Minister keeps it.

## One set, one plan, real contact (Sam, 19 Oct: Poker Mon)
- **Each location is built once, in 3D, and every shot is a camera on it** (`poker_mon_room.render` with a `Cam3`):
  close-ups, reverse angles and the wide shot all draw the same room, furniture, people and props. Never redraw a
  place or its props by hand for one shot (Poker Mon's close shots had a few hand-placed props while the wide shot
  had its own list, so the table emptied between cuts).
- **Everything on a table, desk or shelf comes from one written plan** (Poker Mon's `THINGS`): kind, place in metres
  from the table's centre, its own details. A busy scene is busy in every shot: a high-stakes table has tall chip
  stacks at every place, bets in the middle, cards, drinks, napkins, ashtrays.
- **Anything a hand moves is driven by the hand, never on its own timeline:** one grip point moves both the hand
  targets and the object (Poker Mon's `grip(t)`), and a hand that cannot reach is a fault, never a hand stopped short
  (`screen_hand_target.clamped`, `CONTACT_FAULTS`). The chips once slid to him with no hand on them.
- **Loose things behave as pieces:** stacks topple when pushed, a pile is dragged as a pile (the back pieces lag and
  spread), a glass tips before it spills, thrown things bounce and stay where they land.
- **Checks (run by preflight through the film's `audits()`):** a contact check (every touch reaches what it touches;
  an object moves only while held) and a hands-seen check (a hand on something is drawn over it, never under the
  table). Copy `contact_check` and `hands_check` from `source/poker_mon.py`.

## Staging and acting (each is checked or has a tool)
- Everyone in a fight or a conversation looks at the other (`LOOKS_AT`; checked: eyelines).
- **Natural, moderate movement (Sam, 16 Oct, every film):** characters are never stock-still like robots or
  scarecrows by default, and never frantic unless the script calls for it. Give them normal movement that fits the
  scene (weight shifts, glances about, small gestures, adjusting their posture, a sigh). When unsure what movement suits
  a character or a scene, describe it to Sam and get his OK **before** making the stills.
- Nobody is ever frozen, and nobody wobbles: idle life is a held pose with a quick small shift now and then
  (`filmkit.shifts`), a blink or a glance; never a looping sway or tremble. A dead-still hold that is the joke (a
  stunned stare) is listed in `allow` (checked: the audit).
- Eyes **jump** to each new thing on one frame, and the head turns on the same frame (`filmkit.glance`); only following
  something that moves is smooth. An eased look reads as woozy, not alert.
- Background people and animals behave normally (pecking, chatting, walking) with relaxed, friendly faces. Nobody looks
  at the camera or reacts unless the script says so.
- One of each facial feature: when a face part is drawn over the library's face (a shocked mouth, raised brows),
  switch the library's own off (`mouth`, `brows`), or the face shows two. A drawn mouth (gritted teeth, a grimace) goes
  on only when the library mouth is 'hidden': call `satire_style.own_mouth(sp)` first (it stops with an error otherwise).
- Selfie shots: the arm holding the phone runs out of the frame towards the lens, raised for an over-the-shoulder view
  and never under the on-screen text; we never see a phone in that hand. When the threat is behind him, he glances back
  over his shoulder towards its side of the screen.
- A small or distant person reacting to the story uses the whole body (stops dead, hands on hips, a big slow head shake,
  then holds), placed where nothing in front hides them. A face-only reaction is for close shots.
- Every action as beats: set-up, action, contact, follow-through, settle, with a pace ('fast' into a hit, 'slow' out)
  (`filmkit.Beats`; every frame of the path is tested with `filmkit.check_joints`: joint limits, bone lengths, a hand
  never through a head).
- Plan big moves in the floor plan first: a fallen body is long; place action seen in two shots with
  `filmkit.visible_spots`.
- Anything that changes stays changed (a smear, a broken window): list it and probe it (`filmkit.probe_marks`).
- **Collisions and pop-ins: `source/audit.py`** (rules 5 and 6 of `guides/film-quality-rules.md`, 21 Oct). Every film
  gives `scene(t)`: its own `picture(t)` run with the drawing switched off (`audit.Recorder`), catching every person
  (`audit.placed`, from their pose, props included) and every set piece as solids; copy `power_crime.scene()` (3D sets)
  or the template's (flat films). Meant contacts go in `ALLOWED_CONTACTS` and meant pop-ins in `ALLOWED_POPS`, each
  with its reason. It tests every frame and two moments between, reports only what is on screen, and lists who is in
  each shot. Pre-flight runs it and calls it a FAULT if a film has no `scene(t)` (Power Crime Action never had the
  clipping check, and nobody knew). Run it alone: `python3 source/audit.py FILM [--shots a,b] [--sheet OUT.jpg]`
  (about 4 minutes for a 48 s film with a 2,000-person crowd). It does not judge drawing order (someone drawn over a
  door that should hide him): that is `layers(t)` below.
- **Script and mouths: `python3 source/voices.py --film FILM`** (rule 7, 21 Oct; about 25 s, pre-flight runs it).
  Each recording is cut into phrases and its syllables counted from the sound; the script's words are laid over the
  phrases, and a phrase the script doesn't cover (a sentence said but never written down) is flagged. The subtitles
  shown are compared word by word with the script (a starred word matches). Every frame, each speaker's drawn mouth
  (on screen, facing us) must shut in silence, move while the voice speaks, and open and shut no more than about
  once a syllable. A film gives `mouths_seen(t)` (copy `power_crime.mouths_seen`, which rides on its `scene(t)`, or
  the template's), `MOUTH_OPENNESS` for its own mouth drawings, and `ALLOWED_MOUTHS` (a jaw dropped in horror) with
  reasons. No speech recognition here: a flagged phrase means "listen to that bit", not certain proof.
- **Nothing passes through anything** (Sam, 18 Oct, after the trip in Shocking Behaviour took nine rounds). Before every
  animatic `preflight.py` runs `source/clipcheck.py` over every frame: every body, head, limb, hand, prop, piece of
  furniture and flying thing is a solid (the film's `solids(t)`; people come free from their pose with
  `clipcheck.person_solids`), and no two may overlap unless the contact is listed in `ALLOWED` (a hand on a desk, a
  punch landing). Drawing order: the film's `layers(t)` in the order it draws them; nearer is always on top, and when
  two swap front and back, the one moving must not be hidden behind the other at that moment (or a part jumps out
  from behind in one frame: Jenrick's arm and Farage). Anything on the floor (spills, stains, dropped things) is drawn
  as part of the floor, before the people. `IN_SHOT` people never touch the frame's edge.
  **Nothing is left out of `layers(t)`** (Sam, 18 Oct: Jenrick stood 'inside the desk' after the trip because his
  second drawing, over the desk top, was the one piece not checked). Better, never draw a person twice: draw
  furniture in pieces (top, legs, front panel), each at its own depth, so someone behind a desk is hidden by its top
  and someone leaning over it shows above it. If a second pass is unavoidable, it is its own layer and may show only
  the parts that really sit above the thing it is drawn over (here: only while he lay across the desk).
- **Movement that obeys physics** (the same check): no part moves faster than a real one can in a frame (a teleport);
  if the script says someone hits something, they really touch it (`CONTACTS`: Jenrick first stopped short of the
  desk); a stumble or fall keeps moving until it lands (`MOMENTUM`: he slowed and steadied himself); things knocked
  flying go the way they were pushed (`PUSHES`: the pens flew backwards onto his legs). For any motion-led beat, plan
  the path in metres with a speed for each moment before drawing a pose, and judge it in a short clip.
- Anything thrown or dropped falls under gravity, scatters unevenly (each piece its own size and speed), lands, and
  stays where it lands.
- The title never covers anyone (checked). It sits no higher than 310 px (TikTok's buttons); one line sits highest
  (`TITLE_AT` in the template).
- Sound effects are placed by when they really start (`filmkit.place`), not by the start of their file.
- Anyone in a close-up must be seen in a wide shot.

## Subtitles (Sam, 16 Oct)
- **Short chunks of two to five words**, each on its first word, so the text changes about once a second (Sam,
  17 Oct: holds second-by-second attention).
- **Never ahead of the voice:** each comes up with its first word (about 0.1 s after it starts), never before.
- **A punchline gets its own subtitle**, on the exact word (e.g. "helicopters,", "I'll get back to you on that.").
- **Word timing:** match the script's syllables to the syllable beats in the recording (see `press_secretary._syllable_beats`),
  snap each comma and full stop to the nearest real pause, and pin any word Sam names to his second
  (`PINS`). Evenly spreading words over a stretch drifts. Sam's times refer to the animatic he last watched.

## Sound (all in `source/mossad_audio.py`)
- **No sound effects unless the script names them or Sam asks** (Sam, 14 Oct): voices only by default.
- **Cut a recording only in a moment of silence** (Sam, 16 Oct): find the quiet gap before the first wanted word (loudness in
  20 ms steps), cut there and lay silence in front; never start earlier to be safe (a scrap of the word before is heard).
- Never squash the voice to make it loud: `MA.master` evens out loud stretches gently (down over 30 ms, back over
  300 ms), masters at -16 LUFS and limits by 3 dB at most (checked: `MA.limit_check`). Phone takes peak about 20 dB over
  their average; squashed 8 dB to reach -14 LUFS, they crackled on a phone.
- Every line's tail is cleaned (`MA.smooth_tail`, built into `MA.line`): the real "s", "z" or "k" is kept, then the hiss
  only fades. The phone's clean-up chops final hisses into bursts and thumps, which the extra volume makes obvious.
- Lines recorded in one go and played back to back with no gap stay ONE unbroken piece of sound, split only for the
  mouths (as in `cryminister._voices`); never fade, treat separately or space out pieces cut mid-sound.
- When Sam reports a bad sound, first make a short clip of the original recording and the film's version of that moment
  at the same volume, to learn whether the fault is in the recording or our processing. Send each sound fix as a
  sound-check file (the soundtrack over one still) before any render.

## Overlays and Hook Text (Roadster, 16 Oct)
- On-screen readouts (dials, scores) sit inside the safe area and are big enough to read on a phone; no decorative icons
  beside them (Sam: cluttering). A number too long for its dial shows short (1.3M) with the full figure on a plate.
- Check the frames under the Hook Text: it must not cover the action of the opening seconds (`finish.py ... --y`).
  Emoji at the end of the Hook Text are drawn as Noto pictures (`source/fonts/emoji/<hex>.png`; download new ones from
  fonts.gstatic.com/s/e/notoemoji/latest/<hex>/512.png).

## Before every render
`python3 source/preflight.py NAME OUT_DIR` (all cores; or `python3 source/NAME.py check` for the plan checks and audit
alone, seconds to minutes). It runs: the plan checks (mouths move for every phrase, the voice sits at least 6 dB above
everything else, subtitles printed as text: proofread them now), the general audit (each body alone: in pieces, popping,
stretching, frozen; actions, including elbows staying on their own side; eyelines; the title clear of everyone), and a
contact sheet with the safe area, and the shared checks (housestyle, audit, clipcheck, hookcheck, musiccheck, linecheck,
sizes, landmarks: see 'Getting it right first time'). Fix every fault, or list a deliberate one (`FAST_OK`/`allow`/
`ALLOWED`/`LINE_OK`) with its reason.
It also prints **QUESTIONS FOR SAM** about the sound (deep wind rumble, dead silence, a jump in volume at a cut). They may
be meant: put each to Sam with a recommended answer, and change nothing until he answers.

## Render
- `python3 source/NAME.py final OUT.mp4 --small --span T0 T1`: a clip of just that moment (under a minute) for any
  note on movement (Sam, 18 Oct); no yes needed first.
- `python3 source/NAME.py final OUT.mp4 --small`: a quick look (540 x 960), only when a shot's movement changed.
- `python3 source/NAME.py final animations/NAME-vertical.mp4`: the final. Pictures are cached; captions and title go on last.
- Caption or timing note: `... final OUT --reuse` (no pictures re-rendered). Note on shot X: `... --reuse --redo X`.
- Sound note: rebuild the sound only and attach it to the finished picture (never a re-render).
- Say how long it will take; push notification when it ends; send the film in the chat; update `story/status.md`.

## If a check fails
| Message | Fix |
|---|---|
| `in N pieces` | A body part is detached (neck, head, limb): its base must sit inside the shape it joins. A stain on the floor is fine: list it in `allow`. |
| `pops` / `stretches` | A pose switches drawing or a limb flips between frames: add an in-between pose, or ease the beat. A body thrown on purpose: list it. |
| `frozen` | Give them a held pose with small quick shifts (`filmkit.shifts`), a blink or a glance; never a sway loop. A hold that is the joke: list it in `allow`. |
| `crossed the middle of the body` | The elbow bends the wrong way (usually `'down'`): bend it `'out'` or use a relaxed `'depth'` arm. If the action really crosses (arms folded, reaching across), list it; ask Sam if unsure. |
| `the title covers` | Raise it (no higher than 310 px), make it one line, or make it smaller (`TITLE_AT`). |
| `not looking at who they are dealing with` | Fix `LOOKS_AT` or the pupils' side. |
| `bends ... degrees` / `elbow folded` | Move that beat's target further from the shoulder or add a beat that swings wide. |
| `no mouth movement` | The words aren't spread over that phrase: check the line's recording and text. |
| `only N dB above the rest` | Turn the crowd, music or effects down under that line (or the line up). |
| `... is missing at` | A permanent mark isn't drawn in that shot: draw it from the list of permanent changes. |
| `never seen in shot 2 or 3` | Move that person, or show them in a wide shot. |
| `passes through` | Two solids overlap: move the path or the pose apart; a deliberate contact goes in `ALLOWED` with its times. |
| `passes ... while partly hidden behind them` | Someone passes in front of or behind another while overlapping on screen: keep the arm (or path) clear of them as they pass. |
| `is drawn over ... nearer` | Draw it before the nearer thing (floor things before the people), or move it nearer. |
| `jumps ... in one frame` | A teleport: add in-between keys, space the keys further apart, or slow the move (a slap may be listed in `FAST_OK`). |
| `should hit ... stops ... short` / `slows to` / `flies against` | Move the end point to real contact; keep the speed up (no eased stop); launch things the way the push goes. |
| `the Hook Text ... covers` | Move it (`--y`/`--x`, the same in `HOOK`) clear of the sign or readout. |
| `the song skips` / `repeats` | Start the next piece where the message says, then send a sound-check clip. |
| `no outline` / `edge with no line` / `line weight` | Ink that edge with the house outline; see the marked picture. A flat shadow side may go in `LINE_OK`. |
| `a real ... is about` / `too thin` | Redraw it at its real size (sizes.SIZES) through the scene's camera. |
| `the skirt top is at` (etc.) | Move the garment edge to its landmark (waist, hips, knee). |
| `house style:` | Switch the template's default back on, or give the check what it needs. |
