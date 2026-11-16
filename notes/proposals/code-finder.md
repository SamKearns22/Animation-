# Proposal: The code finder shows the wrong lines for a third to half of Sam's notes

Status: open

## Problem
In a round of Sam's notes, the chat looks at the code for each note with one step, the code finder
(`python3 source/page.py FILM show "note words"`, about 40 lines). When those 40 lines do not hold the place the fix
needs, the chat falls back to hand searches (grep, ranged reads), each of which is then re-read at every later step of
a long chat. Replayed on 26 old Blessed notes, the finder held what the fix needed in only 69% (loose score) and 50%
(strict score, distinctive names only); the bar set for it is 80% on both. The misses fall in four kinds: the value
lives in a table or constant, not a function (a face setting in a TUNE table, the script's LINES list); the setting is
one line inside a long function and the 40 lines showed the function's start instead; the note names the shot or the
moment, not the thing in the code (the shot gates2, the dock); the code did not exist yet (a new shot to be added).
Every film is new, so whatever changes must work on a film's code the first time, with no per-film hand lists; quality
of fixes must not fall, and the finder must stay one step of about 40 lines.

## Facts
- Replay method and scores: notes/proposals/learn/search-cost.md section (e); script notes/proposals/learn/replay-show.py
  (fixed per-note target words T, hand-read from the fixes). Re-run today (16 Nov, chat 8): loose 18 of 26.
  Strict 7 of 14 (hits 1, 12, 19, 27, 32, 38, 45; misses 2, 9, 18, 30, 31, 35, 37).
- The replay feeds the finder only the note's words. The notes table (notes/archive/blessed-notes-animatics-1-2.md,
  columns: # | shot | time | note | line | status) records a shot name and a time span for every note; a round chat
  knows these when it fixes. Example: note 30, shot gates2, 49.45-53.6 s, "Walliams is not a new shot: he goes in the
  BACKGROUND..."; note 35, shot oath2, 10.4-14 s, "change the second shall to will".
- Where the missed targets live (grep, 16 Nov): chin_long: source/blessed_cast.py:65, a module-level line
  `P4.TUNE['brand'] = dict(..., chin_long=4.0, ...)`; ears_hidden: blessed_cast.py:666, one argument inside a long
  function; LINES: blessed.py:65, a module-level list of the script's lines (the word "shall" is inside it); the shot
  names: blessed.py:185-197 (a shot timing table, VIEW = {'dock': 'court_dock', ...}, who is in each shot), `def dock`
  at blessed.py:877, `def gates2_head` at :1310, shot branches like `if shot in ('tvroom', 'push'):` at :1704/:1763;
  T['tvroom'] timing values at :133-134.
- How the finder works today (source/page.py, 213 lines): build() writes story/FILM-page.md (each def's name, line and
  first docstring line, plus people/places/moves lists); find() scores page lines by shared words (3+ letters, plurals
  folded, a stop list); show() rescores the top 12 by words inside each def's body, prints the best def whole or its
  first 6 lines plus lines holding the note's words, runners-up' first lines, then FILE:LINE. Module-level code
  (tables, constants, assignments outside a def) is not on the page and never shown.
- The current code carries comments naming note numbers ("note 18: cot_top"); a replay on today's code is therefore
  slightly kinder than the round was. Git history starts 15 Nov, so the lines actually edited are not kept.
- Cost context (search-cost.md (a)): hand searches were ~30% of steps in 7 counted round chats; estimated 7-30% of
  their cost, middle ~15%. Blessed code: 8 files, 410k characters; blessed.py 117k.
- Other films' code the finder must also serve: source/protest_tiers*.py (same shape: defs, module tables).

## Record
source/page.py
notes/proposals/learn/search-cost.md
notes/proposals/learn/replay-show.py
notes/archive/blessed-notes-animatics-1-2.md
source/blessed.py
source/blessed_cast.py
source/protest_tiers.py
story/blessed-page.md
