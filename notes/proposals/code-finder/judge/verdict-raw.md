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
