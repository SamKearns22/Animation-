# Prompt: The Salt for TikTok (paste into a new chat)

Continue the animation project. First read CLAUDE.md, story/status.md and guides/tiktok-design.md, and follow
them exactly (plain English for me; make the choices yourself; render times up front and afterwards; a push
notification when each render finishes; send finished files in the chat).

**The job:** make the TikTok version of "The Salt" (source/salt.py; current video animations/the-salt.mp4,
17.4 s, 720 x 1280, 12 fps, with the title "THE SALT"), polished to the standard of the rest of the account,
ready to post.

**0. The opening rule.** Follow the opening rules in guides/tiktok-design.md: no held title card; the first
frame moves with sound; the title at most 1 second or small over the action. Suggest where the set-up can be
tightened without losing the joke, and ask me before cutting.

**1. Get it rendering again.** salt.py no longer runs: it imports Canvas, W, H, FPS, SR and more from
source/pencil.py, which has since been changed. Find the version of pencil.py that The Salt was last
rendered with in the git history (around 26 September), and make salt.py use it without changing what other
scripts depend on (for example, bring the old version back under its own name and point salt.py at it).
Check the first frames match animations/the-salt.mp4 before changing anything else.

**2. Render natively at 1080 x 1920** (not an enlargement of the 720 version), untitled, then add the title
fresh at full size following the title rules in guides/tiktok-design.md: inside the safe area (x 60-900,
y 310-1500), below TikTok's tabs, never over a face.

**3. Iron out visual quality and consistency.** Before rendering the whole film, make stills of every shot
and review them closely at full size, like a picky art director. Fix anything slapdash; known so far:
- **The family coat of arms** on the wall behind the gentleman (crest() in salt.py): the crossed pickaxes
  and the block of salt are weak and scrappy. Redraw them with confident, clean shapes: proper pickaxe heads
  and handles, crossed symmetrically; a clearly readable block or heap of salt crystals; a well-proportioned
  shield with a firm outline. It must still read at phone size.
- Then look for the same kind of problem everywhere: wobbly or unfinished shapes, inconsistent line weights,
  details that don't read at phone size, anything off-model between shots (the couple, the table, the
  room), and anything that breaks the palette (greys, with colour only in the food, the wine, the flames and
  the salt).
- Send me a sheet of before-and-after stills for the fixes and wait for my OK before the final render.
- Keep the timing, the joke and the sound exactly as they are.

**4. Deliver:** animations/the-salt-vertical.mp4, 1080 x 1920, under 25 MB (use a target bitrate if the
pencil texture makes it large), checked against the safe-area guides on the title frame and the busiest
frame. Send it in the chat, save it on GitHub, update story/status.md, and suggest the post text, three or
four hashtags, a cover frame and a pinned question - following the no-spoiler rule.
