# Prompt for the next session: animate 'Merry Chr'

Continue the Yuletide project on this branch. Read `CLAUDE.md`, then `story/status.md`, then
`story/horror-merry-chr.md`, and the guides it names (`guides/tone.md`, `guides/movement.md`,
`guides/pipeline.md`, `guides/character-anatomy.md`). The latest still is
`animations/yuletide-merry-chr-still.jpg`; the recipe is `source/shots/h1_merry_chr.py`.

Animate the 'Merry Chr' horror shot. The camera, room and everything in it stay exactly as in the
still: the camera never moves; nothing in the room moves except what is listed here.

**Length:** 3 seconds at 24 frames a second (enough to test the loop; in the trailer it will be cut to about
1 s). Draw on twos, but the strikes on ones.

**The man (the only thing that moves):**
- He slams his forehead into the r, again and again, like a machine: pull back 6-8 cm from the neck and upper
  back, a short hold, then the strike. A strike every 0.9 s, the same rhythm every time (robotic, not
  frantic). Controlled force: the strike is fast (2-3 frames), then a small recoil (1-2 cm) and settle; his
  shoulders give a tiny jolt with each impact; his arms hang dead and barely sway. No other movement - no
  breathing show, no looking round. Checks: his forehead meets the wall at contact, never passes into it.
- Follow `guides/movement.md` for easing (slow out of the hold, no easing into the impact).

**The blood at the r:** grows a little with every strike - the blotch spreads, a fresh ring of spatter flies
out, one or two new drips start down the wall and lengthen over the next frames. Everything else on the wall
is dry and still.

**The fairy lights:** both strings (the back wall and the right-hand wall) flash in a broken, stuttering way,
each bulb from `merry_chr.bulb_lit(i, t)`; a few stay dead. Their glow on the wall flickers with them.

**Sound:** the THUD of each strike exactly on the impact frame, dull and close, over the trailer score at
its most distorted (`music/horror-trailer-score.m4a` - pick the most insane passage). The THUDs are the
loudest thing.

**How to work (budget):**
- Only the man, the blood at the r and the lights change, so use the partial redraw in `shot.py sequence`
  (render and redraw only the changed patches). The drawing uses this shot's `exposure`, `frame_depth` and
  `contrast_budget` settings - keep them.
- Make a quarter-size animatic first (no pencil pass), check the timing and the contact, and only then do
  the full render. Render in the background and report once at the end.
- Finish with an MP4 under a few MB in `animations/`, sent to me in the chat.

**Small faults to fix on the way (from the still):**
- His short grey hair still draws as a pale patch; it should read as a dark, close-cropped head of hair.
- A few toiletries and one torn suitcase lid don't fit on the floor and are left out - fine unless there is an
  easy place for them.

Update `story/status.md` at the end.
