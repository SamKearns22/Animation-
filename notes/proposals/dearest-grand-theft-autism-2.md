# Proposal: cost: Claude's own thinking and code writing (22.3% of a week on grand-theft-autism)

Status: open

## Problem
"Claude's own writing" (thinking, code, notes, messages) cost 22.3% of a week on grand-theft-autism (41% of all it spent), in 27 chats: the dearest thing. Older rows cannot split it; on the two fully named records thinking was 39-48% of it and writing code 32-38%. Sam's pick 2 (21 Nov list: "Claude's thinking and code writing"). Statement 1 (Sam, 13 Nov): every choice takes the way that gives higher quality first, then fewer notes and faults, then a film nearer 15% of a week; never one that trims the joke or reuses old content. The question: how can this thing cost less with no loss of quality, or buy more quality or fewer notes for what it costs?

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
<!-- verdict-hash: 8dd7b8368d3ab28d -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = helper A, V3 = chat. Picked: V1 (helper B). Critiqued: 7 found, 3 fixed, 4 named.

## Leak
none
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 4 | 4 | 3 | 4 | 4 | 19 |
| V3 | 3 | 2 | 3 | 3 | 4 | 15 |
## Sam test
Q1: Yes. An expert measures where the words go (first build or rework, by shot) before cutting anything, and attacks rework, the biggest waste. Thinking and effort are not cut blindly.
Q2: The scope is right. It covers all 28 chats of the film (re-tagged from the chat records and Sam's messages) plus the named rows of check-repairs, and it judges at the scale of the whole film, not one chat.
Q3: Tools enforce it (the handover and sending check), not a chat's choice. Gap mended: a still can pass checks that cannot see the fault, so each check the gate relies on must first be shown to flag Sam's own earlier marked-up pictures. Success has a number: the share of Claude's words spent on rework, and the count of repeated notes.
Q4: Four to five really different approaches were weighed: rework, effort, chat length and kit reuse. The ledger shows length makes no difference to the share (41.9% in long chats against 41.3% in short), so rework is the best lever.
Q5: The learn step changes nothing. The gate is a single change, made only after the numbers support it, and it can be removed on its own. Weak spot (named): the "half or more" threshold was set before measuring.
Q6: Checked against the ledger: 23.55% of a week from the origins column (14.05% writing, about 9.5% re-reading); 7.77% in chats 1-10 against 15.79% in chats 11-28; the sausage arm given a fourth time. "Opus high on note rounds" rests only on the notes text, because rows have no effort field. Costs are estimates.
Q7: Not the cheap version. It spends one stage per shot to save whole rebuilds and does not trim thinking or effort. Its honest cost: about 1% of a week to learn, plus the gate build.
Q8: The ledger fields and the gate are permanent, reviewed when Sam calls the film complete. No trial.
## Pick
V1
## Why
V1 and V2 both see the real decision: this film paid for Claude's words about twice over because shot 4 was rebuilt again and again (chats 11-28 cost 15.79% in words against 7.77% for the first build). V1 checks more of the facts. It found the second named record (check-repairs), which V2 says it could not find, and it showed chat length has no effect, so V2's later chat-length limit has no case behind it. V1's gate stops a fault before its code is written, which saves the thinking and code directly. V2's gate only acts after Sam has already seen a fault once. Taken from V2: the learn step also splits words by shot and pulls note and repeat counts from Sam's own messages; and the gate's checks must be proven on Sam's old marked-up pictures, so the gate cannot pass on paper. Taken from V3: the film-end review lists which notes cost the most words to fix. V3's other parts are unmeasured, bundle three changes into one yes, and lean on effort, so they were dropped.
## Faults in the pick
- F1 [fixed] The learn step only re-tagged from notes. It now also splits words by shot and fills in note and repeat counts from Sam's messages (from V2).
- F2 [fixed] The gate could pass stills with checks blind to the fault. Each check it relies on must first flag Sam's earlier marked-up pictures.
- F3 [fixed] It overlapped the existing acting-list check before animatics (rule 74). The gate is now built into that check, one step earlier, not added as a second list.
- F4 [named] "Note rounds ran on Opus high" comes from the notes text, not the ledger. The new effort field settles it.
- F5 [named] The "half or more rework" threshold was set before measuring.
- F6 [named] Even halving Claude's words saves about 12% of a week. This alone will not bring a film to 15%.
- F7 [named] All costs are estimates from the chat records, not the app's own figures.
## Final version
**Learn (changes nothing; about 1% of a week; one Opus-medium chat).**
- Re-tag this film's 28 ledger rows from its chat records, notes and Sam's messages. Each row gets: stage, effort, first build or rework, which shot, Sam's note count and repeats.
- From now on the ledger fills these fields on every row by itself, from the chat-opening step and the handover check. No row reads "auto, 0 notes" again.
- Report: the share of Claude's words spent on rework, by shot. The share spent at high effort on note rounds. Which notes cost the most words to fix (kept for the film-end review).

**Then one change, chosen by the report (its own yes):**
- If rework is half or more of Claude's words: a **pre-code still gate**. Before a shot's moves code is written, one still per beat is drawn and must pass the seeing checks (body, back view, crowd, held object, contacts). Each check it uses must first be shown to flag Sam's earlier marked-up pictures. The gate sits inside the existing acting-list check (rule 74), one step earlier. The handover check refuses a handover with moves code that has no passed stills.
- Only if high effort on note rounds costs more than rework does a separate effort change go to Sam, with its own test.

**Numbers to beat:** the next film's share of Claude's words spent on rework, against this film's measured baseline; and repeated notes (rule 30), aiming for none.

**Review:** at film end, against these numbers. The gate can be removed on its own if it adds cost without cutting rework.

**Honest size:** at best about 12% of a week saved on a film like this. Start-up reading (11.9%) and the number of chats still need their own fixes.
## For Sam
### Option 1: Measure the rework, then stop bad drawings before they are animated
Most of Claude's writing on this film went into redrawing shot 4 again and again. First we tag every chat so we can see how much was redoing work you had already rejected (no change to the film). If that is half or more, every shot gets a set of key still pictures that must pass the checks before any movement is written. Each check must first prove it would have caught your earlier notes.
What you'd notice: fewer versions of the same shot coming back with old faults. Clips may come a little later but right.
Lost: a shot can no longer go straight to movement before its stills pass.
Added: four facts recorded per chat, automatically; a stills check before movement (only if the numbers back it).
### Option 2: Measure, then block repeated notes from reaching you
The same measuring step first. Then any clip that fixes a note you have given before cannot be sent until the new check has caught your own marked-up picture of that fault. Later, as a separate choice, a limit on chat length.
What you'd notice: a note you have given before should not come back. It acts only after a fault has reached you once.
Lost: some clips that fix a repeated note arrive later.
Added: a measuring tool; a repeat block in the sending step; later, a chat-length limit.
