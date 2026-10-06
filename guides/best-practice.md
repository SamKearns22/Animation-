# Best practice: the master file

Read this before starting or changing any film, in any chat. It has two kinds of rule, kept apart on
purpose:

- **Part 1, general principles.** These apply to any animation we make. They come from recognised sources
  (listed at the end) and are written as principles, not recipes. Every one serves the film's intent. If a
  shot is meant to look awkward, stiff, ugly or wrong (a comic pose, a horror beat), breaking a principle
  on purpose is fine. Doing it by accident is not.
- **Parts 2-4, project rules.** These are what we have learned for one kind of film. They apply only to
  that kind of film, never to everything:
  - **Part 2:** the TikTok parody series in the flat, FilmCow-influenced cartoon look. This series is
    ongoing.
  - **Part 3:** the coloured-pencil comedy shorts.
  - **Part 4:** the Yuletide horror trailer.
- **Part 5:** how we work and deliver, for every project.

The detailed guides hold the numbers and the code:
- `tiktok-design.md`: TikTok format, safe area, titles, posting
- `character-anatomy.md` and `movement.md`: people and motion
- `pipeline.md`: the 3D pencil shots
- `figure-rig.md`: bodies and movement in the flat cartoon films (`source/figure.py`)
- `preflight.md`: the checklist that catches problems before the first render
- `tone.md`: the horror trailer
- `perfect-prompt.md`: how to brief a film

If two files disagree, this file wins; then fix the other file.

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

## 1.3 Staging, continuity and layering
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

## 1.4 Sound
Sources: EBU R 128 and streaming-platform loudness practice; standard audio-editing practice. On sound
design as storytelling: Walter Murch and the film-sound literature.
- **Sound is half the film.** Plan it shot by shot alongside the picture, including the silences.
- **Recorded voices are the performance.** Keep them natural. Any processing (reverb, pitch) must serve
  the intent and stay light. Captions and lip sync follow what was actually said.
- **Effects match the world and the tone:** realistic and understated for a realistic film. Exaggerated
  sounds are a style choice, not a default.
- **Contrast makes impact:** a beat of silence before a big hit; quiet before loud.
- **Clean edits:** every cut and every start and stop of a sound gets a short fade (a few milliseconds up
  to about 30), so nothing clicks. Before delivering, scan the finished track for clicks.
- **Loudness:**
  - mix for where the film is heard; most of ours are heard on phone speakers, which can't play deep
    bass, so add upper harmonics (a higher layer of the same sound) a phone can play;
  - streaming services turn tracks down to about -14 LUFS (a measure of how loud a track sounds overall),
    so master near that, with peaks no higher than about -1 dBTP (the loudest moment), and keep the
    loudness even across sections.
- **Reproducible:** any sound built from random noise uses a fixed seed (the starting number for the
  randomness), so a re-render sounds the same.
- **Music:** original or properly licensed; never lift a show's or film's music.

## 1.5 Look and art direction
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

# Part 2. The TikTok parody series (flat, FilmCow-influenced cartoon)
For Listening & Learning, Hope Again, The Patriots and future topical parodies. These rules apply only to
this series. Full details in `tiktok-design.md`.

**The comedy**
- **Deadpan:** a sincere character, a still camera, hard cuts, absurdity played completely straight; the
  escalation is the joke.
- Set-up, then payoff. No text on screen, in the post or in hashtags that gives the joke away.
- Topical parody must be out within 24-48 hours of the news, so the look is quick to make.

**The look**
- Flat shapes, clean black outlines, almond eyes with small pupils, soft shading. Developed from
  Listening & Learning's FilmCow look, but it must stay clearly our own (no dot eyes, uniform outlines or
  FilmCow construction).
- Reuse `burnham.py` and the film code of the latest parody, so people, captions and titles match across
  the series.
- Real people as simple, affectionate-to-sharp caricatures. Costume and makeup carry character (the
  royal king's crown, fur and chain; the reporter's lipstick).

**What we learned**
- **Voices:**
  - Sam's recordings play exactly as recorded, with volume changes only, no echo and no pitch change;
  - mouths follow each voice (Hope Again);
  - crowd sound only for what is on screen, with natural, uneven clapping;
  - music made in code, never the parodied show's (Hope Again).
- **Gestures carry the speech:** pointing, air quotes, a wagging finger, a hand on the hip. Keep fists and
  props steady, and give each character a different salute or reaction (Hope Again).
- **One shared set for every camera:** the single shot is the two-shot camera zoomed in, so positions
  never jump between shots (The Patriots).
