# TikTok design rules (CranbriJoos)

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
  - best: draw the captions fresh onto the vertical frame, wrapped to at most 800 px wide, centred on
    x = 480 (the middle of the safe area), just below the picture.

## The title card
- Bold Impact-style capitals (Anton), **cranberry red (178, 24, 52)**, letters widened 20%, thick black
  outline (`source/add_title.py`).
- On screen from the first frame, held 3 seconds, fading out over 1 second.
- **Large**: as big as fits within 90% of the width. A long title goes on two lines of equal size.
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
- UK evenings: post around 6-7pm, ahead of the 6-10pm peak.
- Post text: short and dry, with the title, a few specific hashtags (the people or topic being parodied,
  #animation, #parody or #satire), and a question that invites replies. Pin that question as a comment.
- Reply to comments in the first hour. Keep the next video ready within 24-48 hours.
- X gets the original widescreen version.

## Working (for Claude)
- **Say how long each render will take before starting it, and report how long it took.**
- **Send a push notification to the director's phone when each render finishes**, with what is ready
  and its size.
- Send finished videos in the chat so they can be saved to Photos; save finished versions in
  `animations/` with `-vertical` in the name for TikTok versions.
