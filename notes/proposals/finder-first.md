# Proposal: Chats search by hand about 65 times for every finder use, in every chat, despite two earlier fixes

Status: open

## Problem
Sam's goal is a film within 15% of a week. Searching is the one cost that is meant to be already solved: the code
finder (page.py show) answers "which lines does this note touch" in one step. In Milburn, chats searched files by hand
far more than they used it, in every chat, including after a reminder at the moment of a hand search was added. Sam
calls this the overwhelming search failure and wants it fixed before anything else. Sam has shelved the cost-reading
work (proposal search-first, judged but not decided) for now: this proposal is about searching only.

## Facts
- Milburn ledger (notes/ledger/milburn.json, 15 chats, 17-18 Nov, 1,259 steps; costs are transcript estimates, not app
  figures): finder used 12 times in total; hand searches of film code 248; searches of non-film files (the ledger kind
  "tool search": any grep or partial read of a non-film file) 531, of which 328 shared tools, 101 other, 81 film
  notes, 21 guides. About 780 hand searches against 12 finder uses.
- Estimated cost: film-file search 2.77 points and non-film-file search 5.27 points of the 32.14 recorded (Sam's own
  reading of the whole film was 22%, so these are probably high by about a third).
- Of the 248 film-code hand searches: 74 in chats with no finder call, 13 before a chat's first finder call, 43 within
  10 calls after a finder call (a miss), 118 later after a finder call.
- Shared tools most searched: facehouse.py 30, critique.py 29, people.py 27, people_parts.py 23, handover.py 23,
  acting.py 20, preflight.py 18, kittests.py 16, views.py 11. The finder covers only the film's own source/FILM*.py.
- Per chat (finder uses / film-code hand searches / non-film searches): 0/1/41, 0/6/48, 0/24/65, 1/9/19, 0/13/82,
  1/14/36, 0/18/27, 0/1/11, 1/16/34, 2/24/50, 2/36/35, 3/40/29, 0/10/18, 2/35/31, 0/1/5 (ledger order).
- Earlier fixes: the finder's change 1 and 2 (notes/proposals/code-finder.md, adopted 16 Nov); a per-chat reminder at
  the first hand search and a per-chat search record (commit 64f19a94, 17 Nov, from notes/proposals/finder-use.md).
  The 16 Nov baseline: hand search 6.65% + 3.22% of a week against the finder 0.21% (19 Protest Tiers chats).
- Notes ticked per chat is 0 in every Milburn row, so searches per note cannot be computed. A chat cannot tell,
  from the record, which hand searches were building (legitimate) and which were fixing a note.
- Unchecked: why the 17 Nov reminder did not change behaviour (was it printed, read, ignored); what the finder misses
  on real Milburn notes; how many of the 531 non-film searches were for something the finder or a one-page list would
  have answered in one step.
- Sam, this chat: the 15% goal applies to every film; chat length and model-by-stage rules stand.

## Record
notes/ledger/milburn.json
notes/ledger/milburn.md
notes/logs/milburn-show.log
notes/proposals/finder-use.md
notes/proposals/code-finder.md
notes/proposals/early-warning.md
notes/proposals/history-and-search.md
notes/proposals/search-first.md
source/page.py
source/stepcost.py
source/handover.py
source/ledger.py
guides/kit-catalogue.md
guides/job-packs.md
