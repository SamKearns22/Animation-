# Best practice: the master file

Everything we have learned from every film so far, in one place:
- Dam (Beaver vs Asteroid)
- The Salt
- the two Oxford rap battles: Andrew / Andy, and Sam
- Listening & Learning (Ed)
- the Yuletide horror score and animation test
- Hope Again (King in the North)
- The Patriots

**Read this before starting or changing any film, in any chat.** Each rule names the film it came from in
brackets, so you can see why it exists. The detailed guides it points to hold the numbers and the code:
- `tiktok-design.md`: format, safe area, titles, posting
- `character-anatomy.md`: building people
- `movement.md`: timing of eyes, smiles, hair and body
- `pipeline.md`: how the 3D pencil shots are built
- `tone.md`: the horror trailer
- `perfect-prompt.md`: how to brief a film

If two files disagree, this file wins; then fix the other file.

---

## 1. The joke and the story
- **Explain the joke, and what would ruin it, before making anything.** "Deadpan and realistic, no cartoon
  noises" did more than any visual detail (Dam).
- **Deadpan is the house style.** The absurd is played completely straight: a sincere character, a still
  camera, no winking at the audience (all films). The escalation is the joke (Hope Again).
- **Cartooning reduces absurdity.** When the joke is "this is completely normal", draw the normal thing
  realistically. Our beaver was redrawn as a field-guide illustration (Dam).
- **Set-up, then payoff.** Never open on the punchline. No text on screen or in the post that gives the
  joke away, including hashtags (Dam, Hope Again: no Game of Thrones hashtags).
- **Give seconds, not just order. Name the moments to linger on.** Build-ups need more time than you
  think: Dam's grew from 3 to 13 seconds. But on TikTok the *set-up before the first line or event* must be
  tight (see section 7).
- **Silence is a tool.** The silent close-up was the biggest laugh in Dam. The held pause after "Of
  course!" is the joke in The Salt, so keep it when tightening.
- **Don't interrupt a gag** with cutbacks in the middle of it (rap battle Sam: mid-picture cutbacks
  removed).
- **Satire:** affectionate to sharp, never cruel. Never a realistic likeness traced from a photo of a real
  person; caricature only. Suggest real organisations with colour and generic signs rather than their
  real logos (Hope Again, The Patriots). Never satirise Grenfell.
- **Evoke, don't copy.** Borrow the feel of a show or a style, never its imagery, logos, music or an
  artist's signature look (Hope Again: no show music; Listening & Learning was too close to FilmCow; the
  trailer borrows A24's craft, never its brand).