- **Layering:**
  - the reporter's microphone arm goes in front of the protester's arm;
  - his accusing point goes in front of the reporter;
  - lettering and badges stay clear of arms (The Patriots).
- **Props and costume on everyone, in every shot:** lanyards on the whole audience (Hope Again).

- **Background sound (Mossad):** no constant noise beds. A café murmur or street rumble made from filtered noise
  sounds like wind on the microphone and irritates from the first second; use only distinct, motivated sounds (clinks,
  typing, a machine, a passing car).
- **Every background person has a clear, readable action** (the barista pouring milk), never vague arm-waving.
- **Even a deadpan character acts with the face, beat by beat** (the cashier: serious, wide-eyed, hand on heart), while
  the camera stays still.
- **Everyone has legs and feet,** including people seated or standing behind counters (draw them; let the set hide them).
  Never switch legs off to save drawing, even where something "should" hide them: in The Patriots 2 the people at the
  edges of a close-up ended at the waist. `person()` in patriots2.py now always draws legs (standing, seated or walking).
- **Urgency before the deadpan (The Patriots 2):** a sudden decision to do nothing is funnier straight after urgent
  movement (doors banging open, staff running the trolley into the ward), so build the rush, then stop dead.
- **Props at real size and used the real way:** a 12 oz takeaway cup is about half a head tall; stacks sit wide end
  down; an order pager is a small upright block, not a disc.
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

**Hands (Russiadent Evil, 6 Oct)**
- **Never invent a close-up hand from circles and sausages.** Three freehand attempts at hands holding a phone came out
  as claws, mittens and "penile" thumbs, and dots for fingers. Any hand bigger than a fist-sized blob is built on
  MakeHuman's real hand with `source/hands3d.py`: a solver bends the real finger bones round the prop (resting on it,
  never through it; the thumb on its target with its **nail facing the viewer**), nails are added (MakeHuman's mesh has
  none) on the back of each fingertip, and it is drawn flat in our style (one skin tone, one shadow tone, black
  outlines from the silhouette, overlaps and creases). The prop is in the render too, so whatever is behind it is
  hidden. Check the solve by eye: a failed solve pushes a finger through the prop (drop that pose).
- Work from photo references of the real grip (two palms round the phone, thumbs over the screen).

**Lessons from The Patriots 2 (4 Oct)** - each is now caught at the start by `preflight.md` and `figure-rig.md`:
- **Bodies:** arms built by the figure system (`figure.py`: one length per character, solved from targets, the
  guard measures every arm); legs and feet on everyone, always; a person lying on a bed is drawn side-on, on their
  back, face up, with a face profile; people pushing a trolley lean into it; a heard letter is not spoken (no mouth
  movement while typing).
- **Sets:** one plan per location and per desk or table, drawn by every camera; set pieces that must stay apart are
  listed and checked; uniform details are part of the garment, drawn before the arms; props at real size and
  working height (a trolley's mattress at the staff's waist, a keyboard under the fingertips).
- **Detail that sells a place:** generic set dressing proposed in the brief (the ambulance's oxygen cylinder,
  labelled drawers, kit bags, sharps bin, drip bag, blue lights through a frosted window; the ward's whiteboard,
  dispensers, oxygen and suction outlets, clinical waste bin); an urgent rush (doors banging open, staff running)
  before a deadpan stop makes the stop funnier.
- **People from real groups:** check sources before drawing (small-boat arrivals: about 13% adult women, mostly
  from countries where women cover their hair: draw headscarves); design each person's hair and clothes
  deliberately (a greying man's hair on young men read as beads).
- **Caricature by accident:** compare a new invented character with the series' real-person caricatures (the
  doctor first resembled our Andy Burnham).
- **Recordings:** files named by script line number; `voices.py` catches duplicates (two names, one take) at once;
  shortening the silences between phrases (never the words) tightened the film by 2 s.
- **No unexplained movement:** a prop that moves needs a visible cause (the wobbling can).

