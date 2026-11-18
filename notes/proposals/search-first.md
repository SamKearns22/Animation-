# Proposal: Chats search by hand and re-load tools instead of using the finder; cost is a guess, not the app's figure

Status: open

## Problem
Sam's goal is that every film costs 15% of a week or less. Milburn came in at 22% by Sam's own reading of the app
(71% to 93%); the ledger said 32.14%, because every row is a guess from the chat transcript, not the app's figure.
Three things drove the spend. (1) The code finder (page.py show) was built to answer "which lines does this note
touch" in one step, yet chats searched the code by hand about 20 times as often as they used it, in every chat, even
after a reminder was added at the moment of a hand search. (2) Chats loaded tool definitions one by one, hundreds of
times, with no one-page list of which tool does which job. (3) The film's cost is only known after the fact and only
by guess, so nobody can steer against 15% while the film is made.

## Facts
- Milburn ledger (notes/ledger/milburn.json, 15 chats, 17-18 Nov, 1,259 steps, all rows src "estimate", none from the
  app): recorded 32.14% (Opus 29.15, Sonnet 2.99); Sam's manual reading 22% (71% to 93%).
- Finder (page.py show) used 12 times in total (calls.page.py). Hand searches of film code: 248 (calls film-file
  search), split by the ledger as: 74 in chats with no show call, 13 before the chat's first show, 43 within 10 calls
  after a show (a miss), 118 later after a show.
- Cost by kind (estimates): other 21.4 points (mostly re-reading history, 200-300k words by the end of a chat), tool
  search 5.27, film-file search 2.77, pictures 1.64, renders 0.81.
- Tool-search calls: about 531 in the 15 chats (11 to 82 per chat). No tool-map page exists in the repo; kit-catalogue
  and job-packs list tools in prose.
- Other searches in the same chats named shared tools: facehouse.py 30, critique.py 29, people.py 27,
  people_parts.py 23, handover.py 23, acting.py 20, preflight.py 18. The finder covers only the film's own
  source/FILM*.py.
- A per-chat reminder at the first hand search was added 17 Nov (commit 64f19a94, notes/proposals/finder-use.md).
  Finder use rose in the later Milburn chats (0 uses early; 2 to 3 per chat in the last four Opus/Sonnet round chats)
  but stayed far below hand searches.
