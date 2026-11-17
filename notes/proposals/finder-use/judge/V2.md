# Helper B: finder use

## Leak
Mild: "finder only covers the film's own code, not shared tools" points at extending it; no fix stated.

## Results
- 16 Nov, 19 Opus chats, 35.18%: film-file search 6.65%, tool search 3.22%, page.py 0.21% (= 28% of Opus cost). Calls: 891 searches vs 21 page.py over 1,305 steps (ledger protest-tiers.json).
- 6 of 19 chats never called show: film-file search 26.6% of their cost vs 15.9% in the 13 that did (my sums, ledger). Finder chats still made 6-44 film-file searches each.
- The measure mislabels (stepcost.py `kind_of`, `_film_paths`): "film-file" includes greps of story/protest-tiers* notes and ls/head/tail; "tool search" includes rulebook/guide greps CLAUDE.md prescribes. "46 times" and "shared tools 3.22%" are not what they say.
- Handover flag is per day (handover.py `finder_faults`); first show 09:15 (show log) silenced the day. The adopted spec was per note ("lists notes fixed with no show call or with hand searches after it"): built short.
- handover-end.log stores only time and session (`end_stamp`), never faults: "no FINDER line" proves nothing.
- Show log has no session id: calls cannot be tied to chats.
- 16 Nov notes were mostly builds (A4-A12 an 11-step plan; F12-F23 built in one chat; notes/archive/protest-tiers.md).
- Film files 3,846 / 2,205 / 1,991 lines; rule 61 says split over ~1,000 (warning only).
- Change 2 is on by default (page.py:352, "Sam's yes, 16 Nov"); whether during those chats: unchecked.
- **Gap:** nothing splits searches by purpose (locate a note / every use of a name or verify / build / rules or notes lookup).

## The real decision
What finding code costs across a film's chats, and which lever cuts it most. Bigger levers: chat length (re-reads; Sam's 17 Nov Y covers it), oversized film files, size of each result.

## Root cause
1. Enforcement is day-level and after the fact, so it never fires; skipping chats paid ~1.7x for film search.
2. One look per note cannot replace "every line naming X" (call sites, tables like ALLOWED_POPS) in builds and multi-place fixes; grep is right there. A searches-to-finder ratio is the wrong target.
3. The measure mixes purposes, so nobody knows which part is waste.
4. Files are 2-4x rule 61's size.

## Approaches weighed
A. Enforce finder-first per chat at the moment of use.
B. Reframe: cap search result size (cost = size x later steps), for all searches.
C. Reframe: rule 61's split as a gate for new films.
D. Extend finder to shared tools (unmeasured).
E. Learn first: split the measure by purpose; session id on show calls.
Chosen: E, then A; B, C, D each wait for E's number.

## Proposal
**Learn (no film change, ~0.5% of a week):** stepcost splits searches into film code before the chat's first show / after it / film notes / shared code / guides; ls stops counting. Show log gains the session id. Runs on every chat via the Stop hook; read at the next film's first notes round. Answers: the "locate" share of round cost; which shared tools.

**Change 1 (own yes, ~0.5%; evidence in):** the adopted per-note check, per chat. A hook prints one line on a chat's first film-code search with no show yet in that chat (warns, never blocks: build searches are legitimate). `handover.py end` lists each chat that edited film code with no show, with its pre-show search count. Bar: 0 such Opus chats (16 Nov: 6 of 19); under 1 pre-show film-code search per note; from the new split.

**Changes 2-4 (each own yes, only if Learn shows it):** D if shared-code locate searches >= 3% of round cost; B if results average over 1,500 tokens; C if search cost per note rises with file size over two films. Each its own bar, undone alone.

**Cost:** ~1% once vs 15% per film; one day spent 9.87% searching; halving locate searches saves an estimated 2-3% per round day.

**Sam notices:** nothing in films.

## Sam test
- Q1: measures the right unit first, enforces at use.
- Q2: all the film's chats; next round is the unseen test.
- Q3: causes evidenced; the hook fires in every chat, no reading needed; show-then-grep shows in the after-show split.
- Q4: five different approaches; three reframes wait for their numbers.
- Q5: warns, never blocks; each part undone alone; nothing unshown asked.
- Q6: every figure from ledger, logs or code named; estimates marked.
- Q7: completes the adopted spec rather than a cheap flag; sized to the result.
- Q8: measure and hook permanent, reviewed at the film's end.

## Lost / Added
Lost: day-level flag. Added: split measure, session id, one-line reminder.

## Unchecked
16 Nov transcripts; when change 2 went on; split by purpose; saving; result sizes.