## 2. Voice and sound
**Recorded voices (Sam's own recordings)**
- **Play voices exactly as recorded:** change the volume only. No echo, no reverb, no pitch change (Hope
  Again). Where an effect is part of the joke, keep it gentle (Listening & Learning: reverb turned down).
- **Never change, trim or reorder the words.** Captions and timing follow what was actually said, not the
  script (Hope Again, rap battles).
- **Mouths follow each voice,** opening and closing with the loudness of that speaker's recording,
  frame by frame (Hope Again, rap battles: beak flaps).
- Clean voices of hiss and rumble before mixing (horror score).

**Sound effects**
- **Realistic and understated. No cartoon noises.** "The more we emphasise with clown noises the less
  humour there will be" (Dam). One dull thud for a landing; exploding rock, not a cartoon smash.
- **Direct every sound and every silence** in the plan, shot by shot (Dam).
- **Make crowd and room sound to match what is on screen:**
  - clapping only when people clap, with no generic crowd murmur;
  - natural clapping, uneven and not machine-regular;
  - no sword sounds when swords aren't struck (Hope Again).
- **Music is original, made in code.** Never use a show's or film's music. Hope Again's ominous regal
  ending (D minor strings, brass, low choir, timpani) replaced battle sounds that weren't working.
- **Big moments need contrast:** a split second of silence before the biggest hit makes it land (Dam's
  explosion; the trailer's THUD on the cut to black).

**Technical rules (check every soundtrack)**
- **No clicks.** Every sound fades in and out over at least 30 milliseconds, even a hard cut to silence.
  A rumble cut off at full volume made "an offensive crack" (Dam). Scan the whole track for sharp jumps
  before delivering.
- **Made for phone speakers.** Deep bass vanishes on a phone, so add a higher growl an octave up that a
  phone can play. Check that the loudest moment is still the loudest on a phone (Dam, horror score).
- **Master to about -14 LUFS, peaks no higher than -1.5 dBTP.** LUFS is a measure of how loud a track
  sounds; dBTP is how high its loudest peaks go. Match the loudness between sections so nothing jumps
  (horror score).
- **Fixed randomness:** any sound made from random noise uses a fixed seed (the starting number for the
  randomness) per part, so a re-render sounds the same (horror score).
- Fade out the last 1.5 seconds of a soundtrack that is cut from a longer recording (rap battles).

## 3. People: posture, movement and acting
The numbers are in `movement.md` and `character-anatomy.md`. Their checklist applies to every character
shot.

**Posture and bodies**
- **3D films:** build people on the MakeHuman body. Never hand-place a limb: say where the hand goes and
  let the arm work itself out, within natural joint ranges (animation test).
- **Wrists stay nearly straight:**
  - within about 20 degrees in normal use, never at their sideways limit;
  - when a hand holds a tool, turn the tool to suit the forearm, rather than bending the wrist to suit the
    tool;
  - the edge comes square to its target only at the moment of contact (animation test, director's note).
- **The chest follows the spine only,** so lifting an arm must never dent the chest (animation test).
- **Every contact shows proof:** a dent, a cut, a shadow, fingers wrapping. A hand resting on something
  must just touch it, neither sinking in nor hovering (animation test).
- **Feet and limbs attach to the body:** they come out from under the fur or clothes, not stuck on the
  outside (Dam).
- **Bodies stay on model:**
  - consistent heights and builds between characters and shots (rap battles: T as tall as the pigeon;
    The Patriots: protester the same height as the reporter);
  - the build fits the character (The Patriots: thick-set with a belly).

**Movement**
- **Nothing is ever frozen.** A held character still breathes, sways or blinks (moving hold). Occasional
  blinks and nose twitches made the beaver feel alive (Dam).
- **Eyes lead, the head follows.** An eye turns only so far before the head must join in, and the lids
  follow a downward look (animation test). Too much eye white looks cartoony: a glance upward shows only a
  thin pale sliver (Dam).
- **Smiles grow over half a second to a second and fade slowly.** A fast smile reads as fake.
- **No twins.** Two things never move identically:
  - falling slices twist and land differently (animation test);
  - the knights each salute differently (Hope Again);
  - crowds are uneven.
- **Gestures carry deadpan speech.** Pointing, air quotes, a wagging finger, a hand on the hip (Hope
  Again). Keep them steady: no bobbing fists (Hope Again).
- **Clear expressions:** a raised eyebrow or a cackle is drawn big enough to read on a phone (rap battles).
- **Camera moves are slow and stop dead for a reason.** The slow pull-back during the build-up stops at the
  launch, and keeps the hero object the same size (Dam).

## 4. Scene consistency and layering (what is drawn in front of what)
- **One shared set for every camera.** Build the scene once and point different cameras at it. Never
  redraw the set per shot. A close-up should be the wide camera zoomed in, so people and objects keep the
  same order and positions in every shot (The Patriots: officer, reporter, family and case, protester).
- **Carry continuity from shot to shot.** Props keep their state and position: the ham's cut and the fallen
  slices; a wall clock that stays on the wall the whole time (animation test, rap battles). Costumes too:
  lanyards on every audience member, in every shot (Hope Again).
- **Draw things in depth order, and check every overlap from the camera's view:**
  - splashes behind the dam go behind the beaver (Dam);
  - the reporter's microphone arm goes in front of the protester's arm (The Patriots);
  - an arm pointing at someone goes in front of the person it points at (The Patriots: his accusing point).
  Where two things cross, decide which is nearer the camera and draw that one last.
- **Keep writing and badges readable.** Arms, props and other people must never cross lettering, badges or
  signs the joke depends on (The Patriots: officer's lettering, arm badges).
- **Things belong where they are.** Candle flames sit on their wicks, shelves have brackets, chairs have
  legs, and floors, ceilings and ramps have no seams (The Salt). Hands stay attached to sleeves (animation
  test).
- **Frame for the action.** Keep the important moment inside the frame and the safe area (The Salt: the
  crash). Don't leave empty floor or dead space behind the characters, and keep the hands and the key prop
  in shot (The Salt, animation test).
- **When the camera moves, redraw the whole picture.** Patches from another camera position leave stale
  pieces behind (animation test).

## 5. Style and art
- **Choose one look per film and stick to it.** The account's looks so far:
  - **Coloured pencil** on off-white paper, with visible strokes and paper texture (Dam, The Salt, the rap
    battles).
  - **Graphite drawing of a 3D world**, with colour only on food, plants and decorations, and later blood
    (Yuletide trailer). See `tone.md`.
  - **Flat cartoon:** clean black outlines, almond eyes with small pupils, soft shading, still camera,
    hard cuts (Hope Again, The Patriots; developed from Listening & Learning away from FilmCow).
- **Reuse the drawing code of the film whose look you match,** so characters, captions and titles match
  across the account (Hope Again and The Patriots share `burnham.py`).
- **A limited palette,** with colour that means something: the red hat, the ham, the salt, the wine, the
  flames. Everything else stays muted (The Salt, Yuletide).
- **Confident, clean shapes.** Every emblem and prop must read at phone size: proper pickaxe heads, a
  clear salt cube and a firm shield outline replaced a slapdash coat of arms (The Salt). Shapes are built
  the way an illustrator draws them, not out of noise: clouds as cloud banks, not eggs; a vapour trail, not
  beads (Dam).
- **Detail where the eye should go.** Faces, hands and the key prop get the most detail; the edges of the
  frame are looser and lighter (animation test).
- **Make background people specific.** Model a crowd on the real audience, give everyone the right props
  (lanyards, flags), and make crowds big enough to feel real (rap battles, Hope Again).
- **Real people:** caricature only, recognisable through simple traits, never traced. A royal version
  needs royal detail: crown, dark fur, gold chain, gilded breastplate (Hope Again).
- **Makeup and costume are part of the character:** the reporter's lipstick, lashes and blush (The
  Patriots), the conference armour varied per minister (Hope Again).
- **No pencil flicker.** The stroke pattern stays tied to the surfaces and changes only on a new drawing.
- **Fresh eyes:** after any change, look at the whole picture at full size and at phone size and ask
  "what looks fake, pasted on or AI-made?"

## 6. Subtitles (captions)
- **Every spoken line is captioned, burned into the picture** (all films).
- **Words exactly as spoken,** with the script's punctuation. Check them against the recording if Sam
  changed anything while recording (rap battles, Hope Again, The Patriots).
- **A whole line at a time, held until the next line starts.** Not word by word (rap battles). For fast
  speech, show short chunks instead (Listening & Learning).
- **Look:** bold white letters with a thick black outline.
- **Placement in TikTok films:**
  - centred across the frame;
  - wrapped to at most 700 pixels wide;
  - balanced rows, so no lone word on the second row;
  - just below the picture or the faces;
  - always inside the safe area: x 60-900, y 310-1500 (The Patriots, latest director's decision).
  - Measure every line from the script text itself. Never sample a few frames: that missed the longest
    line, and it ran off both edges of a posted video (Listening & Learning).
- **Shouts can be big Anton capitals,** still inside the safe area (Hope Again: "KING OF THE NORTH!").
- **A different voice can get a different style:** the protester's childish line is in plain italics
  (The Patriots).
- **Unclear words:** a flashing red UNINTELLIGIBLE sign instead of a guess (rap battles).

## 7. Titles and the opening
The details are in `tiktok-design.md`.
- **The same title on every film:**
  - Anton capitals, letters widened 20%;
  - cranberry red (178, 24, 52) with a thick black outline;
  - the account's standard size: capitals about 148 pixels tall (Anton at about 200);
  - one or two lines, fitted inside the safe width;
  - drawn fresh at full size, never an enlarged small title.
- **TikTok opening:**
  - the full-size title sits on the opening frame, over moving picture, never over a face;
  - it is gone by about 1 second (1.6 seconds at most);
  - sound and movement start on the first frame, and the first line begins almost at once.
  - **Never a held title card.** Our first posts lost most viewers in the first 3 seconds while a title
    sat over a still scene.
  - The opening frame doubles as the cover.
- **Placement:** top edge at about 330 pixels, below TikTok's tabs (a posted title hid under them).
- **Tight set-ups:** 15-30 seconds for a short; the first payoff within about 8-10 seconds (The Salt was
  cut from 17.4 to 11.6 seconds).
- **Endings:** a hard cut to black, with the sound carrying on or landing on the cut (Hope Again, The
  Patriots, Yuletide).

## 8. Format, files and delivery
- **TikTok:** 1080 x 1920, MP4 (H.264 video, AAC sound), 12 fps; the file name ends in `-vertical`. Make
  it vertical from the start where possible. To convert a widescreen film:
  - enlarge it by a third;
  - crop only empty background at the sides;
  - fill above and below with a soft glow of the picture's own edges (no bars, streaks or blurred copies).
- **Sizes:** under 25 MB for TikTok, a few MB where possible, and always under 50 MB. Pencil textures
  need a fixed bitrate (the amount of data per second, about 3.4 Mb/s); flat cartoons are small anyway.
  Copies for Discord stay under 10 MB at full picture size.
- **X** gets the original widescreen version.
- **Only finished films go on GitHub,** in `animations/`. Drafts and test frames stay in the chat. Sam's
  reference photos never go on GitHub.
- **Send every finished film in the chat** so it can be saved to Photos from the iPhone.

## 9. How we work (process)
1. **Brief:** ask all questions in one message, with a recommended answer for each.
2. **Stills** of the look, or a storyboard. Sam can skip this step to save usage.
3. **Animatic:** a quick, small, rough version with sound, to check timing before the full render.
4. **Final render,** checked against the safe-area guides on the title frame, the widest caption and the
   busiest frame.
5. **Deliver:**
   - send the film;
   - save it on GitHub;
   - update `story/status.md`;
   - suggest a cover frame.
   Sam writes the post text and the pinned question himself.
- **Timing and notifications:** say how long each render will take, report how long it took, and send a
  push notification when anything long finishes, fails or needs a decision.
- **Feedback rounds:**
  - expect several;
  - apply every note;
  - check that the fix didn't break anything else;
  - when a fault gets through, add an automatic check so it can never return (`source/checks.py`).
- **Keep usage low:** one piece of work per session, render in the background, look at few images.
- **Write every new lesson into this file** (and the detailed guide it belongs to) as soon as it is
  learned.
