# Ledger: brexit-is-done

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 27.89%; 12 chats, 0 rounds, 8 notes, 3 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | d9128054 | est | opus | cast |  | 1.85 |  | 3 | 1 |
| 2026-11-23 | 9db844b1 | est | opus | auto |  | 2.47 |  | 0 | 0 |
| 2026-11-23 | f27fff03 | est | opus | cast |  | 2.58 |  | 2 | 1 |
| 2026-11-23 | f960632f | est | opus | cast |  | 2.55 |  | 2 | 0 |
| 2026-11-24 | da73dc7c | est | opus | build |  | 2.01 |  | 0 | 0 |
| 2026-11-24 | ea6a7a83 | est | opus | sets |  | 3.19 |  | 0 | 0 |
| 2026-11-24 | ccee3e40 | est | opus | auto |  | 2.62 |  | 0 | 0 |
| 2026-11-24 | 436a9d65 | est | opus | auto |  | 1.92 |  | 0 | 0 |
| 2026-11-24 | 946806fb | est | opus | board |  | 2.03 |  | 1 | 1 |
| 2026-11-24 | 99562b0e | est | opus | auto |  | 2.03 |  | 0 | 0 |
| 2026-11-24 | 5e7b21fe | est | opus | auto |  | 2.49 |  | 0 | 0 |
| 2026-11-25 | e5d6ce05 | est | opus | shot 3 chase watched and fixed, critique r5 |  | 2.15 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-23 9db844b1 (auto): 144 steps, history 273k at the end; other 66.1%, tool search 20.6%, pictures 7.1%, renders 5.5%, film-file search 0.6%, page.py 0.2%
- 2026-11-23 f27fff03 (cast): 131 steps, history 223k at the end; other 71.7%, tool search 24.3%, pictures 2.1%, renders 1.2%, film-file search 0.6%
- 2026-11-23 f960632f (cast): 122 steps, history 267k at the end; other 76.2%, tool search 18.4%, pictures 2.8%, whole-file .py read 1%, film-file search 0.9%, renders 0.6%, page.py 0.1%
- 2026-11-24 ea6a7a83 (sets): 129 steps, history 316k at the end; other 74.4%, tool search 19.5%, pictures 2.8%, film-file search 2.5%, renders 0.6%, page.py 0.2%
- 2026-11-24 ccee3e40 (auto): 99 steps, history 292k at the end; other 78.5%, tool search 14.2%, renders 4.8%, pictures 2.5%
- 2026-11-24 436a9d65 (auto): 82 steps, history 226k at the end; other 72.6%, tool search 18.9%, pictures 4.7%, renders 2.6%, film-file search 0.9%, whole-file .py read 0.5%
- 2026-11-24 946806fb (board): 53 steps, history 168k at the end; other 70%, tool search 17.5%, film-file search 6.3%, pictures 4.1%, renders 1.5%, page.py 0.6%
- 2026-11-24 99562b0e (auto): 105 steps, history 273k at the end; other 64.7%, tool search 23.3%, film-file search 8.5%, pictures 2.8%, renders 0.6%, page.py 0.2%
- 2026-11-24 5e7b21fe (auto): 107 steps, history 269k at the end; other 64.8%, tool search 16.4%, film-file search 11%, pictures 6.3%, renders 1.5%
- 2026-11-25 e5d6ce05 (shot 3 chase watched and fixed, critique r5): 110 steps, history 282k at the end; other 69.2%, tool search 11.7%, pictures 9.7%, film-file search 7.8%, renders 1.1%, page.py 0.6%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-23 9db844b1 (auto): carried history 33.2%, start-up floor 27%, Claude's words 22.4%, new writes 17.4%. Biggest origins: Claude's words 41.2%, start-up floor 27%, result: tool search 15%. Leftover 0%
- 2026-11-23 f27fff03 (cast): start-up floor 34.7%, carried history 27.4%, Claude's words 19.9%, new writes 18%. Biggest origins: start-up floor 34.7%, Claude's words 33.3%, result: tool search 19%. Leftover 0%
- 2026-11-23 f960632f (cast): new writes 32.6%, carried history 30.6%, Claude's words 19.4%, start-up floor 17.4%. Biggest origins: Claude's words 35.4%, start-up floor 17.9%, cache re-write 15.9%. Leftover 0%
- 2026-11-24 ea6a7a83 (sets): new writes 32.9%, carried history 25.5%, Claude's words 23.5%, start-up floor 18.1%. Biggest origins: Claude's words 39.4%, start-up floor 18.1%, cache re-write 17.1%. Leftover 0%
- 2026-11-24 ccee3e40 (auto): carried history 33.2%, new writes 31.9%, Claude's words 26.8%, start-up floor 8%. Biggest origins: messages and reminders 39.9%, Claude's words 38.2%, start-up floor 8.1%. Leftover 0%
- 2026-11-24 436a9d65 (auto): start-up floor 30.5%, new writes 24.4%, carried history 23.7%, Claude's words 21.4%. Biggest origins: Claude's words 32.9%, start-up floor 30.5%, result: tool search 16.1%. Leftover 0%
- 2026-11-24 946806fb (board): start-up floor 32.6%, new writes 25.6%, Claude's words 23.1%, carried history 18.7%. Biggest origins: start-up floor 33.7%, Claude's words 32.6%, result: tool search 17.7%. Leftover 0%
- 2026-11-24 99562b0e (auto): Claude's words 28.4%, carried history 27.5%, start-up floor 23.8%, new writes 20.3%. Biggest origins: Claude's words 46%, start-up floor 23.8%, result: tool search 20.7%. Leftover 0%
- 2026-11-24 5e7b21fe (auto): Claude's words 30%, carried history 25.7%, start-up floor 23.9%, new writes 20.4%. Biggest origins: Claude's words 51%, start-up floor 23.9%, result: tool search 10%. Leftover 0%
- 2026-11-25 e5d6ce05 (shot 3 chase watched and fixed, critique r5): carried history 49.3%, Claude's words 25.5%, new writes 23.1%, start-up floor 2.1%. Biggest origins: Claude's words 47.7%, result: pictures 19.7%, messages and reminders 15.8%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 16% of the film (4.39% of a week over 10 chats: start 4.28, re-learning 0.11; 0.44% a chat; step-1 context re-read is 23% of a chat on average).
- 2026-11-23 9db844b1: step-1 context 84k; first real work at step 17 (0.26% of a week); read before it: source/facehouse.py 4.4k, source/turnhead.py 1.8k, notes/sam-notes/brexit-cast-v1/n2-blair-threequarter-not-same.jpg 1.6k, notes/sam-notes/brexit-cast-v1/n3-kemi-orange-gone-threequarter.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/9db844b1-280f-5d8a-a457-8c9f20d932da/scratchpad/t0.jpg 1.6k, notes/sam-notes/brexit-cast-v1/notes.md 1.4k
- 2026-11-23 f27fff03: step-1 context 84k; first real work at step 10 (0.12% of a week); read before it: notes/logs/broken.md 1k, source/watcher.py 0.4k, .claude/settings.json 0.3k, source/hookran.py 0.3k, source/data/freeze/films.json 0.2k
- 2026-11-23 f960632f: step-1 context 84k; first real work at step 40 (0.53% of a week); read before it: source/castsheet.py 2.4k, source/sitting.py 2.2k, notes/next-jobs.md 1.6k, notes/brexit-is-done.md 1.6k, notes/sam-notes/brexit-cast-v2/n5-kemi-body-like-a-mans.jpg 1.6k, notes/sam-notes/brexit-cast-v2/n5-may-body.jpg 1.6k
- 2026-11-24 ea6a7a83: step-1 context 84k; first real work at step 48 (0.73% of a week); read before it: notes/brexit-is-done.md 3.1k, guides/kit-catalogue.md 3.3k, /tmp/claude-0/-home-user-Animation-/ea6a7a83-115e-5b55-8941-8d3a521b6bc8/scratchpad/wolfsheet.png 1.6k, /tmp/claude-0/-home-user-Animation-/ea6a7a83-115e-5b55-8941-8d3a521b6bc8/scratchpad/refs.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/ea6a7a83-115e-5b55-8941-8d3a521b6bc8/scratchpad/geo/thumbs.jpg 1.6k, guides/preflight.md 1.3k
- 2026-11-24 ccee3e40: step-1 context 84k; first real work at step 27 (0.76% of a week); read before it: notes/brexit-is-done-sets.md 5.4k, source/wolf.py 5.4k, guides/critique-checklist.md 3.7k, source/freeze.py 1.8k, /tmp/claude-0/-home-user-Animation-/ccee3e40-ca89-5aa9-b493-855be3c5b81f/scratchpad/wolf-old.png 1.6k, source/eyekit.py 1.4k
- 2026-11-24 436a9d65: step-1 context 84k; first real work at step 19 (0.3% of a week); read before it: notes/brexit-is-done-sets.md 5.8k, notes/learn/kemi-build/cast-v3.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/436a9d65-1b11-5462-8fb2-0e83962b3255/scratchpad/turned-before.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/436a9d65-1b11-5462-8fb2-0e83962b3255/scratchpad/turned-crop.jpg 1.6k, source/views.py 1.3k, notes/learn/kemi-build/judge.py 0.4k
- 2026-11-24 946806fb: step-1 context 84k; first real work at step 22 (0.3% of a week); read before it: source/milburn.py 4.7k, notes/brexit-is-done-sets.md 4.1k, source/rough.py 1.6k, story/brexit-is-done-places.txt 1.4k, source/castsheet.py 0.7k, story/brexit-is-done-people.txt 0.3k
- 2026-11-24 99562b0e: step-1 context 84k; first real work at step 10 (0.14% of a week); read before it: source/handover.py 1k
- 2026-11-24 5e7b21fe: step-1 context 82k; first real work at step 38 (0.57% of a week); read before it: source/brexit_is_done_action.py 2.8k, notes/brexit-is-done-sets.md 2.1k, source/brexit_is_done.py 2k, /tmp/claude-0/-home-user-Animation-/5e7b21fe-b708-5a33-b4a2-002cc1814d83/scratchpad/s3/a.jpg 1.6k, source/wolf.py 1.5k, source/places_site.py 1.6k
- 2026-11-25 e5d6ce05: step-1 context 84k; first real work at step 34 (0.57% of a week); read before it: /tmp/claude-0/-home-user-Animation-/e5d6ce05-56e8-5a03-87c6-f1bb090bc4b5/scratchpad/cyc.jpg 3.2k, source/brexit_is_done_action.py 2.3k, source/moves.py 1.9k, /tmp/claude-0/-home-user-Animation-/e5d6ce05-56e8-5a03-87c6-f1bb090bc4b5/scratchpad/sheet0.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/e5d6ce05-56e8-5a03-87c6-f1bb090bc4b5/scratchpad/sheet2.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/e5d6ce05-56e8-5a03-87c6-f1bb090bc4b5/scratchpad/z1.jpg 1.6k

## Repeated notes (what would have caught them)
- Blair 3/4 not the same person as front | a front-vs-3/4 match check
- Women drawn on a man's body (GTA Lucia 20 Nov, Open Wounds n5) | none: no check knows who is a woman; the GTA fix was opt-in for one person
- No bum/circular knees | castsheet.seated_faults (built now); P7 by hand only
