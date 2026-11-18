# Helper B: finder-first

## Leak
Yes, mild: the title and "about 65 times for every finder use" make finder use the target, which points at forcing the finder. Ignored.

## Results
- Milburn ledger (notes/ledger/milburn.json, re-summed): 15 chats, 1,259 steps, 779 hand searches = 62% of all steps; 12 finder calls. Search cost 8.04 of 32.14 estimated points (25%): film code 2.77, other files 5.27.
- 531 of 779 searches (68%) were of files the finder cannot read at all: 328 shared tools (49 files), 81 film notes, 21 guides, 101 other.
- Repeated across chats: handover.py searched in 12 of 15 chats, people.py in 7, kittests.py 7, people_parts.py 6, preflight.py 6, views.py 6 (milburn.json, per-chat `search.other`). Each fresh chat re-learns the same kit and process tools.
- Film code (248): 74 in the 8 chats with no finder call; 161 in chats after a finder call (43 within 10 calls = misses).
- Every stage done was building (sets, props, build, board; milburn.json `stages`); no notes rounds. Sets planned 1.8%, ~16.7% spent by their end. The show log (notes/logs/milburn-show.log) holds 13 note look-ups, so some chats fixed board notes, but ledger `ticked` is 0 everywhere.
- The 17 Nov reminder (.claude/hooks/finderwarn.py) fires once per chat, only on film code, and says "Building something new may search on purpose; then carry on." In a building film it invites chats to carry on, and it is silent for 68% of searches and after any one finder call.
- Even at zero search cost the film would sit near 24 estimated points (about 16% real at Sam's 22% reading); search fixes alone cannot reach 15%.

## The real decision
Not "how do chats use the finder more" but: how does every chat of a film get each fact it needs (a note's lines, a kit's API, what a check's fault means) in one step, without each new chat re-learning it. Bigger levers than the finder: the 328 shared-tool look-ups repeated chat after chat, and process tools (handover.py, preflight.py, kittests.py) whose output sends chats into their code.

## Root cause
1. The finder answers one question (where does this note touch the film's code), but Milburn's chats were mostly asking others (how does this kit work, why did this check fail). The tool fits a minority of searches.
2. Nothing carries what one chat learned to the next; a 15-line handover cannot hold a kit's API, so 12 chats each search handover.py.
3. Both earlier fixes were advice tied to finder use (a start line, then one warning per chat with a built-in exit). Advice that excuses building cannot change a building film. Whether it was even printed is unchecked.

## Approaches weighed
1. Force the finder: block hand search of film code until `show` runs. Touches 32% of searches; blocks legitimate building.
2. Reframe, widen the one-step answer: `show` also searches the shared kits the film imports, by their MAPs.
3. Reframe, carry knowledge: a kit card per film (functions used, file:line) written by the chat that learned it, read by the next.
4. Reframe, fix the source: process tools print the cause and the fix with every fault, so no chat greps them.
5. Learn first: classify every Milburn search by the question it asked, and replay which one-step answer would have served it.
Chosen: 5, then the one of 2, 3, 4 (or 1) the classification shows carries the most cost, one at a time. Classifying 779 searches costs little next to 8 points; building 2 or 3 blind could again fit the minority.

## Proposal
**Learn (its own yes; changes nothing; about 1.5% of a week; Sonnet).**
(a) Read the search calls of all 15 Milburn chats (session ids in milburn.json, `list_events`). Label each by question: note locate / kit API while building / process-tool fault / same-chat repeat / repeat of an earlier chat's look-up.
(b) Replay a sample of 60 against `page.py show` now and against a kit-wide `show`: one-step hit or not.
(c) Permanently, stepcost records each search's file and pattern on the ledger row (not only counts), so every later film answers (a) automatically, and the reminder's printing is logged.
Output: cost per label and per remedy in % of a week.

**Then one change at a time (each its own yes, its own bar, undone alone):**
- If kit-API and cross-chat repeats carry the most: approach 2, enforced by the hook: a hand search of a shared kit with no kit `show` in that chat is refused once with the show command (one retry allowed).
- If process-tool faults carry the most: approach 4 for the named tools; enforced by a kittest that every fault line carries a fix.
- If note-locate misses carry the most: fix `show` on the missed notes.
Bar for the whole film, measured by stepcost at the next film's review: hand-search cost under 10% of film cost (25% now) and under 1.5% of a week; no shared file searched in more than 2 chats.
**Cost:** learn 1.5%, each change 0.5-1.5%, against 8 estimated points spent searching in Milburn.
**Sam notices:** nothing in the films; a short results line, then one change at a time put to him.

## Sam test
Q1: An expert measures what the searches were for before building a tool; yes.
Q2: All 15 chats and every search, both files kinds; Protest Tiers kept for comparison. Wider than the finder's frame.
Q3: Root causes evidenced; measurement runs in every chat by hook; each change is enforced by hook or kittest, not reading.
Q4: Five different approaches; the choice is the one that cannot fit the minority again.
Q5: Learn changes nothing; each change is undone alone; nothing unshown is trusted.
Q6: Figures re-summed from milburn.json; hook wording read; reminder printing unchecked.
Q7: Sized by the 8 points it targets; the bar is the whole film's search share, not finder counts.
Q8: The search record is permanent; each change is permanent once said yes, reviewed at film completion.

## Lost / Added
Lost: about 1.5% of a week before any fix; for a later shared-kit gate, one refused hand search per chat.
Added: a permanent per-search record; later one remedy at a time.

## Unchecked
Whether the reminder printed; real (app) costs; how many searches were legitimate building; whether `list_events` returns every tool input for finished chats.