**TikTok format (the account's standard; it also applies to TikTok versions of the other films)**
- Native 1080 x 1920; the safe area is x 60-900, y 310-1500, measured on a real post.
- **The opening:**
  - sound and movement from the first frame, with the first line almost at once;
  - never a held title card: our first posts lost most viewers in the first 3 seconds while a title sat
    over a still scene;
  - the standard title shows for about 1 second (1.6 at most) over moving picture, and that frame doubles
    as the cover.
- **Set-ups:** 15-30 seconds in all, with the first payoff within about 8-10 seconds.
- **The title:**
  - Anton capitals, letters widened 20%, cranberry red (178, 24, 52) with a thick black outline;
  - capitals about 148 pixels tall, top edge at about 330 pixels;
  - drawn fresh at full size.
- **Captions:**
  - bold white with a black outline, centred on the frame;
  - wrapped to at most 700 pixels, in balanced rows;
  - just below the faces;
  - big Anton capitals for shouts, plain italics for a childish aside (The Patriots).
- **Endings:** a hard cut to black.

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

---

# Part 3. The coloured-pencil comedy shorts
For Dam, The Salt and the Oxford rap battles (Andy and Sam).
- **The look:** coloured pencil on off-white paper, with visible strokes and paper texture, and simple
  backgrounds.
- **Realism serves the joke:** the beaver is drawn like a field-guide illustration because "cartooning him
  reduces the absurdity" (Dam). Sounds are realistic and understated, never cartoon noises.
- **Lessons from Dam:**
  - a long, slow build-up (13 seconds) before the launch;
  - a slow pull-back that stops dead at the launch, keeping the dam the same size;
  - a glance up shows only a sliver of eye white;
  - splashes behind the dam are drawn behind the beaver;
  - the feet come out from under the fur;
  - no click at the cut to silence;
  - the explosion stays loudest on a phone.
- **Lessons from The Salt:**
  - a clean coat of arms that reads at phone size;
  - flames sit on wicks, and floors have no seams;
  - the crash is framed inside the safe area;
  - the deadpan pause after "Of course!" is kept when the film is tightened.
- **Lessons from the rap battles:**
  - whole-line subtitles from the punctuated script, held until the next line;
  - a flashing red UNINTELLIGIBLE sign for words nobody can make out;
  - the two rappers at matching heights;
  - the crowd modelled on the real audience;
  - no cutbacks in the middle of a picture gag.
- TikTok versions follow the TikTok format in Part 2. Widescreen originals converted to vertical are
  enlarged by a third, with a soft glow of their own edges above and below.

---

# Part 4. The Yuletide horror trailer (3D world drawn in graphite)
The guides for this project are `tone.md`, `character-anatomy.md`, `movement.md` and `pipeline.md`, and
they apply to this project:
- the A24 craft (dread over shock, restraint, patient camera);
- graphite with colour only on food, plants and decorations (and later blood);
- MakeHuman bodies, measured contacts and automatic checks;
- the animatic-first workflow.

Specific lessons recorded there include:
- the cleaver held with a near-straight wrist, the blade turning with the forearm and coming square only
  in the cut;
- the chest following the spine only;
- eyes clamped with lids following the gaze;
- slices that fall differently;
- a full redraw whenever the camera moves.

---

# Part 5. How we work and deliver (every project)
1. **Brief:** ask all questions in one message, with a recommended answer for each.
   - **Set dressing goes in the brief.** For every location in the script, list the everyday items such a place
     usually has, so the place reads as real (a business meeting: laptops, pens and paper, glasses of water, a
     digital whiteboard, cabinets; an ambulance: oxygen cylinder, labelled drawers, kit bags, sharps bin). Keep it
     generic (no logos or brands) and say where each item would sit. Sam accepts or rejects them with the other
     answers, so they are decided before the storyboard and never added in later editorial renders.
2. **Stills or a storyboard** (with a model sheet of each new character), then **pre-flight**
   (`python3 source/preflight.py FILM OUT_DIR`: bodies, contacts, sets, captions and shot lengths checked on every
   third frame, plus a contact sheet with the safe area drawn on), then an **animatic** (a quick rough version with
   sound) before the final render. Sam may skip steps to save usage. Full checklist: `preflight.md`.
3. **Final render,** checked against the safe-area guides on the title, the widest caption and the busiest
   frame.
4. **Deliver:**
   - send the film in the chat;
   - save only finished films in `animations/` (under 50 MB, a few MB where possible);
   - update `story/status.md`;
   - suggest a cover frame.
   Sam writes the post text and the pinned question himself.
- **Timing and notifications:** say how long each render will take, report how long it took, and send a
  push notification when anything long finishes, fails or needs a decision.
- **Fixes:**
  - apply every note;
  - check that a fix hasn't broken anything else;
  - where possible, add an automatic check so a fault can't return.
- **Automatic clip checks (The Patriots 2):** every set piece that must stay separate (a wall monitor and a curtain, a
  dispenser and a cupboard) is listed with its outline, and the render stops if any two overlap; a typing fingertip
  must land on the keyboard. Uniform details (reflective bands, badges) are drawn as part of the jacket, before the
  arms, so arms always pass in front of them. The checks only know what they are told: keep the fresh-eyes review too.
- **Record every new lesson here, in the right part:** general only if it is truly general and backed by a
  good source; otherwise under its project.

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
