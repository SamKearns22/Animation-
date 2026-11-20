# Ledger: grand-theft-autism

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate 53.2% of a week; spent 12.02% (-41.18); 7 chats, 0 rounds, 0 notes, 0 repeated.**

**Forecast: Spent 12.02% of the 0% planned so far; at this rate the film lands at 62.6%.**

| stage | planned % | done | spent at its end |
|---|---|---|---|
| opener | 2.67 |  |  |
| plan | 2 |  |  |
| cast | 13.3 |  |  |
| cars | 4.5 |  |  |
| sets | 4.7 |  |  |
| board | 0.5 |  |  |
| moves | 11.3 |  |  |
| animatic1 | 2.1 |  |  |
| round1 | 9.4 |  |  |
| round2 | 2.4 |  |  |
| final | 0.35 |  |  |

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-19 | c079f576 | est | opus | auto |  | 2.67 |  | 0 | 0 |
| 2026-11-20 | ba8d2922 | est | opus | auto |  | 0.69 |  | 0 | 0 |
| 2026-11-20 | 23d4842a | est | sonnet | auto |  | 0.13 |  | 0 | 0 |
| 2026-11-20 | caff6f5e | est | opus | auto |  | 3.29 |  | 0 | 0 |
| 2026-11-20 | 303835b1 | est | opus | auto |  | 1.84 |  | 0 | 0 |
| 2026-11-20 | 48091c44 | est | opus | auto |  | 2.09 |  | 0 | 0 |
| 2026-11-20 | 78cd6210 | est | opus | auto |  | 1.31 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-19 c079f576 (auto): 101 steps, history 274k at the end; other 75.9%, pictures 9.9%, renders 8.6%, tool search 5.6%
- 2026-11-20 ba8d2922 (auto): 46 steps, history 156k at the end; other 63.7%, tool search 23.9%, renders 8.4%, pictures 2.8%, page.py 1.2%
- 2026-11-20 23d4842a (auto): 18 steps, history 108k at the end; other 84.2%, renders 7.4%, tool search 6.1%, page.py 2.4%
- 2026-11-20 caff6f5e (auto): 130 steps, history 289k at the end; other 73.6%, tool search 13.9%, pictures 5.4%, film-file search 3.8%, renders 3.1%, page.py 0.3%
- 2026-11-20 303835b1 (auto): 69 steps, history 260k at the end; other 68.3%, tool search 18.8%, renders 7.7%, pictures 5.2%
- 2026-11-20 48091c44 (auto): 82 steps, history 288k at the end; other 53.4%, tool search 31.7%, renders 5.9%, pictures 4.8%, film-file search 3.1%, whole-file .py read 1%, page.py 0.1%
- 2026-11-20 78cd6210 (auto): 77 steps, history 191k at the end; other 76.5%, tool search 18.5%, pictures 3.8%, renders 1.2%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-19 c079f576 (auto): new writes 33.2%, Claude's words 30.9%, carried history 19.3%, start-up floor 16.6%. Biggest origins: Claude's words 47.7%, cache re-write 17.4%, start-up floor 16.6%. Leftover 0%
- 2026-11-20 ba8d2922 (auto): start-up floor 33.8%, Claude's words 30.9%, new writes 23.4%, carried history 11.9%. Biggest origins: Claude's words 43.3%, start-up floor 33.8%, result: tool search 13.9%. Leftover 0%
- 2026-11-20 23d4842a (auto): start-up floor 47.8%, new writes 24.1%, Claude's words 23.2%, carried history 4.8%. Biggest origins: start-up floor 47.8%, Claude's words 29.8%, result: other 17.7%. Leftover 0%
- 2026-11-20 caff6f5e (auto): new writes 44.2%, carried history 22.1%, start-up floor 17.6%, Claude's words 16%. Biggest origins: cache re-write 30%, Claude's words 27.5%, start-up floor 17.6%. Leftover 0%
- 2026-11-20 303835b1 (auto): Claude's words 40.1%, new writes 22.3%, carried history 19.4%, start-up floor 18.2%. Biggest origins: Claude's words 59.8%, start-up floor 18.2%, result: tool search 10%. Leftover 0%
- 2026-11-20 48091c44 (auto): Claude's words 35.3%, carried history 23.2%, new writes 22.8%, start-up floor 18.7%. Biggest origins: Claude's words 56.3%, start-up floor 18.7%, result: tool search 17.9%. Leftover 0%
- 2026-11-20 78cd6210 (auto): new writes 38.7%, start-up floor 26.5%, Claude's words 18.2%, carried history 16.6%. Biggest origins: Claude's words 28.3%, start-up floor 26.5%, cache re-write 20.5%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 22% of the film (2.62% of a week over 7 chats: start 2.52, re-learning 0.10; 0.37% a chat; step-1 context re-read is 20% of a chat on average).
- 2026-11-19 c079f576: step-1 context 80k; first real work at step 12 (0.21% of a week); read before it: guides/kit-catalogue.md 2.1k, /tmp/claude-0/-home-user-Animation-/c079f576-588d-58fe-aa6f-b16fc9938f9a/scratchpad/vid/s4.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/c079f576-588d-58fe-aa6f-b16fc9938f9a/scratchpad/sea.png 1.6k, guides/job-packs.md 1.2k, source/flying_whales_sea.py 1.2k, story/status.md 0.3k
- 2026-11-20 ba8d2922: step-1 context 82k; first real work at step 40 (0.6% of a week); read before it: notes/_template.md 1.5k, notes/grand-theft-autism.md 1.3k, /tmp/claude-0/-home-user-Animation-/ba8d2922-8810-560c-9071-db977029f213/scratchpad/refs/tulip1.png 1.6k, /tmp/claude-0/-home-user-Animation-/ba8d2922-8810-560c-9071-db977029f213/scratchpad/refs/tulip2.jpg 1.6k, guides/kit-catalogue.md 1.4k, /tmp/claude-0/-home-user-Animation-/ba8d2922-8810-560c-9071-db977029f213/scratchpad/refs/jl.jpg 1.6k
- 2026-11-20 23d4842a: step-1 context 80k; first real work at step 14 (0.1% of a week); read before it: notes/grand-theft-autism.md 3.5k, story/status.md 0.2k, notes/ledger/sam/bdslc8hv.md 0.3k
- 2026-11-20 caff6f5e: step-1 context 82k; first real work at step 24 (0.32% of a week); read before it: source/people.py 4.9k, notes/grand-theft-autism.md 3.8k, guides/kit-catalogue.md 3.4k, guides/figure-rig.md 2.4k, /tmp/claude-0/-home-user-Animation-/caff6f5e-2e4e-56a5-be31-0ef3425985f7/scratchpad/refs.jpg 1.6k, source/people_parts.py 1.5k
- 2026-11-20 303835b1: step-1 context 82k; first real work at step 16 (0.25% of a week); read before it: notes/grand-theft-autism.md 4.1k, source/sets.py 2.6k, /home/user/Animation-/references/grand-theft-autism/tulip-side-trailer1.jpg 1.6k, /home/user/Animation-/references/grand-theft-autism/tulip-rear-three-quarter.jpg 1.6k, /home/user/Animation-/references/grand-theft-autism/vcpd-cruiser-rear.jpg 1.6k, /home/user/Animation-/references/grand-theft-autism/vcpd-cruiser-above.jpg 1.6k
- 2026-11-20 48091c44: step-1 context 82k; first real work at step 6 (0.1% of a week); read before it: notes/grand-theft-autism.md 4.2k
- 2026-11-20 78cd6210: step-1 context 82k; first real work at step 69 (0.94% of a week); read before it: source/gta_rehearse.py 8k, /tmp/claude-0/-home-user-Animation-/78cd6210-928b-5aee-845d-05993a6f4285/scratchpad/s4/sheet.jpg 6.4k, /tmp/claude-0/-home-user-Animation-/78cd6210-928b-5aee-845d-05993a6f4285/scratchpad/s4/crop.jpg 3.2k, /tmp/claude-0/-home-user-Animation-/78cd6210-928b-5aee-845d-05993a6f4285/scratchpad/v.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/78cd6210-928b-5aee-845d-05993a6f4285/scratchpad/cs/strip.jpg 1.6k, story/status.md 0.9k
