# Ledger: one-route-kit

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate 14.0% of a week; spent 3.2% (-10.80); 3 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-20 | 474881c3 | est | sonnet | auto |  | 0.25 |  | 0 | 0 |
| 2026-11-20 | e3a7708e | est | sonnet | auto |  | 0.98 |  | 0 | 0 |
| 2026-11-20 | 4487bc3c | est | opus | auto |  | 1.97 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-20 474881c3 (auto): 33 steps, history 132k at the end; other 65.5%, tool search 27.5%, renders 3.2%, pictures 1.9%, whole-file .py read 1.8%
- 2026-11-20 e3a7708e (auto): 122 steps, history 229k at the end; other 69.8%, tool search 26%, renders 2.9%, pictures 1.2%
- 2026-11-20 4487bc3c (auto): 109 steps, history 260k at the end; other 62.2%, tool search 37.3%, whole-file .py read 0.5%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-20 474881c3 (auto): start-up floor 39.5%, Claude's words 30.1%, new writes 22.1%, carried history 8.3%. Biggest origins: Claude's words 40.5%, start-up floor 39.5%, result: tool search 14.3%. Leftover 0%
- 2026-11-20 e3a7708e (auto): start-up floor 29.7%, carried history 27.2%, Claude's words 26.7%, new writes 16.4%. Biggest origins: Claude's words 43.1%, start-up floor 29.7%, result: tool search 14.7%. Leftover 0%
- 2026-11-20 4487bc3c (auto): Claude's words 28.1%, carried history 27.3%, start-up floor 24.9%, new writes 19.7%. Biggest origins: Claude's words 48.2%, start-up floor 24.9%, result: tool search 22.8%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 6% of the film (0.20% of a week over 3 chats: start 0.18, re-learning 0.02; 0.07% a chat; step-1 context re-read is 26% of a chat on average).
- 2026-11-20 474881c3: step-1 context 82k; first real work at step None (None% of a week); read before it: notes/one-route-kit.md 1.8k, /tmp/claude-0/-home-user-Animation-/474881c3-cb04-55bc-ae36-05cf93ead27a/scratchpad/m.png 1.6k, notes/proposals/one-route-kit/measure/patches.py 1.2k, /tmp/claude-0/-home-user-Animation-/474881c3-cb04-55bc-ae36-05cf93ead27a/scratchpad/sheet.png 1.6k, notes/proposals/one-route-kit.md 0.4k, notes/proposals/one-route-kit/measure/reach.py 0.4k
- 2026-11-20 e3a7708e: step-1 context 82k; first real work at step 26 (0.18% of a week); read before it: notes/one-route-kit.md 1.1k, notes/proposals/one-route-kit/chat.md 1.1k, notes/proposals/one-route-kit/measure/reach.py 0.8k, source/film_engine.py 0.6k, story/status.md 0.5k, source/bayeux.py 0.4k
- 2026-11-20 4487bc3c: step-1 context 82k; first real work at step None (None% of a week); read before it: source/freeze.py 3.4k, notes/one-route-kit.md 1.7k, ../story/grand-theft-autism-people.txt 1.8k, notes/logs/broken.md 0.5k
