# Ledger: brexit-is-done

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 6.64%; 3 chats, 0 rounds, 5 notes, 2 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | d9128054 | est | opus | cast |  | 1.85 |  | 3 | 1 |
| 2026-11-23 | 9db844b1 | est | opus | auto |  | 2.47 |  | 0 | 0 |
| 2026-11-23 | f27fff03 | est | opus | cast |  | 2.32 |  | 2 | 1 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-23 9db844b1 (auto): 144 steps, history 273k at the end; other 66.1%, tool search 20.6%, pictures 7.1%, renders 5.5%, film-file search 0.6%, page.py 0.2%
- 2026-11-23 f27fff03 (cast): 115 steps, history 211k at the end; other 72.1%, tool search 24.1%, pictures 2.1%, renders 0.9%, film-file search 0.7%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-23 9db844b1 (auto): carried history 33.2%, start-up floor 27%, Claude's words 22.4%, new writes 17.4%. Biggest origins: Claude's words 41.2%, start-up floor 27%, result: tool search 15%. Leftover 0%
- 2026-11-23 f27fff03 (cast): start-up floor 36.3%, carried history 25.1%, Claude's words 19.3%, new writes 19.3%. Biggest origins: start-up floor 36.3%, Claude's words 31.6%, result: tool search 19.3%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 6% of the film (0.38% of a week over 2 chats: start 0.38, re-learning 0.00; 0.19% a chat; step-1 context re-read is 29% of a chat on average).
- 2026-11-23 9db844b1: step-1 context 84k; first real work at step 17 (0.26% of a week); read before it: source/facehouse.py 4.4k, source/turnhead.py 1.8k, notes/sam-notes/brexit-cast-v1/n2-blair-threequarter-not-same.jpg 1.6k, notes/sam-notes/brexit-cast-v1/n3-kemi-orange-gone-threequarter.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/9db844b1-280f-5d8a-a457-8c9f20d932da/scratchpad/t0.jpg 1.6k, notes/sam-notes/brexit-cast-v1/notes.md 1.4k
- 2026-11-23 f27fff03: step-1 context 84k; first real work at step 10 (0.12% of a week); read before it: notes/logs/broken.md 1k, source/watcher.py 0.4k, .claude/settings.json 0.3k, source/hookran.py 0.3k, source/data/freeze/films.json 0.2k

## Repeated notes (what would have caught them)
- Blair 3/4 not the same person as front | a front-vs-3/4 match check
- Women drawn on a man's body (GTA Lucia 20 Nov, Open Wounds n5) | none: no check knows who is a woman; the GTA fix was opt-in for one person
