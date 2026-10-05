# Prompt: "A Professional" - Steve Backshall stranded on Neptune (paste into a new Claude Code session on SamKearns22/Animation-)

From Sam's own Tiny Island Times article "Steve Backshall Stranded On Neptune"
(https://tinyislandtimes.co.uk/article/steve-backshall-stranded-on-neptune).

Continue the animation project. First read these and follow them:
- CLAUDE.md;
- story/status.md;
- guides/best-practice.md: Part 1, plus **Part 2, the TikTok parody series**, which this film belongs to (every
  lesson from Mossad and The Patriots 2);
- guides/tiktok-design.md;
- guides/pipeline.md: the animatic-first rule;
- **guides/preflight.md: follow its stages in order, from this brief to the final render;**
- **guides/figure-rig.md: every person is built and posed with `source/figure.py`.**

The working rules:
- plain English for me;
- make the choices yourself;
- say how long each render will take and report how long it took;
- send a push notification at every major stage: when anything long finishes, fails or needs my decision;
- send pictures and videos in the chat.

**The brief questions are already answered** (decisions below). Only ask me something new if building turns up a
real problem. Then go straight to stage 2: the model sheet and storyboard, sent to me for approval.

**The audio comes later.** I will record every voice after the pictures are built. Model the whole film first:
- time every line from my natural pace (about 3.3 words a second), with silent placeholders;
- captions use the script words, timed to those placeholders; the sound effects can go in already;
- when my recordings arrive (named 01 to 08 by line, extra takes 03b, see preflight.md stage 4), run
  `python3 source/voices.py FILES --script ...` at once, then retime the cuts, mouths and captions to what I
  actually recorded.

## The joke
A TV series spokesperson calmly insists that explorer Steve Backshall, stranded on Neptune, will be fine,
because "Steve is a professional", while we cut to Steve earnestly presenting through ever more impossible peril.
- The target is the media's unshakeable spin and the adventure-TV persona, not Steve himself: he is drawn with
  affection, upbeat and game.
- The refrain escalates three times, the last one slowed down, as if explaining something obvious to a child.
- Play it completely straight. Nobody winks to camera.
- **What would ruin it:** Steve dying, anything gory or frightening, or mocking his looks.

## Decisions (all agreed)
1. Title: **A PROFESSIONAL**.
2. The real show's name ("Expedition") stays off screen; no real logos.
3. Steve is an affectionate caricature: dark swept hair, broad toothy grin, wiry and athletic, rolled sleeves,
   outdoor shirt and trousers, boots, a helmet with a head torch, a chest camera.
4. The spokesperson (Amelia Chin in the article), the journalist and the science editor are invented people.
5. I record all the voices; files named 01-08 by script line.
6. Ending: Steve tiny in the vast blue haze, still giving a thumbs-up as he drifts down towards the glow; hard cut
   to black. No death.
7. I write the post text and hashtags myself; avoid #SteveBackshall (suggested: #satire #UKcomedy #space #Neptune
   #explorer #animation).

## Length and words
About 38 s. 84 spoken words (about 25 s of speech at my pace, plus action). First laugh: "He will kayak to safety"
over Steve paddling a kayak on Neptune, at about 9 s. Say plainly at the animatic if it runs past 45 s.

## Script
1. SPOKESPERSON (at the lectern): "We would encourage fans not to panic. Steve is a professional."
2. SPOKESPERSON (voice over, Steve paddling on Neptune): "He has survived perils on ice and on water. Neptune is an
   inseparable mix of both. He will kayak to safety."
3. JOURNALIST: "What about the thirteen-hundred-mile-an-hour winds?"
4. SPOKESPERSON (a contemptuous huff): "Steve is a professional. Some combination of rope-work will keep him safe."
5. SPOKESPERSON (voice over, almost dreamy): "And when the diamonds rain down, he'll say things like..."
6. STEVE (to camera, sweaty, beaming, diamonds pinging off his helmet): "Wow! This is why exploration is so important!"
7. SCIENCE EDITOR: "No suit could survive the pressure of Neptune's core."
8. SPOKESPERSON (slowly): "Steve is a professional. A professional."

## Shots (no shot over about 7 s)
1. Press room (0-6 s): the push-in on the spokesperson has begun on frame one; title over the backdrop, gone by 1 s.
2. Neptune (6-11 s): a deep blue storm world; Steve in a red sea kayak paddling earnestly across a churning cyan
   sea, lightning in the methane clouds, the kayak turning in circles.
3. Press room, the journalists (11-16 s), the reverse angle of the same room: notepads and raised phones; one asks
   about the winds; back on the spokesperson's huff.
4. Neptune (16-22 s): Steve horizontal in a 1,300 mph gale, roped to his team of experts, all flapping like bunting,
   Steve giving a thumbs-up.
5. Neptune, deeper (22-29 s): diamonds raining, shirt torn and soaked, hair plastered, earnest grin: "Wow!"
6. Press room (29-35 s): the science editor in the front row; the spokesperson, slowly: "A professional."
7. Ending (35-38 s): Steve tiny in the vast blue haze, thumbs-up, drifting down towards the glow; hard cut to black.

## Places, cast and objects
- **Press room** (one set and one written plan; the journalists' shot is its reverse angle): lectern with a cluster
  of microphones, a glass and jug of water, a backdrop board (plain mountain silhouette and lettering, no real logo),
  rows of journalists with notepads and phones, a TV camera on a tripod, a boom mic, press lanyards, takeaway coffee
  cups.
- **Neptune:** deep blue and cyan sky with white streaks of methane cloud, a dark storm spot, faint rings, lightning,
  a churning sea, glowing diamonds, the moon Triton faint in the distance.
- **Cast:** Steve (above); the spokesperson (composed, blazer, lanyard, polite contempt); four or five journalists,
  each with a clear action, including the science editor (glasses, a magazine under her arm); a team of two or three
  experts in matching expedition jackets.
- **Recurring objects** (drawn once, one size against Steve): the red kayak and paddle, the rope.
- **Postures:** the spokesperson stands; journalists sit (legs under their chairs); Steve sits in the kayak, then
  flies horizontally on the rope, then floats. Design his kayak, flying and floating views on the model sheet.

## Use the new shared tools (built after The Patriots 2; first real use here)
- `source/figure.py`: solved arms, the guard, contacts, timing helpers; `rig.pose('hold', ...)` for anyone holding a
  phone, cup or notepad (upper arm hangs by the side, forearm comes forward).
- `source/mouths.py`: proper mouth shapes from the script, timed to my recordings (placeholders first).
- `source/kit.py`: contact shadows (feet, chair legs, tripod, lectern), the hands library (thumbs-up and rope grip
  for Steve; cup, phone and pen for the journalists), and secondary motion: lanyards, the rope and the experts'
  jackets lag behind and swing past; Steve's hair and rope whip in the gale.
- Start a shared series file for anything reusable from The Patriots 2 (`person()` with legs always, set and desk
  plans, `check_apart`), rather than copying from patriots2.py. **Never change patriots2.py: that film is posted
  and final.**
- Run `python3 source/preflight.py FILM OUT_DIR` before every animatic and fix what it reports.

## Sound
- Press room: camera shutter clicks, a chair creak, one cough; no murmur bed.
- Neptune: howling wind (motivated, not a constant bed), thunder cracks, paddle splashes, diamonds tinkling on the
  helmet; Steve's line shouted over the wind.
- A short, uplifting nature-documentary string swell made in code under "This is why exploration is so important"
  (original music, never a real show's), cut dead on the hard cut to black.
- Master at -14 LUFS, peaks -1 dBTP.

## Deliver
- Model sheet and storyboard first, for my approval; then the animatic; then the final render after my recordings.
- Final MP4 at 1080 x 1920, 12 fps, a few MB, saved as `animations/a-professional-vertical.mp4` and sent in the chat.
- Update story/status.md and add any new lessons to guides/best-practice.md.
- Work on a new branch for this film, and don't open a pull request unless I ask.
