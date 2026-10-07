# Prompt: Oxford Uni Rap Battle, split into three TikTok parts (paste into a new Claude Code session on SamKearns22/Animation-)

Continue the animation project. First read these and follow them:
- CLAUDE.md;
- story/status.md;
- guides/best-practice.md: Part 1, **Part 3 (the coloured-pencil shorts, which this film belongs to)** and the
  **TikTok format** rules inside Part 2, which apply to every TikTok version;
- guides/tiktok-design.md.

The working rules:
- plain English for me;
- make the choices yourself;
- say how long each render will take and report how long it took;
- send a push notification when anything long finishes, fails or needs my decision;
- send pictures and videos in the chat.

**The job:** turn the finished rap battle film `animations/andrew.mp4` (the penguin raps at the pigeon; code in
`source/rap.py`, 239.4 s, widescreen) into **three TikTok videos**, each 1080 x 1920, each ending at a sensible
place:
- `animations/oxford-uni-rap-battle-part-1-vertical.mp4`
- `animations/oxford-uni-rap-battle-part-2-vertical.mp4`
- `animations/oxford-uni-rap-battle-part-3-vertical.mp4`

## Where to cut
The film opens with a short intro (the penguin examines the pigeon: "Good, fascinating. I think it's trying
to communicate with us.", 1.5-6.4 s). **Drop the intro.** Part 1 starts on the next line. Times are in
seconds in the original film. Each part is about 77 seconds.

| Part | From | To | Opens on | Ends on |
|---|---|---|---|---|
| 1 | **8.1** | **~85.9** | "I apologize to the other guy, I'm really sorry, I..." (first word at 8.2; the cutaway gags start by 10.9) | "...the feces in the crease of your chin." The picture holds on the chin gag (its shot ends at 85.8), then cuts to black. |
| 2 | **~86.6** | **162.5** | "You're not spinning a yarn, Sam, you're tying a noose" (first word at 86.9) | "Normally, they don't stack shite that high." The picture holds on the pile-of-crap gag (its shot ends at 162.54), then cuts to black. |
| 3 | **162.5** | **240.4** (the end) | "You're a quite fat guy, I've half a mind to give you a nice black eye." (first word at 162.5) | The finale: the penguin's flipper drop, the hug and RESPECT, with the applause. The film's own ending. |

Notes on the cuts:
- **Every part opens with a line that starts almost at once** (within about 0.3 s of the first frame), with
  sound from the first frame and the picture already moving.
- **Check that no first or last word is clipped,** and nudge a start or end by up to 0.15 s if one is. Cuts
  must fall in the gap between lines, never inside a word.
- **No part shows the first picture of the next part.** At the end of Parts 1 and 2, hold the final drawing
  for about half a second after the last word, then cut to black. The picture and sound cut together, with a
  short fade (a few milliseconds up to 30) so the sound doesn't click.
- **A hook inside each part,** within the first 10 seconds:
  - Part 1: the sleeping-pigeon lullaby gag and the crossed-out game plan, both within the first 10 seconds;
  - Part 2: the tied-in-knots gag and the crowd gasp, within about 8 s;
  - Part 3: the "black eye" line, the factory gag and the crowd gasp.
  If the stills show a part opening on a dull picture, tell me.

## The titles
- **Our standard title** (Anton capitals about 148 px tall, widened 20%, cranberry red (178, 24, 52), thick
  black outline, top edge about 330 px, drawn fresh at full size, inside the safe area).
- **Three lines:** OXFORD UNI / RAP BATTLE / PART 1 (then PART 2, then PART 3). Fit them inside the safe width.
- **On screen for about the first second** over the moving picture (gone by 1.6 s at most), **never over a
  face.** If three lines cover a face in the opening shot of any part, use two lines at the standard size
  (OXFORD UNI RAP BATTLE / PART 1) or move the picture down a little, and tell me what you chose.
- The first frame doubles as the cover.

## The look and format
- The picture is the finished coloured-pencil film: don't redraw anything.
- **Vertical:** use the conversion in **`source/rap_vertical.py`** (read its current state first; I started it
  and it may need finishing):
  - the widescreen picture is enlarged by a third and sits in the middle of 1080 x 1920;
  - a soft glow of its own top and bottom edges fills above and below (no bars, no streaks, no blurred
    copy);
  - the old burned-in subtitles are removed and redrawn fresh.
- **Add a way to render a time range** (a start and an end), so each part is rendered separately. Check that
  the picture at each start time is identical to the same moment in the full film.
- **Make Part 2 and Part 3 consistent with Part 1:** the same framing, title and caption style.
- **12 or 24 fps:** the film is drawn at 8 drawings a second. Write the video at 24 fps, with each drawing
  held for three frames, unless that breaks something.
- **Size:** under 25 MB each. The pencil texture needs a fixed bitrate, so try about 2.2 Mb/s and check the
  result.

## The captions (word for word, our standard style)
- Every lyric line is captioned, from the script's punctuation (`source/data/rap_words.json`), whole line at a
  time, held until the next line starts.
- **Look:** bold white with a thick black outline, centred on the frame, wrapped to at most 700 px in balanced
  rows (no lone word on the last row), at most three rows.
- **Inside the safe area** (x 60-900, y 310-1500), just below the picture.
- Measure **every line of every part** from the script text and check that the widest fits.
- The flashing red **UNINTELLIGIBLE** sign (99.3-104.6 s, in Part 2) is drawn to fit the safe width; the
  single "FROG IN THE HOB?" flash stays.
- **A caption that is still on screen at a part's end** is cut at the cut to black.

## The sound
- The real battle audio plays exactly as recorded: volume only, no echo and no pitch change.
- Cut each part's audio from `source/audio/rap-battle.m4a`:
  - start and end in the gaps between lines;
  - add a short fade (up to 30 ms) at both ends so nothing clicks;
  - **scan each finished track for clicks.**
- Set the three parts to the same loudness: about -14 LUFS (a measure of overall loudness), peaks no higher
  than -1 dBTP (the loudest moment). Phones play dialogue best when it is even and clear.
- Keep any clean-up of the recording gentle, so no voice sounds underwater.

## Things to handle carefully
- **Strong language.** The battle is explicit (swearing and some very harsh lines about children, bodies and
  families). TikTok limits some videos with this kind of audio, especially in the first seconds.
  - **Part 1 opens clean:** its first lines have no swearing. Keep it that way.
  - Don't change or bleep anything without asking me (see the questions).
- **It is a parody rap battle between a penguin and a pigeon.** No real person is shown.
- **Keep the three parts in order and the same quality,** so a viewer who finds Part 2 first still gets it.

## How to work
1. Ask your questions (below) and wait for my answers.
2. Make **opening stills** of each part: the first frame (with the title) and the first caption, at phone
   size, with the safe-area guides drawn on. Send them and wait for my OK.
3. Render **Part 1** first (about 8-10 minutes). Send it, say how long it took, and wait for my OK before
   Parts 2 and 3.
4. Render Parts 2 and 3. Check each against the safe-area guides on the title, the widest caption and the
   busiest frame, and listen for clicks at the cuts.
5. **Deliver:**
   - send all three in the chat;
   - save them in animations/;
   - update story/status.md (the rap battle conversion note there now means this three-part plan; Sam's
     film is a later job);
   - suggest a cover frame for each part, with no spoilers.
   Do not suggest post text or a pinned question; I write those. You may point out a hashtag that would
   spoil a joke or limit reach.

## Questions to ask me (with your recommendation for each)
- **Captions:** keep every word as spoken, or star out the strongest swear words (for example "f***")?
  Recommend keeping every word, as the audio says them anyway, and so the captions stay accurate to what is
  said. If TikTok limits a part, we re-render it quickly with changes.
- **The harshest lines** (for example the "pedophile" line and the "child abuse" line):
  keep them, or mute those words on TikTok? Recommend keeping them for now: they are the parody's point
  and they are in the cartoon context of a pigeon and a penguin. If TikTok restricts a part, tell me what
  it says in your Inbox and I'll decide.
- **An "end tag":** a small "PART 2 NEXT" over the last half second of Parts 1 and 2? Recommend no.
  A cut to black is our usual ending, and I'll say it in the post text.
- **Anything to avoid** (people, jokes, symbols)?
