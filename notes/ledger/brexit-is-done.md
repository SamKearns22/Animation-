# Ledger: brexit-is-done

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 6.02%; 3 chats, 0 rounds, 3 notes, 1 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | d9128054 | est | opus | cast |  | 1.85 |  | 3 | 1 |
| 2026-11-23 | 9db844b1 | est | opus | auto |  | 2.47 |  | 0 | 0 |
| 2026-11-23 | f27fff03 | est | opus | auto |  | 1.7 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-23 9db844b1 (auto): 144 steps, history 273k at the end; other 66.1%, tool search 20.6%, pictures 7.1%, renders 5.5%, film-file search 0.6%, page.py 0.2%
- 2026-11-23 f27fff03 (auto): 78 steps, history 167k at the end; other 70.9%, tool search 24.3%, pictures 2.4%, renders 1.5%, film-file search 0.9%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-23 9db844b1 (auto): carried history 33.2%, start-up floor 27%, Claude's words 22.4%, new writes 17.4%. Biggest origins: Claude's words 41.2%, start-up floor 27%, result: tool search 15%. Leftover 0%
- 2026-11-23 f27fff03 (auto): start-up floor 41.5%, new writes 20.8%, Claude's words 19.4%, carried history 18.3%. Biggest origins: start-up floor 41.5%, Claude's words 29.6%, result: tool search 19.6%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 6% of the film (0.38% of a week over 2 chats: start 0.38, re-learning 0.00; 0.19% a chat; step-1 context re-read is 31% of a chat on average).
- 2026-11-23 9db844b1: step-1 context 84k; first real work at step 17 (0.26% of a week); read before it: source/facehouse.py 4.4k, source/turnhead.py 1.8k, notes/sam-notes/brexit-cast-v1/n2-blair-threequarter-not-same.jpg 1.6k, notes/sam-notes/brexit-cast-v1/n3-kemi-orange-gone-threequarter.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/9db844b1-280f-5d8a-a457-8c9f20d932da/scratchpad/t0.jpg 1.6k, notes/sam-notes/brexit-cast-v1/notes.md 1.4k
- 2026-11-23 f27fff03: step-1 context 84k; first real work at step 10 (0.12% of a week); read before it: notes/logs/broken.md 1k, source/watcher.py 0.4k, .claude/settings.json 0.3k, source/hookran.py 0.3k, source/data/freeze/films.json 0.2k

## Repeated notes (what would have caught them)
- Blair 3/4 not the same person as front | a front-vs-3/4 match check
