## Leak
Mild. The name "finder-first" and the count "65 hand searches for every finder use" assume the answer is more finder use. No fix is stated outright.

## Results
- Milburn so far is all building: no notes rounds, and sets, props, build and board are done (notes/ledger/milburn.md stage table, "0 rounds"). The ledger's "notes ticked" is 0 in every row, so searches per note cannot be measured (milburn.json).
- 779 hand searches: 248 in the film's own code, 531 elsewhere (328 in shared tools). 12 finder uses (problem file; per-chat sums re-added from milburn.json).
- Cost estimate: 8.04 of 32.14 points, 25% of the film's spend. Sam's own reading puts it a third lower, about 5.4% of a week, against a 15% target for the whole film (problem file; ledger).
- Where the film-code searches fell: 74 in chats with no finder call, 13 before the first call, 43 within 10 calls after a call (a miss), 118 later (milburn.json).
- 9 shared tools take 197 of the 328 shared-tool searches. facehouse.py has 1,703 lines, people.py 939 and people_parts.py 665; none has a line starting "MAP" (checked with grep). The finder reads only source/FILM*.py (page.py; finderwarn.py film_re).
- The record cannot yet say why each search was made: to place a note, to learn how a tool works, or to check an edit. This is a gap.

## The real decision
How a chat at any stage finds the code it needs, across the film's code and the shared tools, in the fewest steps. The bigger lever is the 531 searches outside the film's code (5.27 points, against 2.77 for film code), which the finder cannot answer at all. The real question is how to find code, not how to get the finder used.

## Root cause
The 17 Nov reminder (.claude/hooks/finderwarn.py) could reach at most 87 of the 779 searches (11%), because:
1. It speaks once per chat, and only before the first finder call. The 161 searches after a call get nothing.
2. It covers only the film's own files. The 531 other searches get nothing.
3. Its own text excuses the search: "Building something new may search on purpose; then carry on." Every Milburn chat was building, so every chat could rightly take that exit.
4. The finder answers a different question. It takes a note's words, a shot and a time, which fits notes rounds, but building asks "what does people.py's turned head take?". Shared files with no map leave a hand search as the only way in. The 43 misses show that it also fails on some of the questions it does get.

The earlier fix's own bar ("no Opus round chat edits film code without a show") was never tested, because Milburn had no rounds.

## Approaches weighed
1. **Hard gate.** Refuse any hand search until the finder has run. This blocks legitimate build searches and does nothing for the after-call misses.
2. **Reframe: one locator for all code.** The finder also covers shared tools, using a map made from each file's functions and docstrings, so one step answers a build question too.
3. **Reframe: the search comes to the locator.** When a chat hand-searches code, a hook runs the locator on the same words. If the locator has a confident answer, the search is turned away with that answer in its place. If not, the search goes ahead. Nothing relies on the chat choosing to comply.
4. **Make each search cost less.** Cap result size, and split big files (rule 61) for shared code. This treats the cost, not the step count.
5. **Learn first.** Label why each Milburn search was made, and replay a sample through the finder to see what one step would have answered.

Chosen: 5, then 2, then 3, each as its own yes. Approach 4 waits for a number.

## Proposal
**Learn (own yes; about 1.5% of a week; changes nothing).** One Opus chat reads Milburn's 15 transcripts through stepcost. It does four things:
- labels every hand search by purpose (place a note / learn a tool / read notes or guides / check own edit);
- replays 60 searches (30 in film code, 30 in shared tools) through the finder and through a draft map of the shared tools, and counts the answers one step gives;
- records whether the reminder fired in each chat;
- adds the purpose label to the ledger's per-chat search record for good, so every film reports it at its review.

**Change 1 (own yes; about 3%; only if the replay shows the shared-tool map answers at least 60% of "learn a tool" searches).** page.py `find` covers the film's code and every shared tool. A kittest keeps each tool's map current: it fails when a function has no map line. The bar: shared-tool hand searches fall from 22 per chat (328 / 15) to under 8, measured by the same ledger columns on the next film.

**Change 2 (own yes; about 2%; after change 1).** A hook that runs before each search turns the redirect on (approach 3). It replaces the 17 Nov reminder. A grep the locator cannot answer goes ahead, so building is never blocked. The bars:
- film-code hand searches per chat under 5 (Milburn: 16.5);
- misses under 1 in 5 of locator calls (Milburn: 43 in 12 calls);
- search share of film cost under 10% (Milburn: 25%).

Each change is undone alone by removing its hook or file. All three are reviewed at the film's completion.

**Cost:** about 6.5% of a week once, then nothing extra per film, against about 5.4% per film now spent searching (estimate).

**Sam notices:** nothing in the films, and one line of search results at each film's review.

## Sam test
Q1: Yes. An expert measures purpose first, then makes the cheap path the automatic one rather than adding another reminder.
Q2: The scope is all 15 Milburn chats and all 779 searches, not just film code. A replay against real searches is the right evidence.
Q3: The root cause comes from the hook's code and the ledger. Change 2 does not depend on a chat reading anything.
Q4: Five different approaches were weighed. Two reframe the problem and one is learn-first.
Q5: Learn changes nothing. Each change has its own bar, comes after the evidence, and is undone alone.
Q6: The figures were re-added from milburn.json; MAPs were checked by grep; the rest is marked below.
Q7: It goes for the 531 searches the cheap fixes ignored, and it is not a third reminder.
Q8: All three are permanent once adopted and are reviewed at film completion. Nothing is a trial.

## Lost / Added
Lost: the 17 Nov once-per-chat reminder (replaced by change 2).
Added: a purpose label on every search record; maps of the shared tools with a check that keeps them current; a hook that answers a hand search with the locator's result.

## Unchecked
- Whether the reminder fired in Milburn chats.
- The split of searches by purpose.
- The hit rate of a shared-tool map.
- That each search costs the same (used for the 3.3-point shared-tool share).
- The build and replay cost estimates.
