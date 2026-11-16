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

## Verdict (the judge, word for word)
<!-- verdict-hash: 2ba6e3820bcd1d61 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = helper A, V3 = chat. Picked: V2 (helper A). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: a hint, not a stated fix. The Facts list where each missed target lives (tables, one line in a long def, shot tables) and say "a round chat knows these [shot, time] when it fixes", which points straight at "index module-level code and add a shot input". The record it lists (search-cost.md (e)) states that fix outright ("rank tables and shot names; show lines holding a note's words"). All three versions landed on it; V1 and V2 said so and tested it, V3 took it as given.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 4 | 4 | 4 | 4 | 5 | 21 |
| V3 | 3 | 3 | 2 | 2 | 4 | 14 |
## Sam test
Q1: Yes, with V1's additions: an expert feeds the tool what the chat already knows (shot, time), measures on notes it was not tuned on, and logs real use. The final version does all three.
Q2: The 26-note replay is one film and hand-picked targets (kinder now: code comments name note numbers). The real bar is the next film's own notes, scored against the lines actually edited (git keeps them since 15 Nov), frozen before anyone tunes on them.
Q3: Root cause shown (only defs and only Sam's words reach the finder). It happens every chat because the replay sits in the kit tests (a score drop fails them) and the handover check lists notes fixed without the finder or with hand searches after it. Paper compliance is caught by the use log.
Q4: Four approaches weighed (smarter matcher, shot input, shot index written by chats, learn first); the chat-written index rejected as it relies on chats keeping it current.
Q5: Two changes, each its own yes, each shown on the replay before it is asked; each undone alone (old calls keep working). The table/long-def change is not asked until it is shown, because the naive version was shown to fail (notes 2, 35).
Q6: Checked here: replay 18 of 26, misses include 44; each show prints 52-60 lines, not 40; note 1's shot is "cast sheet"; 0 page.py runs in the 7 counted chats; kittests.py and stepcost.py exist. Costs and the per-film saving are estimates and marked so.
Q7: Sized to reach 80% on unseen notes, not the cheap "add the shot to the words" (shown to lose note 1).
Q8: Permanent tool change and permanent test; reviewed against the next film's results at its end-of-film review.
## Pick
V2
## Why
V1 and V2 are close; both re-ran the replay, both found that the shot helps (+3) but breaks note 1 when mixed into the words, both split the work into separate yeses with bars. V2 wins on: the true target (lines actually edited, from git, instead of hand-read words), enforcement in the kit tests, a tested finding that a naive table index does not land (so its change 2 is costed honestly at 1-1.5%), and cleaner undo (no new coupling into the handover). Taken from V1: a held-out set frozen before tuning; the use log checked by the handover (V2 relied on a later count only); the line budget (show already prints 52-60 lines; must come back under 45); the "nearest shot to copy" answer for code that does not exist yet. V3 bundles four parts into one yes, adds the shot as a word (shown to lose note 1), states no cost and no real-use measure.
## Faults in the pick
- F1 [fixed] No held-out test: tuning on the same 26 notes could reach 80% and still miss on the next film. Added a frozen held-out set from the next film's first round.
- F2 [fixed] Use not enforced at the moment of use: added the one-line use log and the handover listing.
- F3 [fixed] show already overruns its ~40 lines (52-60): bar now includes under 45 lines.
- F4 [named] Git diffs can mix several notes in one commit; matching edited lines to a note needs each fix commit to name its note number (the chats already write "note N:" comments).
- F5 [named] Whether any wrong fix ever came from a finder miss is unchecked; the gain is mostly speed (~1-2% of a week per film, estimated), so payback is about two films.
- F6 [named] Protest Tiers has no notes to replay; works-first-time on a new film is shown only by the held-out set.
## Final version
Learn (no film change, ~0.3% of a week): freeze the 26-note replay with shot and time columns and the four miss kinds; note 18 scored as "shows the nearest like shot". Put it in kittests so the score can never silently fall. After the next film's first round, before any tuning, freeze its notes as a held-out set, targets = lines actually edited (git, matched by the "note N" in each fix).

Change 1 (own yes, ~0.7%): show takes --shot NAME (and --at SECONDS). Shot names count only if found as string keys in the film's own code (timing table, view table, `shot ==`/`in` branches, `def SHOT`), built automatically. Shot and words are scored separately so a non-code shot ("cast sheet") cannot push out a word hit. When the shot is not in the code, show names the nearest existing shot's code to copy beside. The handover's per-note reminder prints the full command. Every call writes one line to the film's notes log; handover.py end lists notes fixed with no show call or with hand searches after it. Bar: loose at least 21/26, strict at least 9/14, note 1 kept, note 18 hit, under 45 lines.

Change 2 (own yes, asked only after it is shown, ~1-1.5%): module-level assignments (tables, constants, X['k'] = ...) go on the page with their keys and string words; inside a long def, lines holding the note's words come before the head. Bar: strict at least 12/14, loose at least 22/26, under 45 lines.

Real bar, at the next film's review: at least 80% of held-out notes answered by the first show, hand searches under 15% of round-chat steps (from 30%, stepcost). Total ~2-2.5% of a week once, against ~1-2% saved per film (estimated).
## For Sam
### Option 1: Give the finder the shot, then the tables, tested on the next film
When a chat fixes one of your notes, it first asks a finder tool to show it the right bit of the film's code. Today it shows the right bit only half to two-thirds of the time, so the chat goes hunting by hand, which is slow and costly. The fix: the chat tells the finder which shot your note is about (it already knows), and the finder learns to look inside tables of settings (a "table" here is a list of values like face sizes or the script's lines). Each part is shown working on your old Blessed notes before you are asked, then judged on the next film's real notes. You would notice nothing in the films; rounds get a little faster and cheaper.
Lost: nothing in the films; one extra line logged per note fix.
Added: the shot passed to the finder, settings tables findable, a fixed test, and a check at each handover that the finder was used.
### Option 2: Same changes, one yes, no new test
All the same finder improvements built at once and tried on the old notes only, with no test on the next film and no record of use. Quicker to ask, but one test showed adding the shot the simple way breaks a note that used to work, and nothing would tell us if chats stop using it.
Lost: the proof on a new film; the separate yes for each part.
Added: the same finder improvements, sooner.
