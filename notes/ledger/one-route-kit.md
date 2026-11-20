# Ledger: one-route-kit

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate 14.0% of a week; spent 6.04% (-7.96); 4 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-20 | 474881c3 | est | sonnet | auto |  | 0.25 |  | 0 | 0 |
| 2026-11-20 | e3a7708e | est | sonnet | auto |  | 0.98 |  | 0 | 0 |
| 2026-11-20 | 4487bc3c | est | opus | auto |  | 2.57 |  | 0 | 0 |
| 2026-11-20 | fba25ad9 | est | opus | auto |  | 2.24 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-20 474881c3 (auto): 33 steps, history 132k at the end; other 65.5%, tool search 27.5%, renders 3.2%, pictures 1.9%, whole-file .py read 1.8%
- 2026-11-20 e3a7708e (auto): 122 steps, history 229k at the end; other 69.8%, tool search 26%, renders 2.9%, pictures 1.2%
- 2026-11-20 4487bc3c (auto): 143 steps, history 287k at the end; other 64.8%, tool search 34.8%, whole-file .py read 0.4%
- 2026-11-20 fba25ad9 (auto): 146 steps, history 272k at the end; other 63.8%, tool search 23.1%, pictures 10.8%, renders 1.3%, whole-file .py read 0.7%, page.py 0.4%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-20 474881c3 (auto): start-up floor 39.5%, Claude's words 30.1%, new writes 22.1%, carried history 8.3%. Biggest origins: Claude's words 40.5%, start-up floor 39.5%, result: tool search 14.3%. Leftover 0%
- 2026-11-20 e3a7708e (auto): start-up floor 29.7%, carried history 27.2%, Claude's words 26.7%, new writes 16.4%. Biggest origins: Claude's words 43.1%, start-up floor 29.7%, result: tool search 14.7%. Leftover 0%
- 2026-11-20 4487bc3c (auto): carried history 33.4%, Claude's words 24.8%, start-up floor 24.4%, new writes 17.4%. Biggest origins: Claude's words 46.9%, start-up floor 24.4%, result: tool search 23.8%. Leftover 0%
- 2026-11-20 fba25ad9 (auto): carried history 30.8%, start-up floor 28%, Claude's words 22.6%, new writes 18.5%. Biggest origins: Claude's words 39.9%, start-up floor 28%, result: tool search 16%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 52% of the film (3.14% of a week over 4 chats: start 3.11, re-learning 0.03; 0.79% a chat; step-1 context re-read is 26% of a chat on average). Over 0.5% a chat: a warm handover goes to Sam through the proposal route.
- 2026-11-20 474881c3: step-1 context 82k; first real work at step None (None% of a week); read before it: notes/one-route-kit.md 1.8k, /tmp/claude-0/-home-user-Animation-/474881c3-cb04-55bc-ae36-05cf93ead27a/scratchpad/m.png 1.6k, notes/proposals/one-route-kit/measure/patches.py 1.2k, /tmp/claude-0/-home-user-Animation-/474881c3-cb04-55bc-ae36-05cf93ead27a/scratchpad/sheet.png 1.6k, notes/proposals/one-route-kit.md 0.4k, notes/proposals/one-route-kit/measure/reach.py 0.4k
- 2026-11-20 e3a7708e: step-1 context 82k; first real work at step 26 (0.18% of a week); read before it: notes/one-route-kit.md 1.1k, notes/proposals/one-route-kit/chat.md 1.1k, notes/proposals/one-route-kit/measure/reach.py 0.8k, source/film_engine.py 0.6k, story/status.md 0.5k, source/bayeux.py 0.4k
- 2026-11-20 4487bc3c: step-1 context 82k; first real work at step 133 (2.4% of a week); read before it: source/freeze.py 3.4k, notes/one-route-kit.md 1.7k, ../story/grand-theft-autism-people.txt 1.8k, notes/logs/broken.md 0.5k, story/status.md 0.2k
- 2026-11-20 fba25ad9: step-1 context 82k; first real work at step 46 (0.53% of a week); read before it: /tmp/claude-0/-home-user-Animation-/fba25ad9-bfda-51fa-b86f-d4c0e4c49a96/scratchpad/sh/before.png 4.8k, source/limbs.py 3.7k, source/views.py 3.5k, source/body.py 2.3k, /tmp/claude-0/-home-user-Animation-/fba25ad9-bfda-51fa-b86f-d4c0e4c49a96/scratchpad/jury/t8.5.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/fba25ad9-bfda-51fa-b86f-d4c0e4c49a96/scratchpad/jury/crop1.png 1.6k