- notes ticked is 0 in every Milburn ledger row, so per-note search rates cannot be computed.
- notes/ledger/app-costs.tsv (the app's real per-chat cost) was last filled 15 Nov; no Milburn row; the import is
  `ledger.py app`. The automatic Stop hook writes a transcript estimate.
- Earlier: 16 Nov, 19 Protest Tiers chats, hand search 6.65% + 3.22% of a week vs finder 0.21% (finder-use.md).
- Sam, this chat: the 24% estimate should not have been judged against partial scripts; chat length (about 100, up
  to 150) and model-by-stage rules stand and are not under review; the 15% goal applies to every film.
- Unchecked: the real app cost of each Milburn chat; how many hand searches sit in build chats (legitimate) versus
  note rounds; why the 17 Nov reminder did not change behaviour.

## Record
notes/ledger/milburn.json
notes/ledger/milburn.md
notes/ledger/app-costs.tsv
notes/proposals/finder-use.md
notes/proposals/code-finder.md
notes/proposals/early-warning.md
notes/proposals/history-and-search.md
notes/logs/milburn-show.log
source/page.py
source/ledger.py
source/stepcost.py
source/handover.py
guides/kit-catalogue.md
guides/job-packs.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 4c773f7fc9263366 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V2 (helper B). Critiqued: 8 found, 5 fixed, 3 named.

## Leak
yes: the title names two remedies ("use the finder", "the app's figure"), and the facts hint a third ("No tool-map page exists"). Problem (2) also states as fact that chats "loaded tool definitions one by one, hundreds of times"; the record does not support this (in source/stepcost.py kind_of, "tool search" is any grep or partial read of a non-film file; the 531 split 328 shared tools, 101 other, 81 film notes, 21 guides, summed from milburn.json). V3 took the leak and the misreading as given.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 4 | 3 | 4 | 18 |
| V2 | 4 | 3 | 4 | 4 | 4 | 19 |
| V3 | 2 | 2 | 2 | 2 | 3 | 11 |
## Sam test
Q1: Yes: an expert first gets the real figure, then steers the whole film on it, and measures where tokens go (history, build) before policing one habit.
Q2: Scope is the whole film, all 15 Milburn chats with the app's figures, Protest Tiers for comparison; build overrun and history are in view, not only searches.
Q3: The real figure is enforced by a refusal in the handover check, and an over-15% forecast forces a re-plan in the next chat's start check; the failed reminder is explained (advisory, aimed at note rounds while most chats were building). Number to beat is stated.
Q4: Four approaches weighed (force the finder, trim history, steer on the real figure, learn first); the frame was corrected from searches to whole-film cost.
Q5: Learning changes nothing; Change 1 is one yes and undoes alone; later changes come back to Sam as their own proposals.
Q6: Facts checked: 32.14 vs 22, 67% other, the 531 split, stages 29.43 spent vs 3.4 planned, the ignored "lands at 100.4%" forecast, WEEK_USD marked PROVISIONAL, no Milburn app row. Unchecked items listed.
Q7: Sized to the levers that carry the money (build overrun, history), not the cheapest search fix; states plainly that search fixes alone cap at about 3 to 4 real points.
Q8: Change 1 is permanent and reviewed when the next film is declared complete; nothing is a trial.
## Pick
V2
## Why
V2 checks its facts, catches the misread "tool search" figure, and finds the two real levers: building ran 8.7 times its plan (29.43% spent against 3.4% planned for sets, props, build and board) and a forecast of 100.4% was printed and ignored. Its main change works at the whole-film level and forces action, not advice. V1 is close and also catches the misreading, but it pre-commits a blocking search hook inside the same yes and ignores the build overrun. V3 rests on the misreading, bundles three changes, and keeps the advisory pattern that already failed.
Taken from V1: re-setting the provisional week constant from the paired figures (this also fixes every chat's live cost warning), labelling repeat look-ups of the shared kit across chats, and the honest sum that search fixes alone cannot reach 15%.
Added by the judge: re-size the stage plan from real build costs; record a real stage per ledger row; later changes return to Sam separately; the re-plan may never cut content.
## Faults in the pick
- F1 [fixed] V2's root cause 2 (build plan of 3.4% not sized to real cost) had no remedy; the learn step now re-sizes the stage plan from Milburn and Protest Tiers real build costs.
- F2 [fixed] Changes 2 and 3 were conditional on thresholds inside one yes; they now come back to Sam as their own proposals with the learned numbers.
- F3 [fixed] "Re-plan" could drift into doing less; it now changes only how the rest is built (reuse of kit means, order, model), never the joke or content.
- F4 [fixed] Every ledger row says stage "auto", so a by-stage forecast cannot work; Change 1 records the real stage.
- F5 [fixed] The week constant (WEEK_USD, PROVISIONAL) was left out by V2; it is re-set from the paired data.
- F6 [named] Whether get_session returns cost for finished chats is unchecked; learn step (a) tests it first, and if it cannot, Change 1 returns to Sam unbuilt.
- F7 [named] Sam's 22% may include non-Milburn work in that window.
- F8 [named] A forced re-plan is only as good as the cheaper ways left to build; reaching 15% is not guaranteed by this change alone.
## Final version
Learn (changes nothing, about 1.5% of a week, Sonnet):
(a) Read the app's real cost for all 15 Milburn chats (session ids in milburn.json) with get_session; import with `ledger.py app`. If cost is not returned, stop and report.
(b) Set each against its estimate; re-set WEEK_USD from the pairs.
(c) Label each chat build or notes (transcript, show log); count hand searches per note in note chats; mark look-ups of the same shared tool repeated across chats.
(d) Measure per chat the share of history that is search or read output.
(e) Re-size the stage plan from real build costs of Milburn and Protest Tiers.

Change 1 (one yes, about 1% to build, Opus medium):
- `handover.py end` refuses to hand over until this chat's app figure and real stage are in the ledger.
- The handover shows "film so far X% of 15%; forecast Y%" against the re-sized plan.
- If the forecast is over 15%, the next chat's start check makes it write a re-plan of how the remaining stages are built (reuse, order, model) before building, or put the choice to Sam. It never cuts the joke or content.
- Number to beat: every row of the next film is "app"; its forecast is within 2 points of its final cost; ledger within 5% of Sam's meter.
- Reviewed when Sam declares the next film complete.

Later, each as its own proposal with the learned numbers: trimming long search output (if (d) shows at least 20% of history); widening the finder to the shared kit or hand-carrying note locations (if (c) shows repeats or misses carry the search cost).

Honest sum: search fixes cap at about 3 to 4 real points; the 7 needed come mainly from build and history, steered by Change 1.
## For Sam
### Option 1: Real cost, steered during the film
First, a quick look-back (about 1.5% of a week) that fetches the app's real cost for every Milburn chat and finds where it went; building sets and props cost almost nine times its plan. Then every handover must record the real cost so far and show where the film will land. If it heads past 15%, the next chat must re-plan how the rest is built before carrying on, or ask you. It never cuts the joke.
Lost: one extra step per handover, and about 1.5% of a week for the look-back.
Added: a cost figure that matches your app during the film, a warning before the money is spent, and a re-plan that actually happens.
### Option 2: Look-back, then a search block
Same look-back and real-cost line at each handover, plus a rule that blocks chats from searching code by hand once the look-back shows which kind of searching cost most. Searching is only about a quarter of the spend, so this saves less.
Lost: one extra step per handover; chats blocked from some hand searches, which can slow building.
Added: a real cost line, and fewer repeated searches of the shared tools.
