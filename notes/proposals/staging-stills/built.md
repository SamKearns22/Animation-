# staging-stills: what was built (source/staging.py)

## Built (22 Nov, Milburn lessons chain B chat 1, Opus high)
- Step 1 (the look back): notes/proposals/staging-stills/learn.md. 5 staging repeats, all built before Sam saw a board
  (Milburn 2, Patriots 4 1, Blessed 1, EPR 1): the step-2 gate (2 or more) is met.
- Step 2: `source/staging.py` (the hold record story/FILM-staging.txt; restage, options, sent, pick, notframing, check).
  Switched on in `source/film_engine.py` render (every clip: its shots checked) and `source/rough.py` board_gate (the
  animatic's pre-flight); `rough.py board FILM OUT.jpg --shots A,B` draws a re-staged shot alone. Job pack "Notes
  round" names it. Kittests `staging_stills_milburn_replay` (chat 6's and chat 10's builds refused; the fixed flow
  passes) and `staging_stills_note_finder` (all 29 framing notes in four films found; 52 of 205 notes flagged).
- Found while building (named): the judge's "picture fingerprint" cannot tell a re-stage from a move (the board's
  digest is of rendered frames, which change with every pose), so a held shot is released by Sam's number plus a new
  board of that shot, not by comparing fingerprints. Not covered: a chat changing a framing on its own with no note;
  movement code written for a held shot (it cannot be rendered or sent). Films begun before the shot board are not
  gated; Grand Theft Autism renders with its own code (Sam overruled its checks, 21 Nov) and is not gated.
- Rule 11 and 87 wording: written 23 Nov on Sam's "Y to all" (05:51 UK, chat 3, notes/ledger/sam/vs4pf9aa.md).

## Verified working (23 Nov, Sam: "Y then test and verify working")
- End to end on the main line, a made-up film through the real clip command: refused with no board; renders once a
  board reached Sam; refused for an unrouted framing note; refused while held, with the sheet sent but no number, and
  after his number until the shot's new board; renders after the new board; `staging.py check` then clean.
- The made-up film's clip file came out empty (its own test sound, not the check: the check runs before any drawing).
  A real Milburn clip (0-0.5 s) with the check in place: 0.98 s, 540x960, 24 fps, body check clean.
- Kittests on the merged main line: staging_stills_milburn_replay, staging_stills_note_finder, board_gate_refusals,
  board_gate_milburn_reverse, shot_board_every_shot, watcher_catches_last_weeks_four all PASS.
