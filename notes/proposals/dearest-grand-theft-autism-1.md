# Proposal: cost: start-up reading (rules, tools, first files) (11.93% of a week on grand-theft-autism)

Status: open

## Problem
"start-up reading (rules, tools, first files)" cost 11.93% of a week on grand-theft-autism (22% of all it spent), in 28 chats: number 1 of the dearest things. Statement 1 (Sam, 13 Nov): every choice takes the way that gives higher quality first, then fewer notes and faults, then a film nearer 15% of a week; never one that trims the joke or reuses old content. The question: how can this thing cost less with no loss of quality, or buy more quality or fewer notes for what it costs?

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
<!-- verdict-hash: 1b3d290847b7cb70 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = chat, V3 = helper B. Picked: V1 (helper A). Critiqued: 5 found, 2 fixed, 3 named.

## Leak
none
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 4 | 5 | 5 | 21 |
| V2 | 3 | 2 | 3 | 2 | 4 | 14 |
| V3 | 4 | 3 | 3 | 4 | 4 | 18 |
## Sam test
Q1: Yes. An expert measures what fills the step-1 load, and which tools are ever used, before cutting it; rewording our rules again (already done 16 Nov) would be the amateur move.
Q2: Scope is the whole film's 2,775 steps and two films' tool use, the unit that sets the cost. Weak spot: the film has no recorded notes (every row 0, source "estimate"), so quality cannot yet be set against cost; named.
Q3: Root cause shown with numbers (82k x 2,775 steps x $0.18/M is about $41, nearly the whole line). Enforced by the record and the handover check, not by a chat choosing to read. Success: the floor read from the ledger for every chat.
Q4: Five different approaches weighed (condense, fewer steps, smaller app load, learn first, model mix); the text-cutting and model-mix ones are shown to be small or already a rule.
Q5: This yes changes no film. The later connector switch-off is one setting, undone with one setting, and comes back as its own question with its figures.
Q6: Floor sizes, steps, Opus share, CLAUDE.md growth and the re-read price checked against the ledger, git and costwatch. Per-connector size, the 21 Nov cause and the saving are marked unchecked.
Q7: Sized by the result: it goes after the ~95% of the load that is not ours, not the 5% that is cheap to edit.
Q8: Record fields and the flag are permanent, reviewed at film end; no trial.
## Pick
V1
## Why
V1 and V3 find the same real decision (size of step 1 x steps x price, mostly the app's part), but V1's facts are exact (floor 80-82k in 25 chats, 91/95/95k in the last three of 21 Nov; checked in the ledger), while V3 says the rise came "on 21 Nov" generally and that the opening is "identical in all 28 chats", which the ledger contradicts. V1's connector-call count over two films answers "is it used?" directly from chat records, where V3 needs Sam to run an empty test chat. V3 also bundles a new check build (change A) on the steps lever, which overlaps the dearest item 1 proposal; V1 rightly hands steps there. V2 rests on a wrong fact (it says every chat starts at 91-95k; only 3 of 28 did), bundles four changes into one yes (measure, switch off connectors, cut hook printouts, cap CLAUDE.md), and sets a "under 70k" target with nothing measured behind it.
Taken from V3: keep one web search for reference photos whatever the counts say (the reference-photo search order needs it); a size threshold before the switch-off comes to Sam; and its count of back-to-back independent searches, recorded as data handed to the item 1 proposal, not as a check built now.
## Faults in the pick
- F1 [fixed] V1 could switch off the web search that reference-photo searches use; the final keeps one web search regardless.
- F2 [fixed] No threshold for bringing the switch-off to Sam; the final asks only when unused connectors carry at least 10k tokens of the floor.
- F3 [named] Many connector tools load as names only until fetched; only their instructions and a few tools sit in full in step 1. So switching connectors off may save less than the 13k rise suggests. The measurement settles this before Sam is asked.
- F4 [named] The film's notes are not recorded (0 everywhere), so "no loss of quality" can be shown only on the next film.
- F5 [named] Whether a connector switched off in the app leaves cloud chats is unchecked; the next chat's floor shows it.
## Final version
**Learn (this yes only; changes no film; about 0.5-1% of a week once, Opus medium).**
1. The cost record (stepcost) adds three figures per chat: our part of the step-1 load (CLAUDE.md, agent files, hook printouts, opening prompt, counted exactly), the app's part (the rest), and for each connector its tool calls, plus which of its tools are loaded in full at step 1 and how big its instructions are.
2. The handover check prints one line when a chat's step-1 load is 3k tokens or more above the last film's.
3. A one-off pass over this film's and the last film's chats (chat-reading tools) fills in connector calls, and counts runs of back-to-back searches that did not depend on each other (ledger search list). That count goes to the item 1 (steps) proposal as evidence; nothing is built from it here.

**After, each its own question through the route:**
- (a) If connectors with zero calls in two films carry 10k tokens or more of the step-1 load, Sam is asked to switch them off, keeping one web search for reference photos. Number to beat: step-1 load back to 82k or below, read from the ledger, with no chat blocked for a missing tool. Undone by switching them back on.
- (b) Steps per film: the item 1 proposal, with the count from step 3. Number to beat: fewer steps for the same work, notes and repeated faults no higher than the last two films (needs notes recorded).

What Sam notices: nothing now; later at most one settings question.
## For Sam
### Option 1: Measure the start first, then switch off unused add-ons
Every chat pays again, at every step, for a big block of instructions it is given at the start; most of that block is the app's, not ours, and it grew by about an eighth on 21 Nov without anyone noticing. This first step only measures it: each chat's cost record says how big the block is, how much is ours, and which add-ons (connected services like web search) were ever used, and a warning appears if it grows. If unused add-ons turn out to be a big part, you get one plain question to switch them off on your phone, with the saving; web search for reference photos stays.
Lost: nothing now; later, possibly add-ons no film has used.
Added: three figures on each chat's cost record, one warning line, a one-off count.
### Option 2: Measure, plus build a check for more work per step
The same measuring, plus a check that notices when a chat does searches one at a time that could have gone together, so films take fewer steps. Bigger in reach, but it builds a check before we know how often this happens, and it overlaps the separate proposal on Claude's own writing.
Lost: about 1% of a week more to build, before its value is known.
Added: the same figures, plus a check line in each chat and a steps count at handover.
