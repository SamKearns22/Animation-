# Helper A: memory lapses on grand-theft-autism

## Leak
The problem file states no solution. Its record list includes `chat.md`, which holds the writing chat's own idea (hand over before long waits); I read it because it was listed, and set it aside. Its claim of "about an hour idle" is marked unchecked below.

## Results
- Lapses cost 3.11% of a week, in 8 of 28 chats; the other 20 had none (my sum of each row's "cache re-write" share times its cost, `notes/ledger/grand-theft-autism.json`; matches `source/dearest.py`).
- They cluster: one chat (caff6f5e) is 1.52%, half the total; then c079f576 0.47%, 423495d7 0.40%, 78cd6210 0.27%, 77034bac 0.24%; three chats under 0.12% (same file).
- All 8 were big chats when they lapsed: history 186k to 302k at the end (`grand-theft-autism.md`, step lines).
- Every row is an estimate (`src: estimate`) and every stage is "auto", so the record cannot say which stage each lapse fell in (same file).
- The record holds no times. It cannot say how long each gap was, what came before it (a render, a question to Sam, a night) or how many lapses each chat had. That is the main gap.
- The ledger cannot tell an idle gap from other re-writes: `source/stepcost.py` (line 474) counts as a lapse any new write beyond the growth since the step before. Something changing the start of the chat (tools loaded mid-chat, old tool results trimmed) would land in the same bucket. Unchecked which happened.
- A fresh chat is not free: in the chats with lapses, start-up before the first real work cost 0.08% to 0.94% of a week, and the floor was 80k to 82k (`grand-theft-autism.md`, start lines). The average lapse per affected chat is 0.39%. So "hand over before every wait" could cost about what it saves.
- Scale: the film cost 54.67% against 15%. Lapses are 6% of it; start-up reading (11.93%) and Claude's own writing (22.3%) are bigger (`dearest.py`).

## The real decision
Where the long waits fall in the film's whole chain of chats, and whether they fall inside big chats. The number of lapses is set by how waits are placed and how big a chat is when it waits, not by any one chat's behaviour. A bigger lever sits next to it: a cheaper start-up makes every wait-at-a-boundary cheap.

## Root cause
A big chat sits idle past the app's memory window, so its next step pays the write price for its whole history again. Evidence: lapses appear only in big chats, and one chat holds half. Not shown: the cause of each gap, and whether some "lapses" are not idle at all. CLAUDE.md's "back after an hour on amber or red: hand over" rule already exists but did not prevent these: it only fires on amber or red, and nothing checks it.

## Approaches weighed
1. **Learn first:** measure each lapse (minutes idle, what came before, history size, how many per chat) from the 8 chats and the 3 others this week, and keep it as a permanent ledger column.
2. **Reframe, waits at boundaries:** plan the chain so long waits (a long render, a question to Sam) come at the end of a chat, after its handover, not in the middle.
3. **Never idle:** while a render runs, the chat keeps doing real work (checks, notes) so the gap stays short. A "keep warm" ping loop was rejected: it breaks "one wait per render".
4. **Cheaper fresh chats:** cut start-up reading so a handover costs less than a lapse. This is already proposal 1 on the list and is not repeated here.

Chosen: 1, then one of 2 or 3, picked by what 1 shows.

## Proposal
**Step 1, learning (changes no film):** the cost ledger records, for every lapse, the minutes since the step before, what that step was (render wait, end of turn waiting for Sam, other), the history size, and whether the chat was idle at all. It runs on the 11 chats and on every chat from now on. Enforced: it is part of the ledger's existing split, which runs at every handover check; its own test is a made-up chat with one idle gap and one non-idle re-write, sorted correctly. Cost about 0.5% of a week (unchecked estimate).

**Step 2, one change, chosen by Step 1:**
- If waits for Sam make up most of it: a chat over about 150k that ends on a question for Sam writes its handover first, and a cold answer goes to a fresh chat. Enforced by the handover check, which flags any chat whose lapse column shows a cold reply carried on in place.
- If render waits make up most of it: the render runs in the background while the chat works its checks list, or the render ends the chat.
- If the lapses were not idle: fix the cause found (for example, load needed tools at the start).

Number to beat: lapses under 0.5% of a week per film (from 3.11%), with start-up plus lapse cost per wait lower than today's 0.39%, and no rise in Sam's notes. Measured by the ledger at the film's end review. Cost about 0.3% to 1% to build. Sam would notice nothing on screen; at most, an answer he gives may continue in a new chat.

## Sam test
- Q1: An expert measures before changing, and checks that a handover costs less than the lapse it prevents.
- Q2: It uses all 11 chats with lapses this week, not one chat, plus every later film.
- Q3: Enforced by the ledger and the handover check, not by a chat choosing to read a rule; success is one number per film.
- Q4: Four different approaches weighed; the start-up lever is named as bigger.
- Q5: Step 1 changes no film; Step 2 is one change that can be undone alone.
- Q6: Sources named; estimates and the memory window marked unchecked.
- Q7: Sized to cut 3.11% to under 0.5%, not a rule on paper.
- Q8: The measuring column is permanent; the change is reviewed at the film's end.

## Lost / Added
Lost: nothing on screen; a reply may continue in a new chat. Added: one ledger column; one change after it.

## Unchecked
The app's memory window length; the cost of Step 1 and Step 2; whether any lapse was not idle; how many lapses each chat had; the costs themselves (all estimates).
