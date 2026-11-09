# Best practice: general principles and scene lessons

- **Part 1, general principles** for any animation we make, from recognised sources (listed at the end), written as
  principles. Breaking one on purpose (a comic pose, a horror beat) is fine; by accident is not. Sections: 1.1 Story
  and intent · 1.2 Movement and acting · 1.3 Staging, continuity and layering · 1.3b Keeping old films working ·
  1.4 Sound · 1.5 Look and art direction · 1.6 Subtitles and on-screen text.
- **Part 2:** the TikTok parody series: scene lessons by film (read `guides/satire.md` first).
- **Part 5:** how we work and deliver: the few lessons not written elsewhere.
- Every rule, once, with its check: `guides/film-quality-rules.md` (the rulebook). If a guide disagrees with the
  rulebook, the rulebook wins; then fix the guide.
- Archived: the coloured-pencil shorts (`guides/archive/best-practice-pencil.md`). The Yuletide trailer, a separate
  experiment: `guides/yuletide/`.

---

# Part 1. General principles (any project)

## 1.1 Story and intent
- **Decide what the film must make the audience feel, and what would ruin it,** before making anything.
  Every later choice (look, timing, sound, acting) is judged against that. Explaining the *why* in the
  brief did more for Dam than any visual detail.
- **Give the timeline in seconds, and name the moments to linger on.** Timing sets weight and mood (Thomas
  & Johnston). Moments meant to sink in usually need more time than first planned. Openings must earn
  attention quickly: how quickly depends on the platform (Part 2 for TikTok).
- **Silence and stillness are tools,** not gaps. A held, silent moment can carry the biggest laugh or the
  biggest dread (Dam's close-up; the trailer's cut to black).
- **Satire and real people:** aim at what people do in public, not at private individuals; caricature,
  never a traced or photo-real likeness; suggest real organisations through colour and generic signs, not
  their logos. Never satirise Grenfell.
- **Evoke, don't copy.** Learn from a style, a show or a studio, but never reproduce its imagery, logos,
  music or an artist's signature look.

## 1.2 Movement and acting
- **Check that the feeling reads (Roadster, 16 Oct):** sad or weary = brows raised in the middle, mouth corners down,
  closed eyes drooping at the outer corners; calm upward arcs for closed eyes and lifted mouth corners read as content,
  even mid-sigh. Before sending, ask of each key face: would a stranger name the right feeling at phone size?
- **Natural, moderate movement for every character (Sam, 16 Oct; applies to all films):** never stock-still like a
  robot or a scarecrow by default, never frantic unless the script calls for it. Normal movement that fits the scene
  (weight shifts, glances, small gestures, posture, a sigh). If unsure what suits a character or scene, describe it to
  Sam and get his OK before making the stills.
Sources: *The Illusion of Life* (Thomas & Johnston), *The Animator's Survival Kit* (Richard Williams),
and the research in `movement.md`.
- **The twelve principles** are the baseline:
  - squash and stretch, anticipation, staging, straight-ahead and pose-to-pose;
  - follow-through and overlapping action, slow in and slow out, arcs;
  - secondary action, timing, exaggeration, solid drawing, appeal.
  How far to push them (exaggeration especially) depends on the style. A realistic film keeps them subtle;
  a cartoon pushes them.
- **Poses read first as a silhouette, with a clear line of action and believable weight and balance.**
  A character standing naturally puts its weight on one leg (contrapposto). Weight shifts before a reach.
- **Limbs keep one length per character, and are solved from where the hand or foot needs to be** (inverse
  kinematics), never typed in as separate points per shot. A hand that can't reach its target means the body or
  the prop moves, never that the arm stretches. Foreshortening only ever shortens. (Classic canon: elbows at the
  waist, wrists at the crotch, fingertips mid-thigh.) For the flat cartoon films this is built in
  `source/figure.py` and explained in `figure-rig.md`.
