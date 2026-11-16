# Helper A: the code finder misses

## Leak
Mild: the Facts point at two remedies ("a round chat knows [shot, time] when it fixes"; "module-level code ... never shown"). Weighed on evidence, not taken as given.

## Results
- Replay re-run today (replay-show.py): loose **18 of 26 (69%)**; misses 2, 9, 18, 30, 31, 35, 37, **44** (44, tvroom, is a miss the problem file does not list). Strict 7 of 14 (search-cost.md (e)).
- Learn run (scratch copy of the replay, nothing in the repo changed): the note's **shot name added to its words** gives loose **21 of 26 (81%)**, strict **9 of 14 (64%)**; it fixes 30, 31, 37, 44 but **breaks note 1** (shot "cast sheet" pulls `show` off HEAD_K). Shot helps, but mixed into the words it dilutes.
- Learn run (scratch): ranking module-level lines by the note's words naively does not land: note 2 gives HEAD_K, not the TUNE line; note 35 ties "will" with "shall". A naive table index will not reach the bar.
- Module-level statements are many: ~360 across Blessed and Protest Tiers files (grep count), e.g. blessed.py T[...] 118-141, LINES 65.
- Cost: hand searches 30% of steps in 7 round chats, est. 7-30% (middle ~15%) of their cost; the 6 Blessed round chats cost 12.72% of a week (search-cost.md (a)). So the whole prize is about **1-2% of a week per film**, plus fewer wrong-place fixes (unchecked: no fix in the record is known to have gone wrong because of a finder miss).
- Use: **0 `page.py` runs** in the 7 counted chats (search-cost.md); no round has run since `show` became the step (15 Nov). How often round chats actually use `show` is **not yet measured**: a gap.
- The test itself: 26 notes, one film, targets hand-read, code comments now name note numbers (kinder), note 18's target did not exist. The real edited lines were not kept; **they are now** (git history from 15 Nov), so the next round's own diffs give a true test free.

## The real decision
Not "tune one tool on 26 notes" but: how does a round chat, across every film, get from Sam's note row (shot, time, words) to the right lines in one step, and how do we know it does? Bigger levers than the word-matcher: the input the chat already has (shot and time), and a test that measures real rounds.

## Root cause
`show` sees only the note's words and only defs. Sam names what is on screen (shot, moment, word in a line); the code files the value under a code name inside a table, a constant, or one line of a long def. Nothing links shot names, script words or tables to the finder, and nothing measures it on real rounds, so misses went unseen until this replay.

## Approaches weighed
1. **Smarter matcher**: index module-level statements and score single lines inside long defs. Needed for notes 2, 9, 35; naive version shown not to land.
2. **Reframe: give it what the chat knows.** `show` takes the shot as its own input (not mixed into the words), and finds that shot's code from the film's own timing table, view table and `shot ==` branches, built from the code automatically (works first time on any film). Shown: +3 loose hits.
3. **Reframe at writing time**: each film's code keeps a shot-to-lines index in its MAP, written by the chat. Relies on chats keeping it current; rejected.
4. **Learn-first**: measure the next real round (stepcost.py kinds, git diff of the lines actually edited) before tuning further.

Chosen: 4 alongside, then 2, then 1, one at a time.

## Proposal
**Learn (changes nothing, can go now):** freeze the replay as a fixed test set with the shot and time columns, the four miss kinds labelled, note 18 scored as "shows the nearest like piece" (the other camera views). Then, after the next film's first round, harvest each note's real edited lines from git and add them; `stepcost.py` on that chat gives `page.py` runs vs hand searches.

**Change 1 (one yes):** `show` takes `--shot NAME` (the handover's per-note reminder fills it from the notes table); shot code found from the film's tables and branches; words and shot scored separately so note 1 is not lost. Enforced: the reminder prints the full command; the frozen replay runs inside `kittests.py`, so the score cannot silently fall. Must beat: loose 21/26 with no lost hit; strict ≥ 9/14.

**Change 2 (separate yes, after 1's result):** module-level statements and single lines inside long defs ranked. Must beat: strict ≥ 12/14 (80%+), loose ≥ 22/26, still ~40 lines.

**Real bar, at the film review:** ≥ 80% of the next film's notes answered by the first `show` (git diff vs its output), and hand searches under half of today's 30% of round steps (stepcost).

Cost: learn ~0.3% of a week; change 1 ~0.7%; change 2 ~1-1.5%; total ~2-2.5% once, for all films, against a saving of ~0.5-1% per film. Sam notices nothing on screen; rounds a little cheaper, fewer "fixed the wrong thing" repeats.

## Sam test
Q1: yes; measure real use and feed the tool the context the chat has, not just tune ranking. Q2: one film's replay is narrow; the harvest from real rounds widens it. Q3: kittests and the printed command make it happen every chat; the real-round bar shows if it worked. Q4: four different approaches weighed. Q5: each change undone alone; nothing asked on faith, each shown on the replay first. Q6: sources named; gaps marked. Q7: sized to reach 80%, not the cheap shot-word hack (which breaks note 1). Q8: permanent tool and test, reviewed at film end.

## Lost / Added
Lost: nothing. Added: a shot input to the one step; a fixed finder test in kittests; one harvest per round from git.

## Unchecked
Whether rounds now use `show`; whether any fault came from a finder miss; costs of changes 1-2 (estimates); Protest Tiers has no notes to replay.
