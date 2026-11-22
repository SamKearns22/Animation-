# Proposal: Speed up the bench test frames (grey and dressed) without changing a drawn pixel or a check

Status: open

## Problem
The test-space move (Jason leaning out of the car window and back, shot 4's 8.2 s, 197 frames) is too slow to make
and to remake. Sam needs to see it in motion, dressed in the house look, good enough for no notes, and every round
of fixes means re-making frames. Today a plain grey frame takes about 15 s and a dressed frame much longer, plus a
start-up of about 73 s on every run; a whole dressed clip is hours, and each small fix re-makes everything. Sam's
goal (22 Nov): "we just need to speed it up/make it quality so there's no notes." Nothing drawn or checked may
change: the same pictures and the same faults found on old frames.

## Facts
- Timings, this machine (4 processors, no graphics card; chat 38 found no bigger one offered), chat 39 (notes/bench/
  learn-step.md "Stage 1, chat 39"): grey frame ~15 s = fold press 10.1 s (inside the second body solve: the skin
  pressed out where it folds into itself at groin, armpit, neck), body-through-body check 1.8, pistol 0.1, other
  checks ~0, shot view drawing 1.3, outside view 1.6. Start-up ~73 s per run.
- Dressed still 105 s = start-up fits re-run inside it 65 s (fit_ankles 41, fit_knee 14.5, fit_seat 9: they give
  fixed numbers that never change unless the body, keys or car change; never saved), pose solve 16 (fold press),
  drawing both views at double size ~16 (triangle fill 6, house head drawn twice 5, outlines 1.8, clean_parts 1.6,
  compose 1.5).
- The inside test (is a skin point inside the closed skin?) is a winding-number sum over all 20,304 body triangles
  per point, already compiled with numba and run on all 4 processors (source/bench_move.py `_winding`, `_inside2`
  tests each point twice, 1.5 and 3 mm out). The body has 19,158 points. press_folds runs up to 8 rounds,
  `_settle` up to 10 rounds, each calling it; the self-cross check (self_cross) uses it too. (counted this chat)
- The triangle fill (source/bench_draw.py `raster`) is a Python loop over every triangle with small numpy grids;
  house_head draws the whole house figure twice (with and without the head) and keeps the difference.
- run() (bench_move.py) does every frame one after another in one process: solve, check, draw, save a PNG.
  span.py (notes/bench/span.py) re-checks a range of frames with no drawing; it re-runs the three fits each time.
- Frames are not kept between chats (scratch is lost when a chat ends); each chat re-makes what it needs.
- The checks are the bar for the move: car(), self_cross(), pistol(), ranges(), contacts, jumps (bench_move.py
  CHECKS); proof() re-runs them on old failed frames (notes/bench/proof.txt).
- Files: GitHub files must stay under 50 MB (CLAUDE.md). Installed: numba 0.68, numpy 2.5, scipy 1.18, opencv 5.1,
  pillow 12.3; no mesh-distance package installed (unchecked whether one installs here).
- Sam's Y (22 Nov evening, notes/grand-theft-autism.md "Sam's decisions"): to be weighed in the route: a distance
  grid for the inside test (exact test kept near the skin), compiled triangle fill, house head once, 4 frames at a
  time, saved start-up fits; and his three: quick checks with no drawing over all frames first, then ONE render;
  redraw only the frames a fix touches, spliced into the last clip; keep rendered frames between chats (a compact
  bundle on GitHub).
- A full grey run was estimated at ~80 min (learn-step chat 39).

## Record
source/bench_move.py
source/bench_draw.py
source/bench_pose.py
notes/bench/learn-step.md
notes/bench/span.py
notes/grand-theft-autism.md
CLAUDE.md