- **Holding something in front:** the upper arm hangs by the side and the forearm comes forward towards the
  viewer, so it looks shorter; the elbow is not lifted out sideways. Things that touch the ground get a soft
  contact shadow; anything hanging off a body (lanyard, scarf, ponytail) follows a beat behind each move, swings
  past and settles; mouths take the standard cartoon shapes from the words, timed to the recording, closed in
  the pauses. (Built for the flat films in `source/kit.py` and `source/mouths.py`.)
- **Joints move within natural ranges,** and limbs are posed from where the hand or foot needs to be.
  Example: a hand holding a tool keeps a near-neutral wrist, so the tool turns to suit the arm ("bend the
  tool, not the wrist", a basic rule of ergonomics). That example is about realistic, comfortable
  handling. A strained, clumsy or comic grip is a choice, not a mistake.
- **Avoid twinning:** limbs, characters or objects moving identically and at the same moment (a Disney
  training term). Vary timing, angle and pose.
- **No dead holds.** A character on screen breathes, sways, blinks or settles (the "moving hold"). How
  much depends on the style: a deadpan cartoon may hold very still on purpose.
- **Eyes lead:** the eyes move first, then the head, then the body. Blinks often come with a change of
  gaze or the end of a thought. Real eye jumps are fast, and real smiles grow and fade smoothly (numbers
  in `movement.md`).
- **Lip sync:** mouth shapes follow the sounds of the actual recording. Standard practice is to have the
  mouth shape arrive a frame or two before the sound, which reads as in sync to the eye.
- **Contact needs proof:** when things touch, show it (a dent, a shadow, fingers wrapping, a splash).
  Things meant to be apart must not look touching.

- **Write every action as beats with a pace word** (any action: a hit, a jump, a door shove, a sit, a bite): set-up,
  action, contact, follow-through, settle. "Slow" into it, "fast" through the contact, "slow" out. Code it as
  `filmkit.Beats`, which also tests every frame of the path, not just the key poses. A new action should read in
  one look: who does what to whom, and the result stays visible.

## 1.3 Staging, continuity and layering
- **Physical sense (Roadster, 16 Oct):** real sizes (a car is about 2.5 times a person's height); something falling
  straight onto a person stays the same size (same distance from us) and must hit them, never pass in front of them.
  Check these on the stills, before the animatic.
- **Long pieces land flat (Flying Whales, 2 Nov):** a long piece (a boom, a beam, a leg) falling into water or onto a
  floor lands lying down, never standing on its end: check its tilt at the moment it lands, and choose its spin so it
  comes down flat.
- **Read every word in a reference at full size before planning** (Roadster: the dial read ALTITUDE, not speed).
- **Recreating real footage (Roadster, 16 Oct: the ramp took three rounds):** before drawing anything, (1) step
  through the source at 6-10 frames a second over every key action and write down positions, angles and timings per
  frame; (2) work out the source camera (where it stands, what it looks along) and build any set the action touches
  (a ramp, a track, stairs) as 3D geometry seen through that same camera; (3) put the moving thing on that geometry
  with the same camera, never a flat 2D shape with the object laid on top; (4) check a few frames side by side against
  the source before the first animatic. A 2 fps sheet and a 2D ramp cost two extra rounds.
Sources: Thomas & Johnston (staging); Bordwell & Thompson, *Film Art* (continuity editing).
- **Staging:** each shot shows one idea clearly, with the eye led to it by framing, contrast and detail.
  Keep the action and the important props in frame. Avoid dead space unless it is the point.
- **Continuity:**
  - one world, seen from different cameras: build the set once and keep people, props and costumes in
    the same places and states from shot to shot;
  - **every location is built once as one set, and every shot of it is that same set from a different camera:**
    backgrounds, furniture and props never change between shots of the same place unless the script changes them
    (The Patriots 2: the reverse shot of his room first showed a door and a picture that did not exist in the
    opening shot);
  - **a recurring object is one drawing at one size:** a vehicle, piece of furniture or prop that appears in more
    than one shot (even in different locations) is drawn by the same code everywhere, at a fixed size relative to
    the people who use it (`CREW_TO_BOAT` in patriots2.py: the crew are always 0.36 of the lifeboat's scale), never
    redrawn freehand for a new shot (The Patriots 2: the lifeboat alongside the dinghy was a separate navy block,
    far taller than the boat in the shot before);
  - **props are part of the set:** everything on a table, desk, shelf or floor has one place in one written plan (its
    position measured from a fixed point, such as the character or the table's edge), and every camera draws from
    that plan, never from positions typed in separately for each shot. The plan is checked so no two items overlap
    (The Patriots 2: after the walls were shared, each shot still placed its own cans and tubs, so the desk changed
    between shots);
  - respect the 180-degree rule, so screen direction stays consistent across cuts;
  - a close-up should match its wide shot.
- **Layering (draw order):**
  - decide for every overlap which thing is nearer the camera, and draw it last;
  - judge this from the camera's view, shot by shot. A gesture towards the camera or towards another
    character usually comes in front;
  - writing, badges and signs the audience must read are never covered.
- **Objects must belong:** things rest on something, attach where they should, and cast shadows. There are
  no seams, floating pieces or gaps between parts.

- **Compose the frame, not just the floor plan.** Placing each action correctly in the room is not enough: look at
  the frame as a picture (foreground, middle, back; left, centre, right) and give each action its own area. Use the
  empty spaces; never pile the busiest actions into one corner (Russiadent Evil: the attack, a runner and a fallen
  man all in the front left, the front right empty).
- **Every action reads in one glance.** Write each figure's action as one sentence ("a zombie has him from behind and
  is biting his neck; he strains to escape"); then show the contacts that prove it: the gripping hands visible on his
  chest, the mouth on the neck. If the sentence can't be seen in the drawing, the action isn't readable.
- **Bend, don't tilt.** A person leans by bending at the waist and knees with their feet planted. Never rotate a
  whole figure like a plank (feet leave the floor and it reads as sliding or falling), unless they are falling, and
  then show the fall.
- **People never pass through each other.** Every person has a footprint on the floor plan and a planned path; no two
  footprints overlap at any moment, unless they are a pair meant to touch (an attacker and their victim).
- **Never resize a person to fit a prop or a space;** change the pose (a crouched adult is still adult-sized).
- **Close-ups and inserts are cameras in the same plan,** placed relative to the character's real position, so the
  background behind them is what is really behind them.
- **Effects land on surfaces.** Blood, mud, light and shadow attach to the physical thing they hit (the glass, the
  hands), are cut to its outline and move with it; what misses flies on out of frame. An effect over the whole frame
  floats in the air.
- **Never slice a drawing of a body to animate it,** and redraw whatever a moving object uncovers. When the phone
  fell, the hands were cut down the middle and slid apart as flat pieces: a straight cut edge through a hand, and
  holes where fingers had been hidden behind the phone. Each hand must be its own whole drawing, redrawn (here from
  the 3D hand) in its new pose once nothing hides it.
- **Show the consequence.** After an impact, something follows through (bitten, her hands go limp and the phone drops
  out of frame).

- **Check the result, not the cause.** A check written for one fault (a folded elbow) misses the next (a detached neck,
  a leg in the wrong place). Draw each character alone and test the PICTURE over time (`filmkit.silhouette_audit`):
  in pieces, popping, stretching, frozen. Plus `filmkit.check_joints` for any pose given as joints (angle limits,
  bone lengths, attachment points inside the body shape), and `filmkit.probe_marks` for things that must stay changed
  (a smear, a broken window). Shapes cut by the edge of the frame are exempt; a stain on the floor is listed as allowed.
- **Place action by sightlines before animating:** `filmkit.visible_spots` lists floor spots seen in every chosen
  camera, so an attack seen in two shots is placed once, correctly.

**Showstopper Shots (Sam, 27 Oct).** Sam's name for a large, active, eye-catching scene: the Prepper Minister fight, the
Shocking Behaviour dance, the Patriots 3 coast. Each gets an approved list of the screenplay's implied elements before it
is built (film-quality-rules 40). Patriots 3's coast shows the level wanted: terrain and bunkers, boats on their own
headings, aircraft, a combat scene that matches the place and date, and several kinds of effect.

## 1.3b Keeping old films working (Roadster, 16 Oct)
- Never give a new tool the name of an existing file: `pencil.py` was replaced by a different tool and silently broke
  Dam and the rap battles (fixed by pointing them at `pencil_cartoon.py`). Before replacing or renaming a module, search
  for every file that imports it, and render one still of each film that uses it.

## 1.4 Sound
Sources: EBU R 128 and streaming-platform loudness practice; standard audio-editing practice. On sound
design as storytelling: Walter Murch and the film-sound literature.
- **Sound is half the film.** Plan it shot by shot alongside the picture, including the silences.
- **Recorded voices are the performance.** Keep them natural. Any processing (reverb, pitch) must serve
  the intent and stay light. Captions and lip sync follow what was actually said.
- **Effects match the world and the tone:** realistic and understated for a realistic film. Exaggerated
  sounds are a style choice, not a default.
- **Contrast makes impact:** a beat of silence before a big hit; quiet before loud.
- **Trim recordings tight to the voice** (Sam's approval, Andrew the Hutt, 9 Oct): phone recordings carry breaths,
  handling noise and fumbling before, between and after the words. Find each phrase of speech in the recording
  (`mossad_audio.pauses`), keep only from 0.06 s before each phrase to 0.12 s after it, fade each edge over 25 ms, and
  leave true silence everywhere else; then check the mix is exactly silent outside the phrases. One call does it:
  `mossad_audio.gate(x)` (used by `hutt.py` and `quick.py`). The words themselves are never touched.
  Only count a stretch as speech if it reaches about a third of the take's loudest moment, measured over 50 ms
  (`mossad_audio.speech`): a quiet second of mumbling before "Yes" was once taken for the word and the caption and
  mouth ran a second early. Then confirm by measurement that sound, mouth and caption start together.
- **Time the film to the recordings, not the other way round:** place each recording so its first word lands where
  the action needs it, and derive the cuts, captions and mouth shapes from the phrases actually heard (`RECS` in
  `hutt.py`). Tie later beats to events ("0.9 s after the cut"), never to fixed seconds, so a re-record or a speed
  change moves everything with it.
- **Clean edits:** every cut and every start and stop of a sound gets a short fade (a few milliseconds up
  to about 30), so nothing clicks. Before delivering, scan the finished track for clicks.
- **Loudness:**
  - mix for where the film is heard; most of ours are heard on phone speakers, which can't play deep
    bass, so add upper harmonics (a higher layer of the same sound) a phone can play;
  - streaming services turn tracks down to about -14 LUFS (a measure of how loud a track sounds overall),
    but voice-only films made from phone recordings are mastered at about -16 LUFS, with peaks no higher
    than about -1 dBTP (the loudest moment), the loudness evened out gently and never more than 3 dB of
    limiting: squashing the voice harder to reach -14 sounded like crackle (Cry Minister). Keep the
    loudness even across sections.
- **Reproducible:** any sound built from random noise uses a fixed seed (the starting number for the
  randomness), so a re-render sounds the same.
- **Music:** original or properly licensed; never lift a show's or film's music.

## 1.5 Look and art direction
- **Effects are never Looney Tunes (Roadster dust, 16 Oct):** dust, smoke and explosions are built from many irregular
  parts (a low wall, ragged billows with dark undersides and light tops, streaks, fine particles, debris that lands and
  stays) and they thin over time. Ask Sam for a photo reference for any big effect before drawing it.
- **A detail too small to read looks like a glitch** (the visor reflection read as a white bubble, then a black speck):
  give it a clear silhouette at phone size, or ask Sam whether to keep it.
- **One coherent look per film,** with a defined palette, line and texture, held in every shot.
- **Spend detail where the eye should go:** faces, hands, the key prop. The rest is simpler, especially
  towards the frame edges.
- **Clean, confident shapes that read at the size they'll be watched.** For phones, test at phone size.
  Build shapes the way an illustrator draws them, not out of noise.
- **No flicker:** textures stay tied to surfaces and change only on a new drawing.
- **Colour with meaning:** a restrained palette makes the accent colours speak.
- **Fresh-eyes review:** after any change, look at the whole frame at full size and at viewing size, and
  ask what looks wrong, pasted on or machine-made.

## 1.6 Subtitles and on-screen text
Sources: BBC Subtitle Guidelines; Netflix Timed Text Style Guide.
- **Accurate:** the words as spoken. Unclear speech is marked as unclear, not guessed.
- **Readable:**
  - at most about 42 characters a line and two lines (three only when unavoidable);
  - lines broken at natural phrase breaks, with balanced lengths;
  - on screen long enough to read: about 160-180 words a minute, at least about a second;
  - in sync with the speech, without spilling into a different speaker or shot where avoidable.
- **Legible:** strong contrast (light text with a dark outline), a plain bold font, the same position and
  style throughout. A different style (italics, a size change) only when it means something, such as a
  different voice or a shout.
- **Inside the safe area** of the platform it is shown on: TV title-safe for widescreen, the measured
  overlay-free area for TikTok (Part 2). Measure every line's width from the text itself.
- **Titles:** one consistent title treatment across a series, legible at viewing size, never over a face.

---

# Part 2. The TikTok parody series (flat, Satire style, FilmCow-influenced cartoon)
Scene lessons for the series, by the film that taught them. `guides/satire.md` is the method and comes first; this
part is only for a kind of scene satire.md doesn't cover (creatures, fights, chaos, a real artwork, a hospital). The
TikTok format (safe area, title, captions, Hook Text, sign-off) is in `guides/tiktok-design.md`; every rule, with its
check, is in the rulebook.

**Contents:** The comedy · The look · What we learned · Big creatures and tableaux · Fights and set pieces · Chaos
scenes · Straight to the animatic · A Professional · The Patriots 2 · Captions and endings · Redrawing a real artwork ·
Cry Minister.

**The comedy**
- **Deadpan:** a sincere character, a still camera, hard cuts, absurdity played completely straight; the
  escalation is the joke.
- Set-up, then payoff. No text on screen, in the post or in hashtags that gives the joke away.
- Topical parody must be out within 24-48 hours of the news, so the look is quick to make.

**The look**
- The look itself is in `guides/satire.md`, "The look" (built into `source/satire_style.py`; every film starts from
  `source/satire_template.py`). Developed from Listening & Learning's FilmCow look, but it must stay clearly our own
  (no dot eyes, uniform outlines or FilmCow construction).
- Real people as simple, affectionate-to-sharp caricatures. Costume and makeup carry character (the
  royal king's crown, fur and chain; the reporter's lipstick).

**What we learned**
- **Sound:** crowd sound only for what is on screen, with natural, uneven clapping; music made in code, never the
  parodied show's (Hope Again).
- **Gestures carry the speech:** pointing, air quotes, a wagging finger, a hand on the hip. Keep fists and
  props steady, and give each character a different salute or reaction (Hope Again).
- **Layering:**
  - the reporter's microphone arm goes in front of the protester's arm;
  - his accusing point goes in front of the reporter;
  - lettering and badges stay clear of arms (The Patriots).
- **Props and costume on everyone, in every shot:** lanyards on the whole audience (Hope Again).
- **Background sound (Mossad):** no constant noise beds. A café murmur or street rumble made from filtered noise
  sounds like wind on the microphone and irritates from the first second; use only distinct, motivated sounds (clinks,
  typing, a machine, a passing car).
- **Even a deadpan character acts with the face, beat by beat** (the cashier: serious, wide-eyed, hand on heart), while
  the camera stays still.
- **Urgency before the deadpan (The Patriots 2):** a sudden decision to do nothing is funnier straight after urgent
  movement (doors banging open, staff running the trolley into the ward), so build the rush, then stop dead.
- **Props used the real way:** stacks sit wide end down; an order pager is a small upright block, not a disc (sizes
  themselves: `source/sizes.py`, satire.md "Real sizes").
- **Analytics (Mossad, 4 Oct):** with movement and the first line from frame one and the title gone by 1 s, average
  watch time rose to 17.1 s of 30 (first posts: 3.6-4.6 s) and 37% watched to the end. Likely next gain: no single
  shot longer than about 6-8 s; break a long speech with a cut to the listener's reaction (to be confirmed on the
  retention graph).
- **Plain captions on a sensitive topic did not block distribution (Mossad):** "October 7th" and "9/11" were written
  plainly and the video still reached 6.9K views in 6 hours. Don't disguise words in captions (it costs readability,
  breaks accuracy, and TikTok transcribes the audio anyway). TikTok's AI label is required for realistic AI content;
  our flat cartoons with Sam's own voices are not that.
- **The opening needs a hook, not a joke (DLC, 6 Oct):** comedy can take 10-20 s to build its first laugh (The
  Patriots 2 held 14.8 s average with its first laugh at ~23 s; Mossad 17.1 s), but the first seconds must give a
  reason to stay: a person, a situation, a question. DLC opened on a faithful game-logo sequence with no person or
  situation, which reads as a real advert; average watch 7.3 s. One small first batch (175 views), so luck plays a
  part too.
- **Keep the joke's give-away out of the opening shot** (no flags until the camera turns to the cashier).

**Big creatures and tableaux (Andrew the Hutt, 8 Oct)**
- **Copy the reference's pose, not just its parts:** a slug-king drawn as an upright mound read as a sofa; Sam's
  reference (the Hutt reclining, tail out to one side, upper body propped up, head leant over) fixed it. Ask for or
  find a pose reference for any non-human body before the stills.
- **Raise a big body above the people in front of it:** in a 9:16 frame a row of standing people hides anything lying
  low behind them. Put the creature on a tall platform so its whole silhouette (the tail) clears their heads.
- **Chains, leads and ropes to people never cross a face:** let the slack hang down through a gap between two people
  and loop up to the collar, as a real chain would.
- **A check only knows what it measures:** the arm guard measured lengths and the elbow angle, so an elbow folded
  back across the chest passed (Sam spotted it in the animatic). When a fault gets past the checks, add the check that
  would have caught it (`figure.audit_arm` now does), test it on the good poses too, and fix every copy of the code.
- **A swing (whip pan) is one camera turning in one set:** build the room as a strip of walls and slide the camera
  along it with motion blur (9 drawings averaged per frame), so both ends are the same room.

**Fights and set pieces (Russiadent Evil, 7 Oct)**
- **Fighters look at each other and act on each other:** a victim's eyes and free hand go to the attacker (shoving its
  face), never staring ahead.
- **One clear blow beats repeated swinging:** guard, wind-up, one fast hit, then the consequence (it flies, lands,
  bounces, lies there), and the hitter stays in the pose that shows what he did.
- **Plan the space for big moves in the floor plan before animating:** a body lying down is 1.8 m long (it filled half
  the frame and landed behind someone's legs); fold its knees or move the landing. A set-piece (a window bursting)
  goes where nothing in that shot hides it: check its screen position first.
- **Check the whole body in every review still, not only what was changed:** a phone moved into frame was approved
  while the arm holding it passed behind her head. A raised arm goes in front of the body: elbow low and forward,
  forearm up to the hand.
- **Paired characters need contrasting colours** (a zombie in green beside a man in green read as one blob).
- **Pick the simplest staging that tells the beat:** she raises the phone from the crawl rather than a new sitting
  pose. Each new pose or rig is a cost: use it only when the story needs it.

**Chaos scenes (Russiadent Evil, 7 Oct)**
- **Nobody holds a pose in a chaos shot.** A figure frozen mid-action (a tackle, a raised chair) reads as a cut-out and
  stops the eye; every person gets a repeating action (a strike that comes down fast and lifts slowly, thrashing,
  clawing, trembling, backing away) and the attackers keep advancing. Check a strip of frames, not one still.
- **A prop picked up travels with the hand:** the hand goes to it, closes, lifts it; it never just disappears.
- **Blood is thrown, not grown:** drops fly in along a path and hit at full size in one drawing, stretched along their
  flight with spikes thrown ahead and a short tail behind; then they run. A splash that swells from the centre looks
  like a slide transition.
- Keep the joke's words readable through the effect (the big splats round the edges of the page).
- **Repeating actions vary:** strikes, thrashing and clawing each have their own rhythm and phase, never in step.

**Straight to the animatic (Bingo Bingo, 14 Oct)**
- **Before Sam records, time the animatic with stand-in voices** (espeak-ng, installed by the setup script): the film
  is timed from their speech exactly as it will be from his, so pacing, cuts and captions can be judged, and his
  recordings (`polanski-KEY.m4a`) replace them line by line. The robot rushes short words: slow a line's stand-in
  until its captions pass the reading-speed check, rather than splitting the caption into tiny pieces.
- **Card and sign close-ups:** frame the item being read high in the picture, so the captions below never cover
  writing the audience must read.
- **A caption never spills into the next shot;** it stops at the cut.
- **A gesture's direction is its meaning:** "no, no" is a sideways wag; a vertical bob of the same hand reads as pumping
  (Sam, 14 Oct). Write each gesture's direction into the beat, and time it to the words it goes with.
- **Stand-in voices are for timing only: never on anything sent to Sam** (his note, 14 Oct). The animatic carries the
  effects and captions; the robot lines stay inside the code.
- **Hiding what's written further down a card or sign:** a 9:16 frame wide enough to read a line always shows the whole
  card, so framing can't hide it; keep the unread lines out of focus and rack focus to each as it is read.

**Lessons from A Professional (stage 2, 5 Oct)**
- **Props at the cartoon body's heights, not real-world metres:** our figure is about 6 heads tall, so its elbow is
  0.41 m below the neck. A lectern at a real 1.12 m reached the spokesperson's chest and her hands tangled across it;
  at her elbow height (1.0 m) the forearms rest on it naturally. Take working heights from the rig's landmarks.
- **Name who is wrong:** `series.person` tells the arm guard whose arm failed (it caught a TV operator's, a phone
  holder's and a sipping arm whose path passed too close to the shoulder before anything was rendered).

**Lessons from The Patriots 2 (4 Oct)** (the rest is now in `preflight.md`, `figure-rig.md` and the rulebook):
- **Bodies:** a person lying on a bed is drawn side-on, on their back, face up, with a face profile (now `lying.py`,
  rule L1); people pushing a trolley lean into it; a heard letter is not spoken (no mouth movement while typing).
- **Sets:** uniform details (reflective bands, badges) are part of the garment, drawn before the arms, so arms always
  pass in front of them; a trolley's mattress sits at the staff's waist, a keyboard under the fingertips, and a typing
  fingertip lands on the keyboard.
- **Detail that sells a place:** an ambulance's oxygen cylinder, labelled drawers, kit bags, sharps bin, drip bag, blue
  lights through a frosted window; the ward's whiteboard, dispensers, oxygen and suction outlets, clinical waste bin.
- **People from real groups:** small-boat arrivals are about 13% adult women, mostly from countries where women cover
  their hair: draw headscarves. Design each person's hair and clothes deliberately (a greying man's hair on young men
  read as beads).
- **Caricature by accident:** compare a new invented character with the series' real-person caricatures (the
  doctor first resembled our Andy Burnham).
- **No unexplained movement:** a prop that moves needs a visible cause (the wobbling can).

**Captions and endings (The Patriots)** (everything else on format: `guides/tiktok-design.md`)
- Big Anton capitals for shouts, plain italics for a childish aside.
- The film ends on a hard cut to black, then the sign-off.
- Notes from Sam come in one batch, numbered, each with shot and time ("shot 2, 10.3 s, left"): `notes/_template.md`.

**Redrawing a real artwork from photos (The Bayeux Tapestry Season Pass, 5 Oct)**
- Trace the photo into the artwork's own small palette, then re-render every area in code (stitches, weave); no
  photo pixel reaches the film. Enlarge and sharpen the photo *before* sorting colours, and clean gently: a strong
  clean-up at the photo's own size wiped out thin outlines and mail rings, and whole soldiers vanished.
- Erasing an object (a weapon) by borrowing colour from its neighbours leaves streaks unless the object's own
  outline colours are excluded from the borrowing; cover the whole object (fill shapes, not just their outlines).
- Small or busy photos lose faces and helmets in tracing: compare every figure with its photo at full size and
  re-stitch lost parts by hand (`REPAIRS`), rather than hoping the tracer gets them.
- Camera shake must never wrap the picture round (np.roll did: a white sliver flashed on the right); move the frame
  and repeat its edge instead.
- Action timed to a camera pan must happen while it is on screen: work out when each gun enters the view first.
- To shorten a moment, re-render it shorter; never cut frames out of a finished render. Anything still moving (a
  camera drift, flickering flames) jumps at the cut (DLC's title hold).

**Cry Minister (8 Oct)** (its sound lessons and The Park's are now in `guides/satire.md`)
- A mouth seen from the side is see-through between the jaws; only a mouth seen from the front shows the dark throat.

# Part 5. How we work and deliver (every project)
The steps (brief, sheets, pre-flight, animatic, final, delivery), the asking and the messages are in `CLAUDE.md`,
`guides/preflight.md` and the rulebook. What is left here is not written anywhere else:
- **Rules are not optional.** Never skip a step because a tool doesn't fit the film yet: fix the tool, or say so
  before going on. (Russiadent Evil: preflight was skipped, then silently checked zero frames because the film had no
  `BLACK_AT`; it now refuses such a film and runs the film's own `checks()`.)
- **Never build heavy tech when a simpler device in the style references will do** (the circle hands replaced three
  rounds of fingers and the 3D hand).
- **Lessons from Bingo Bingo (15 Oct):**
  - **Recordings with two lines in one file:** measure with `voices.py`, match each file to script lines by its
    phrases and syllables, and split at the pause between lines (`source/audio/FILM-KEY.m4a`). A later retake
    replaces both pieces of its file, so the two lines match.
  - **Fast real delivery vs subtitles:** if a line is spoken faster than 220 words a minute, add a short breath
    where two takes join and re-split the captions; if it still runs fast, say so rather than paraphrase.
  - **Things worn on the mouth** (a lip ring) are placed for each mouth shape (where its lower lip is), not at one
    fixed spot, and checked on one sheet of every shape.
  - **Sam sees every picture Claude opens.** When a film is meant to be a surprise, open no stills of it at all
    before the render.
- **The checks only know what they are told:** keep the fresh-eyes review too.
- **Where a lesson goes:** a rule (with its check) goes in the rulebook, on Sam's yes; a scene lesson for the series
  goes in Part 2 here, under its film; general only if it is truly general and backed by a good source (Part 1).

---

## References
- Frank Thomas and Ollie Johnston, *The Illusion of Life: Disney Animation* (1981): the twelve principles,
  staging, timing.
- Richard Williams, *The Animator's Survival Kit* (2001): timing, spacing, weight, lip sync, avoiding
  twinning.
- David Bordwell and Kristin Thompson, *Film Art: An Introduction*: continuity editing and the
  180-degree rule.
- Walter Murch, *In the Blink of an Eye* (2001), and his writing on film sound: editing rhythm and sound as
  storytelling.
- EBU R 128 (loudness normalisation), with the -14 LUFS reference level used by major streaming services.
- BBC Subtitle Guidelines (bbc.github.io/subtitle-guidelines) and the Netflix Timed Text Style Guide: line
  length, line breaks, reading speed, timing.
- Workplace ergonomics guidance (for example, the UK Health and Safety Executive on upper-limb disorders):
  a neutral wrist when using hand tools.
- The research cited in `movement.md` (eye movement, blinks, smile timing, hair dynamics).
- Our own TikTok analytics (30 Sept 2026) and director's notes, for Parts 2-4.
