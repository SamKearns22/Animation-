# Sam's messages, chat cse_01U3pKQyiJ2poN3syCEWUzsu (handover.py log)

### 2026-11-25T17:23:19
# Seated legs (R7): Sam's notes on sheet v4, 25 Nov — handover to the R7 chats

Written by another chat (session_01GznaASxv3pZQm3sS8pLxQq) at Sam's request. Read this before any more R7 work.

## Sam's notes, in his words
- "Though they finally managed to give characters a bum, the legs look awful."
- "Building body kits is costing huge unacceptable expenditure and producing awful results. This cannot continue.
  Costs are out of control and work is substandard."
- "The approach to building these kits is wrong if it takes 27% of a week to fail to build normal seated legs on a
  simple model."
- He passed on Google's suggestion: build a stick skeleton with explicit joints first, then wrap volume and clothing
  around the bones, because raw hand-written outlines can't manage foreshortening (front view) or overlap (crossed legs).

His pictures (sheet v4, all four views, three people): `examples/sam-25nov-v4-legs-awful-1..3.jpg`.

## What the notes mean, view by view (my reading of his pictures)
- **Bum: accepted.** The seat and hips now read. Keep that.
- **Front:** the lap is a flat grey blob with a scalloped hem, sitting over two straight posts. It reads as a skirt
  over stilts, not thighs coming at the lens. The thighs should be short, wide and foreshortened, with knees as the
  nearest forms and shins dropping from under them.
- **Three-quarter:** the near thigh almost vanishes; the legs look like a standing person's legs behind a chair. The
  thigh must visibly run forward from the hip to the knee.
- **Side:** the least bad view, but the thigh-to-knee step is lumpy.
- **Crossed:** the top shin comes off the knee at a strange angle and the foot floats; the overlap of the top
  leg over the under leg doesn't read as one leg resting on the other.

## What I found (checked in the code and history)
- The rig is ALREADY skeleton-first: `sitting.realize()` solves hip, knee and ankle in 3D. So Google's advice is
  already in place, and more skeleton work will not help.
- What fails is the wrap. Chats 1–4 drew thighs and calves as hand-written curves (`views.leg`: thigh arch, calf,
  knee step, lap shading) and patched them view by view. Each patch fixed one view and broke or missed another.
  Sam's note is that this method is wrong, not that it needs another patch (rule 30: a note given twice means the
  first fix only patched the picture).

## Direction (not approved: it must go through the proposal route first)
- The likely fix is the GTA arm route: `arm3d_film` / `hand3d_film` put the measured MakeHuman body on our skeleton
  and draw it flat (house fill, ink outline, a crease where parts overlap). Legs and hips done that way get
  foreshortening and crossing overlaps from the 3D, in any view.
- Unknowns, said plainly: I have NOT checked whether Sam was happy with the 3D arms; trousers (cloth over the
  leg) were never solved by the arm work; and the cost is unestimated.
- Before building anything, run `propose.py new seated-legs-3d` (helpers, blind judge, top two with Lost/Added).
  An unjudged question to Sam is refused by the guard; it already stopped one today.
- **Cost:** one small test (the same 4 views × 3 people sheet) under a fixed cap set in the proposal. If the sheet
  isn't believable to a stranger by then, stop and tell Sam what is missing. Do not patch outlines again.

## Where things stand
- Rules that bite next: 30 (repeat note: fix the method), 85 (cost watch), 24 (budget stop).
- Done: Sam's notes and pictures saved here; no code changed.
- Next: Opus high, a proposal for 3D-body seated legs through the proposal route; then one numbered question to Sam.
- Needs Sam: nothing until the proposal is judged.
- Locked by Sam: no film shots involved (kit job). Keep the bum/seat shape he accepted.
- Read: this file; `guides/job-packs.md` (Plan); `source/arm3d_film.py` MAP only.
- Open rule requests: none.
- For Claude: R7 chats 1–4 on `claude/r7-seated-lower-body` (last: 45fcc6b3, 152bea67); seated code `source/sitting.py`,
  `source/views.py` (leg), sheet `notes/learn/seated/sheet_r7.py`.

