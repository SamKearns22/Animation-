# Helper B: the code finder misses

## Leak
Partial. No solution is stated, but the file picks the frame ("the finder must stay one step of about 40 lines") and lists the four miss kinds and the shot/time column in a way that points at "rank tables and shot names". search-cost.md (e) says the same outright. I treated both as facts to test, not as the answer.

## Results
- Replay re-run today: loose 18 of 26 (69%), strict 7 of 14 (50%), misses 2, 9, 18, 30, 31, 35, 37 (plus 44 on loose) (replay-show.py, run here).
- Each `show` printed 52-60 lines, ~1,000-1,250 tokens, not 40 (replay output). The ~40-line budget is already being exceeded.
- My test: adding the note's shot name from the notes table to the words: strict 9 of 14 (64%). It gained 30, 31, 37 (and 44 on loose) and LOST note 1 (HEAD_K: "cast sheet" is not a code shot, and its words pushed the right def out). So the shot column is worth about +3 notes on its own, not a cure, and a blunt version causes a regression.
- Hand searches: 30% of steps in 7 round chats, cost share 7-30% estimated, middle ~15%; Blessed round chats 12.72% of a week (search-cost.md (a)). So the prize is roughly 1-2% of a week per film, estimated.
- Gap 1: those 7 chats ran `page.py` 0 times (search-cost.md (a)). Whether round chats use `show` since 15 Nov, and how often a hand search follows it, is not in the record. The finder's hit rate is the proxy; the result is hand searches per note.
- Gap 2: all 26 test notes are from one film and the targets were hand-picked by the same chats that would tune the finder. Any fix tuned on them can score 80% and still miss on the next film. There is no held-out test set.

## The real decision
Not "make `show` rank better" but "how does a round chat get from Sam's note to the lines it must edit, on a film's code it has never seen, with the fewest searches, across every round of the film". Bigger levers than the ranking: what the chat feeds the finder (the note's whole row, not just its words); whether chats actually use it; and how the next film is measured.

## Root cause
The page is built only from defs and their docstrings (page.py build/find). Three of the four miss kinds follow directly: module-level tables and constants are never on the page (2, 35); a long def is cut to its first 6 lines, so a setting deep inside is shown only if the note's words are on that line (9); and the note is scored by Sam's words, while the code is organised by shot names he rarely says (30, 31, 37, 44). The fourth kind (18, new code) has no target to find; the right answer is the nearest pattern to copy, which the finder does not try to give. Nothing was tried before on `show` itself; it failed its first measurement.

## Approaches weighed
1. **Rank better from words:** put module-level assignments on the page, show lines matching the note inside a long def. Fixes 2, 9, 35; not the shot notes.
2. **Reframe: feed the note's row.** `show` takes the shot and time from the notes table; a shot name that exists in the code (found automatically from the code's own string keys) adds that shot's def, its table entries and its `if shot ==` branches. Fixes 30, 31, 37, 44; must not let a non-shot like "cast sheet" score.
3. **Reframe at build time:** new films keep each shot's settings in one shot table, so a note maps to code by its shot. Strong, but untested and changes how every film is written.
4. **Learn first:** log every `show` call and whether the next step was a hand search; score on the next film's real notes, not the tuning set.

Chosen: 4 first, then 2 and 1 as separate changes. 3 waits for evidence from 4.

## Proposal
**Learn (no change, ~0.3% of a week):** keep the 26-note replay as a fixed test; freeze its targets in a file so later changes cannot edit them; add a held-out set taken from the next film's first round before anyone tunes on it.
**Change 1, row input (~0.7%):** `show` takes `--shot NAME`; only names found as string keys in the film's code count. Bar: strict at least 10 of 14, no hit lost (note 1 kept).
**Change 2, tables and long defs (~0.7%):** module-level assignments go on the page; inside a long def, matching lines come before the head. Bar: strict at least 12 of 14 and loose at least 22 of 26 (both over 80%), and each `show` back under 45 lines.
**Change 3, new code (~0.5%):** when the shot is not in the code, `show` names the nearest existing view to copy. Bar: note 18 hits.
**Change 4, use (~0.5%):** `show` writes one line per call to the film's notes log; `handover.py end` lists notes fixed with no `show` call or with hand searches after it. Bar: on the next film, at least 80% of notes fixed from `show` alone, and hand searches under 15% of round-chat steps (from 30%).
Each is its own yes, measured alone, and undone alone. Total ~2.7% of a week once, against an estimated 1-2% saved per film. Sam would notice nothing in the films; rounds come back a little faster and cheaper.

## Sam test
Q1: An expert measures on held-out data and on real use, not on the tuning set; this does both.
Q2: Scope is every round of the next film, not one replay.
Q3: Change 4 makes skipped use show up at handover; it does not rely on a chat choosing to follow it.
Q4: Four different approaches weighed; build-time layout held back for evidence.
Q5: Each change is small, measured and undone alone; nothing ships without beating its bar.
Q6: Replay and shot-name test run here; costs marked estimated.
Q7: Sized to reach 80% on unseen notes, not to the cheapest ranking tweak.
Q8: Each change is permanent once its bar is met, and reviewed when the film is complete.

## Lost / Added
Lost: nothing in the films; one more line in each round's notes log.
Added: a frozen test set, a shot input, tables on the page, a use report at handover.

## Unchecked
Whether round chats since 15 Nov use `show`; per-film saving (estimated); my shot-name test used a single run on today's code, which carries note-number comments.
