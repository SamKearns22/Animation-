# Ledger: brexit-is-done

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 9.45%; 4 chats, 0 rounds, 7 notes, 2 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | d9128054 | est | opus | cast |  | 1.85 |  | 3 | 1 |
| 2026-11-23 | 9db844b1 | est | opus | auto |  | 2.47 |  | 0 | 0 |
| 2026-11-23 | f27fff03 | est | opus | cast |  | 2.58 |  | 2 | 1 |
| 2026-11-23 | f960632f | est | opus | cast |  | 2.55 |  | 2 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-23 9db844b1 (auto): 144 steps, history 273k at the end; other 66.1%, tool search 20.6%, pictures 7.1%, renders 5.5%, film-file search 0.6%, page.py 0.2%
- 2026-11-23 f27fff03 (cast): 131 steps, history 223k at the end; other 71.7%, tool search 24.3%, pictures 2.1%, renders 1.2%, film-file search 0.6%
- 2026-11-23 f960632f (cast): 122 steps, history 267k at the end; other 76.2%, tool search 18.4%, pictures 2.8%, whole-file .py read 1%, film-file search 0.9%, renders 0.6%, page.py 0.1%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-23 9db844b1 (auto): carried history 33.2%, start-up floor 27%, Claude's words 22.4%, new writes 17.4%. Biggest origins: Claude's words 41.2%, start-up floor 27%, result: tool search 15%. Leftover 0%
- 2026-11-23 f27fff03 (cast): start-up floor 34.7%, carried history 27.4%, Claude's words 19.9%, new writes 18%. Biggest origins: start-up floor 34.7%, Claude's words 33.3%, result: tool search 19%. Leftover 0%
- 2026-11-23 f960632f (cast): new writes 32.6%, carried history 30.6%, Claude's words 19.4%, start-up floor 17.4%. Biggest origins: Claude's words 35.4%, start-up floor 17.9%, cache re-write 15.9%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 10% of the film (0.91% of a week over 3 chats: start 0.91, re-learning 0.00; 0.30% a chat; step-1 context re-read is 26% of a chat on average).
- 2026-11-23 9db844b1: step-1 context 84k; first real work at step 17 (0.26% of a week); read before it: source/facehouse.py 4.4k, source/turnhead.py 1.8k, notes/sam-notes/brexit-cast-v1/n2-blair-threequarter-not-same.jpg 1.6k, notes/sam-notes/brexit-cast-v1/n3-kemi-orange-gone-threequarter.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/9db844b1-280f-5d8a-a457-8c9f20d932da/scratchpad/t0.jpg 1.6k, notes/sam-notes/brexit-cast-v1/notes.md 1.4k
- 2026-11-23 f27fff03: step-1 context 84k; first real work at step 10 (0.12% of a week); read before it: notes/logs/broken.md 1k, source/watcher.py 0.4k, .claude/settings.json 0.3k, source/hookran.py 0.3k, source/data/freeze/films.json 0.2k
- 2026-11-23 f960632f: step-1 context 84k; first real work at step 40 (0.53% of a week); read before it: source/castsheet.py 2.4k, source/sitting.py 2.2k, notes/next-jobs.md 1.6k, notes/brexit-is-done.md 1.6k, notes/sam-notes/brexit-cast-v2/n5-kemi-body-like-a-mans.jpg 1.6k, notes/sam-notes/brexit-cast-v2/n5-may-body.jpg 1.6k

## Repeated notes (what would have caught them)
- Blair 3/4 not the same person as front | a front-vs-3/4 match check
- Women drawn on a man's body (GTA Lucia 20 Nov, Open Wounds n5) | none: no check knows who is a woman; the GTA fix was opt-in for one person
