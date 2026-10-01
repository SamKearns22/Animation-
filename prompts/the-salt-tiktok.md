# Prompt: The Salt for TikTok (paste into a new **Claude Code** session on SamKearns22/Animation-)

Continue the animation project. First read CLAUDE.md, story/status.md and guides/tiktok-design.md, and follow
them exactly (plain English for me; make the choices yourself; render times up front and afterwards; a push
notification when each render finishes; send finished files in the chat).

**The job:** make the TikTok version of "The Salt" (source/salt.py; current video animations/the-salt.mp4,
17.4 s, 720 x 1280, 12 fps), polished to the standard of the rest of the account and built to hold viewers.

## What our first two posts taught us (30 Sept) - this film must fix it
- "Listening & Learning" and "Dam" got about 450 views each within hours, but **average watch time was only
  3.6-4.6 seconds** and only about 1.4% watched to the end. The retention graph fell off a cliff in the first
  3 seconds - while a big title sat over a still scene. The people who stayed liked, commented and saved: the
  jokes work; the openings lose people.
- A posted title also sat under TikTok's top tabs, and one caption ran off both edges of the screen.

## The rules for this film
1. **Sound and movement from the very first frame.** No held title card. Her line starts almost at once.
2. **The title** "THE SALT": small (about 40% of the width, inside the safe area, below TikTok's tabs, never
   over a face) while the action plays underneath, gone by 2 seconds. The full-size title goes on the
   **cover** only.
3. **A tighter timeline.** The current one, from salt.py:
   her line "Darling, would you pass the salt?" starts at 3.2 s; cut to him 7.6 s; "Of course!" 8.0 s; the
   camera whips back 11.9 s; he turns 12.9 s; pats 13.55 / 13.95 s; wind-up 14.25 s; SLAP 14.75 s; end 17.4 s.
   Aim for **about 11-13 seconds in all**: her line from about 0.3 s, the cut to him soon after she
   finishes, "Of course!" straight after, then the whip, pats, wind-up and slap with only the pauses the
   comedy needs. Keep a short deadpan beat after "Of course!" - that pause is part of the joke - and keep
   the rhythm of the pats, wind-up and slap exactly as it is.
4. **Captions** for both lines, burned in, every line inside the safe area (x 60-900, y 310-1500), wrapped to
   at most 800 px, measured from the script text itself.
5. **Keep** the joke, the recorded voices (darling.m4a, of-course.m4a), the sounds and the look; only the
   timing tightens.

## Steps
1. **Get it rendering again.** salt.py no longer runs ("cannot import name 'Canvas' from 'pencil'"): it
   imports Canvas, W, H, FPS, SR and more from source/pencil.py, which has since been changed. Find the
   version of pencil.py The Salt was last rendered with in the git history (around 26 September), bring it
   back under its own name and point salt.py at it, without changing what other scripts depend on. Check
   the first frames match animations/the-salt.mp4 before changing anything else.
2. **Iron out visual quality and consistency.** Make stills of every shot and review them at full size like
   a picky art director. Known so far: **the family coat of arms** on the wall behind the gentleman
   (crest() in salt.py) - the crossed pickaxes and the block of salt are slapdash. Redraw them with
   confident, clean shapes: proper pickaxe heads and handles crossed symmetrically, a clearly readable block
   of salt crystals, a well-proportioned shield with a firm outline, all readable at phone size. Then look
   for the same kind of problem everywhere: wobbly or unfinished shapes, uneven line weights, details too
   small for a phone, anything off-model between shots (the couple, the table, the room), and colour
   outside the food, the wine, the flames and the salt.
   **Send me one message with:** a sheet of before-and-after stills, and the proposed new timeline in
   seconds (old and new side by side). Wait for my OK.
3. **A quick animatic** (small and rough, with sound) of the new timing. Send it and wait for my OK.
4. **Render natively at 1080 x 1920** (not an enlargement of the 720 version), with the small title and the
   captions drawn fresh at full size. Under 25 MB (use a target bitrate if the pencil texture makes it
   large). Check the safe-area guides on the first frame, the widest caption and the busiest frame.
5. **Deliver:** animations/the-salt-vertical.mp4 - send it in the chat, save it on GitHub, update
   story/status.md, and suggest a cover frame (with the full-size title, no spoilers). Do not suggest post
   text or a pinned question - I write those.
