# Proposal: cost: memory lapses (re-paying for the whole chat) (3.11% of a week on grand-theft-autism)

Status: open

## Problem
"memory lapses (re-paying for the whole chat)" cost 3.11% of a week on grand-theft-autism (6% of all it spent), in 8 chats: number 3 of the dearest things. Statement 1 (Sam, 13 Nov): every choice takes the way that gives higher quality first, then fewer notes and faults, then a film nearer 15% of a week; never one that trims the joke or reuses old content. The question: how can this thing cost less with no loss of quality, or buy more quality or fewer notes for what it costs?

## Facts
- ledger rows: notes/ledger/grand-theft-autism.json, each chat's split (named from 21 Nov on; older rows only coarse), added up by source/dearest.py
- the whole ranking: python3 source/dearest.py grand-theft-autism
- the films' costs and notes per round: notes/ledger/FILM.md

## Record
notes/ledger/grand-theft-autism.md
notes/ledger/grand-theft-autism.json
source/stepcost.py
source/dearest.py

## Verdict (the judge, word for word)
<!-- verdict-hash: 6c7c12dbba2a8a9c -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = helper B, V3 = chat. Picked: V1 (helper A). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
none
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 4 | 4 | 5 | 20 |
| V2 | 4 | 3 | 3 | 4 | 5 | 19 |
| V3 | 3 | 3 | 3 | 2 | 4 | 15 |
## Sam test
Q1: Yes: an expert times each lapse before changing behaviour, and checks that a fresh chat (start-up 0.08% to 0.94% of a week) really costs less than the lapse it prevents (0.39% average per affected chat). V1 is the only version that does that sum.
Q2: Yes once widened: Step 1 runs on every lapse chat of the week (11, `notes/proposals/dearest-week.md`, 4.22%) and on every chat after, not only this film.
Q3: Root cause is found by Step 1, not assumed. Enforced inside the cost split that already runs at every handover check, with its own made-up-chat test; success is one number per film (lapses under 0.5% of a week, with no rise in start-up cost or notes).
Q4: Four different approaches weighed (measure, waits at chat ends, never idle, cheaper fresh chats); the choice between them is left to the timings. Bigger levers (start-up 11.93%, Claude's writing 22.3%) are named, not hidden.
Q5: Step 1 changes no film. Step 2 is one change, put to Sam as its own yes, undone alone if it misses.
Q6: Facts checked against the ledger and `source/stepcost.py` (line 474). Two facts added by the judge: the raw chat records do hold times; this session's own record shows the one-hour memory in use. Each lapse's actual gap is still unchecked until Step 1 runs.
Q7: Sized to cut 3.11% to under 0.5%, every lapse measured, not a sample; build cost stated (about 0.3% to 1%, unchecked).
Q8: The timing column is permanent; Step 2 is made properly or not at all, reviewed at the film's end.
## Pick
V1
## Why
V1 and V2 share the right shape: measure first, then one change chosen by what the measuring shows. V1 wins because it does the sum the other versions skip: a fresh chat is not free, so "hand over before every wait" (V3's idea) could cost about what it saves. V1 also names that the counter cannot tell an idle gap from a re-write caused by something else (tools loaded mid-chat, the start of the chat changing). V2 rests partly on a wrong lead: its approach 3, "use the longer one-hour memory", is already in use (this session's record writes only to the one-hour memory, none to the five-minute one), and its 1-2% build cost is high for reading a time stamp. V3 bundles three changes in one yes and acts before learning the cause.
Checked by the judge and added: (a) the ledger has no times, but the raw chat records it is built from carry a time on every step, so Step 1 is reading data already there, not new recording; (b) 20 of the 28 chats had big histories too (100k to 330k) and no lapse, so size alone is not the cause: the gap is. Taken from V2: the "done when no lapse is listed as unknown" bar, and classing waits by render, Sam, helper.
## Faults in the pick
- F1 [fixed] V1 says the record holds no times; the raw chat records do. Step 1 now reads those, which makes it cheaper and certain.
- F2 [fixed] V1 did not say when Step 1 is finished; added V2's bar: every lapse in the week has a cause, none "unknown".
- F3 [fixed] Lapses happened in only 8 of 28 big chats; the final version says so, so Step 2 targets the gap, not chat size.
- F4 [named] Older chats' raw records may not all still be on hand (only this session's was found here); if some are gone, Step 1 covers the ones that remain and every chat from now on.
- F5 [named] All costs are estimates; build cost (0.3% to 1% of a week) unchecked.
- F6 [named] Step 2 is not decided yet: Sam gets a second yes after the timings, so this saves nothing until then.
## Final version
**Problem.** Memory lapses cost 3.11% of a week on grand-theft-autism (4.22% across the week's 11 lapse chats). They are bunched: one chat (caff6f5e) is half. They happen only in big chats, but 20 other big chats had none, so the gap before a step, not size, is the likely cause. The chats keep their history in a one-hour memory; a step after a longer silence pays to write the whole history again. Unchecked: how long each gap was, what it was waiting for, and whether some "lapses" were not silences at all.

**Step 1, learning (changes no film).** The cost split, which already reads each chat's raw record at every handover check, also reads the time on each step. For every lapse it records: minutes since the step before; what that step was (render wait, waiting for Sam, waiting for a helper, other); history size; and "not idle" if the gap was short (then the cause is something changing the start of the chat). It shows one line per chat in the ledger. Its test: a made-up chat with one long idle gap and one short non-idle re-write, each sorted correctly. Run on every lapse chat of the week whose record remains, and on every chat from now on. Done when every lapse has a cause, none "unknown". Cost about 0.3% to 1% of a week, once (unchecked).

**Step 2, one change, chosen by Step 1, put to Sam as its own yes:**
- Waits for Sam lead: a chat over about 150k that ends on a question to Sam writes its handover first; an answer arriving after the memory has lapsed goes to a fresh chat. The handover check flags any cold answer carried on in a big chat.
- Render waits lead: the render runs in the background while the chat works its checks, or the render ends the chat after its handover.
- Not idle: fix the cause found (for example, load needed tools at the start).

**Number to beat:** lapses under 0.5% of a week per film, with start-up plus lapse cost per wait below today's 0.39%, and no rise in Sam's notes; read from the ledger at the film's end review. Undone alone if it misses.

Lost: nothing on screen. Added: a timing line per chat in the cost record; later, one change by its own yes.
## For Sam
### Option 1: Time the forgetting first, then fix the real cause
When a chat sits silent for over an hour, it forgets its history and pays to read it all again; that cost 3% of a week on this film, half of it in one chat. Every step already has a clock time in the chat's record, so first the cost tool reads those times and says, for each lapse, how long the silence was and what it was waiting for (a render, your answer, a helper). Then I bring you one fix that matches the real cause. You would notice nothing in the films; later, an answer you give may carry on in a fresh chat.
Lost: nothing on screen.
Added: a timing line on each chat's cost record; later, one fix, asked as its own Y or N.
### Option 2: Hand over before every long wait, now
Before any long render or a question to you, the chat writes its handover first, so your answer lands in a small fresh chat; the cost record also notes each lapse's cause. Quicker to start, but a fresh chat costs to start up, so on some waits it may cost about what it saves, and it is chosen before we know the cause.
Lost: nothing on screen; your answers may go to a new chat rather than the one that asked.
Added: a handover before long waits, three changes in one yes.
