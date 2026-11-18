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
