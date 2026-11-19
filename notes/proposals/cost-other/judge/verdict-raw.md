## Leak
yes: the title ("Name what is in ... other") frames the answer as relabelling the leftover, and the Facts' "prototype split" and "How other is made" list the very sub-kinds to split it into. It also states, unchecked, that the kind shares are "shares of a total off by about half"; the record (notes/proposals/cost-other/milburn-usage.md) shows the dollar estimate matches the app within 1%, so the gap is the week size, not the shares.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 2 | 3 | 4 | 5 | 18 |
| V2 | 4 | 3 | 4 | 4 | 5 | 20 |
| V3 | 2 | 2 | 3 | 3 | 5 | 15 |
## Sam test
Q1: Yes, as patched: an expert first splits real dollars by where the tokens came from (start-up floor, carried history, new writes, Claude's own output), for the whole film, then cuts the biggest block. Done here on real app figures.
Q2: Whole film, real app dollars for 13 of 15 Milburn chats (milburn-usage.md), plus Sam's own notes count (milburn-review.md: 33 notes, 4 repeats). No costly replay of transcripts.
Q3: Root cause named (stepcost charges only tool results; everything else falls to the leftover). The new split runs by itself at every chat's end, and its test fails unless the parts add to the chat's real cost within 1% with a leftover under 5%, so it cannot pass on paper.
Q4: Five approaches weighed across the versions (more labels, exact split by origin, learn from app figures, replay transcripts, cut now); exact split plus the existing app figures is the best of them.
Q5: One change in this yes, one file, guarded by its test, undone by reverting it. Cuts come later, each with its own yes and number.
Q6: Facts checked: app $74.59 vs ledger $73.84 on 13 chats (milburn-usage.md); 33 notes and 4 repeats (milburn-review.md); WEEK_USD 245 "PROVISIONAL" (costwatch.py:26). Start-up floor share and the two missing chats: unchecked, marked.
Q7: Sized to remove the leftover entirely, not to relabel it; ~1.5% of a week once, stated.
Q8: Permanent once made; reviewed at the next film's end against its numbers.
## Pick
V2
## Why
V2 is the only version resting on measured results: it read the app's real usage for 13 Milburn chats and found the estimate right in dollars, which settles the 47% gap as the week size (already owned by notes/proposals/estimates.md, so not bundled) and gives a real split now (re-read 45%, writes 30%, output 25%). V1 proposes a learning step whose answer is already in the repo and leaves the gap's cause "unchecked"; its strong part is the design of the tool change. V3 gives up the Milburn answer and bundles the gap fix with the labels, and its labels still leave a leftover.
Taken from V1: split each step exactly by token origin (no leftover by design), with a test that the parts add to real cost within 1% and the leftover is under 5%, in place of V2's "leftover under 15%". Taken from V3: no list_events replay. Added by the judge: V2's second change (record each chat's purpose and notes) is dropped from this yes because Milburn review item 5 already proposes the ledger counting notes and repeats; it goes there, not duplicated.
## Faults in the pick
- F1 [fixed] V2's leftover target (15%) let a split pass while still hiding cost; now an exact origin split, leftover under 5%, parts within 1% of real cost (from V1).
- F2 [fixed] V2 put two record changes in one plan; the notes/purpose record moves to Milburn review item 5, so this yes is one change.
- F3 [fixed] V2's learning step re-did work already in milburn-usage.md; it shrinks to adding the start-up floor and fix-chat columns from data in the repo (~0.3%).
- F4 [named] Two Milburn chats (5c55685c, ce8f146c) have no app figure, and step-1 size per Milburn chat is not stored; the floor share for Milburn is an estimate (~90k x steps).
- F5 [named] Sam's 22% may include other jobs run on 17-18 Nov; the week size is settled in the estimates proposal, not here.
- F6 [named] This measures and names; it cuts nothing by itself. The cut comes next, against its measured share.
## Final version
**Learn (changes nothing; Sonnet; ~0.3% of a week).** Add to milburn-usage.md, from data already in the repo: per chat, the start-up floor (step-1 context, ~90k where unstored, marked estimate, x later steps x read price), carried history, writes, output; and each chat's purpose from its title and the notes table (new work, note fix, handover). Result: Milburn's real dollars by block and by purpose, ranked. No list_events replay.

**Change 1 (this yes; Opus medium; ~1-1.5% of a week).** stepcost splits every step exactly by token origin from its usage: the step-1 context re-read (start-up floor, stored per chat), carried history (split by the call that wrote it, with Claude's own words and edits as kinds), new writes, output. It runs at every chat's end through the Stop hook. Its test, on the fixture transcript, fails unless the parts add to real cost within 1% and the leftover is under 5%. Number to beat: leftover under 5% on every chat of the next film (Milburn: 58-87%); three chats checked against the app's figure within 5%.

**Not in this yes.** The week size (estimates proposal); the ledger counting notes and repeats (Milburn review item 5); the cost cut, proposed next against the block the table ranks first, with its own number.
## For Sam
### Option 1: See where every dollar goes, then cut the biggest
The cost meter can't say what two thirds of each chat's money went on. We checked the app's real figures for Milburn: the money is right; the "% of a week" was off because the week's size is still a guess (that is fixed separately). This makes the meter split every step's cost into its real parts (the rules every chat re-reads, past work carried along, new writing, Claude's own words), with nothing left as "other". It runs by itself on every chat. You'd notice one short table of where Milburn's money went, then a cut aimed at the biggest part.
Lost: nothing in the films; about 1.5% of a week once.
Added: an exact cost split on every chat, and Milburn's answer now.
### Option 2: Label the leftover, learn from the next film
Add more labels to the meter's "other" pile and wait for the next film's numbers before deciding anything, without looking back at Milburn. Cheaper to think about, but a leftover pile stays and the answer comes a film later.
Lost: Milburn's answer now; a cut one film later.
Added: more labels on every chat from the next film.
