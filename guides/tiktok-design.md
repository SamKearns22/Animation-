# TikTok design rules (CranbriJoos)

The lessons from every film are collected in `guides/best-practice.md` (the master file); this guide holds
the TikTok details.

Use these for every video made for TikTok, in any chat. They can be pasted into a prompt as they are.

## Account
- Name **CranbriJoos**, handle **@cranbrijoos** (the same on TikTok and X). Bio: **no comment.**
- Profile picture: the beaver close-up in white fire (`profile/`).
- Identity: deadpan comedy animation. Comedy is set-up and payoff: never open on the punchline, and never
  put text on screen or in the post that gives the joke away.

## The video file
- **1080 × 1920 (9:16), MP4 (H.264, AAC), 12 or 24 fps.** Under 50 MB; aim for well under 25 MB.
  Pencil-textured films need a target bitrate (about 3.4 Mb/s for 45 s gives ~20 MB); flat cartoon styles
  are small at CRF 20.
- **Made vertical from the start where possible.** A widescreen (16:9) film is converted like this:
  - scale it up so the picture is about a third larger than simply fitting the width, cropping only empty
    background at the sides - first measure how wide the figure and captions ever get, so nothing
    important is cut;
  - the picture sits in the middle of the frame, **untouched**;
  - above and below: a soft glow made from a heavily blurred copy of the picture's own top and bottom
    edges, fading into the scene's background colour (no hard bars, no stretched streaks, no blurred
    zoomed copy of the picture).
- **Keep clear of TikTok's own overlays** (measured on a real post, 1080 x 1920 frame):
  - **top 16% (0-310 px):** the LIVE / Following / Friends / For You tabs and the "Story" button;
  - **right-hand 16% (x > 900 px), from about 45% down:** the profile picture, like, comment, save and share
    buttons;
  - **bottom 22% (y > 1500 px):** the username, post text, promotion button and progress bar.
  - So the **safe area is x 60-900, y 310-1500**. Titles, captions and faces must stay inside it.
- **Captions** for any speech, burned in, readable on a phone, **every line inside the safe area**:
  - never trust captions burned into a widescreen original when enlarging it - measure the widest line
    from the script text itself (every line, not sampled frames: sampling missed the longest line and it
    ran off both edges of a posted video);
  - best: draw the captions fresh onto the vertical frame, wrapped to at most 700 px wide (balanced rows),
    centred on the frame (x = 540), just below the picture or the faces (director's choice on The Patriots).

## The title card
- Bold Impact-style capitals (Anton), **cranberry red (178, 24, 52)**, letters widened 20%, thick black
  outline (`source/add_title.py`).
- **Never a held title card on TikTok.** Our first two posts (Sept 30) lost most viewers in the first 3
  seconds - average watch 3.6-4.6 s - while the title sat over a still scene; the retention graph fell off a
  cliff there. So:
  - **the first frame moves, with sound from the start** (the story begins at once - still never the
    punchline);
  - the title is on screen **at most 1 second**, or sits **small** (about 40% of the width, high in the safe
    area) while the action plays underneath, fading after 2 seconds;
  - the director prefers the **same title size on every film** (Anton at about 200, which makes capitals
    about 148 px tall, as on Dam and Listening & Learning), so the in-video title is full size and on screen
    for about the first second only (gone by 1 s, 1.6 s at most);
  - the full-size title lives on the **cover** (chosen when posting) and in the post text instead.
- **Tight set-ups:** TikTok viewers give a video seconds, not minutes. Cut the set-up to the shortest version
  that still lands the joke (aim for 15-30 s in all; the first payoff or turn within about 8-10 s).
- On the cover: as big as fits within the safe width. A long title goes on two lines of equal size.
- **Standard title size** (so the profile grid matches): capitals about 148 px tall per line, as in
  Listening & Learning (`title_lines` in `source/burnham.py`); two words go on two lines. On TikTok it is
  shown at this size on the opening frame for 1 second at most, over moving picture, so that frame can be
  picked as the cover; never over a face (open on background and move to the character as it fades).
- **Placed in empty space inside the safe area**, never over a face and never in the top 16% (TikTok's
  tabs cover it - a posted title sat under them): in a converted widescreen film, just above the picture,
  its top edge no higher than 330 px; in a film made vertical, a third of the way down, over background.
  Fit it within the safe width (840 px), so it may be a little smaller than the full frame width.
- **Check before posting:** overlay the safe-area guides on a frame from the title, the widest caption and
  the busiest moment, and look at it.
- Always drawn fresh at 1080 × 1920 (never an enlarged copy of a smaller title), onto an untitled render.

## Cover
- Chosen in the TikTok app when posting ("Edit cover"): a frame that intrigues without spoiling the joke,
  ideally the character mid-line. It cannot be changed after posting.

## Posting
- UK evenings: post around 6-7pm, ahead of the 6-10pm peak. **Under test:** Sunday about 9am (Mossad's slot; Buffer's data).
  The evidence on timing is weak and mixed: see `guides/tiktok-posting-research.md` before changing this.
- Post text: short and dry, with the title, a few specific hashtags (the people or topic being parodied,
  #animation, #parody or #satire), and a question that invites replies. Pin that question as a comment.
- **The director writes the post text and the pinned question himself. Claude never suggests lines or wording
  for them** (it can still suggest a cover frame and point out if a hashtag would spoil the joke).
- Reply to comments in the first hour. Keep the next video ready within 24-48 hours.
- X gets the original widescreen version.

## Working (for Claude)
- **Say how long each render will take before starting it, and report how long it took.**
- **Send a push notification to the director's phone whenever a render or any other long process
  finishes** - full renders, animatics, storyboard or mock-up sheets, sound builds, uploads to GitHub,
  research: anything that takes more than a couple of minutes, since the director is often away from the
  chat. Say what is ready, its size or result, and how long it took. Also send one if a long process fails
  or stops to wait for a decision, saying what is needed.
- Send finished videos in the chat so they can be saved to Photos; save finished versions in
  `animations/` with `-vertical` in the name for TikTok versions.
