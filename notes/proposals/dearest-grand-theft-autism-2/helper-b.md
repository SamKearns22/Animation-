# Helper B: Claude's own thinking and code writing (grand-theft-autism)

## Leak
None. The problem file states the problem and points at records; it proposes no remedy.

## Results
- The film has cost 54.67% of a week over 28 chats, 25 of them on Opus. It was estimated at 53.2% and is forecast to land at 69.7%, against an aim of 15%. Round 1 is not finished. (ledger .md and .json)
- "Claude's words" as a source of cost comes to 23.55% when I add it up from the rows (dearest.py says 22.3%; the gap is how older rows are named). Of that, 14.05% is the price of writing it. About 9.5% is paying to re-read Claude's own earlier output at every later step of the same chat. (.json "blocks" against "origins")
- It takes the same share of long chats (110+ steps, 41.9%) as of short ones (41.3%). Chat length is therefore not what drives it. (.json)
- Chats 1-10 (first build) cost 18.98%, of which 7.77% was words. Chats 11-28 cost 35.69%, of which 15.79% was words. Chats 11-28 were mostly shot 4 being rebuilt. The rebuilt versions were v3 to v7 plus animatic v3, and the "sausage arm" came back for the fourth time. (.json; notes/grand-theft-autism.md "Animatic v3"; shot 4 case study §2)
- Thinking and code within the named rows, by my own sums: thinking 42-58% of Claude's writing, code 29-40% (grand-theft-autism 7a739e72; check-repairs 906480b5 and 335c535e). The problem file's figures (39-48% and 32-38%) are close but I could not reproduce them exactly.
- Notes-round chats ran on Opus high. CLAUDE.md says Opus medium for those. In the film notes and the case study, "Opus high" appears 9 times and "Opus medium" once.
- Gaps in the record: every row shows stage "auto" and 0 notes, yet Sam gave notes many times. So the ledger cannot yet say how much went on first builds, how much on rework after a fault Sam saw, or how much depended on effort level.

## The real decision
The question is not how to make Claude write less. It is why this film paid for its writing about twice over. The unit that matters is the whole film. Two levers are bigger than "thinking": rework (attempts redone after Sam found faults the checks missed) and effort settings that ignore the stage rules.

## Root cause
Claude's words are paid once per attempt. Two-thirds of them fell in chats 11-28, which mostly rebuilt drawings Sam had already rejected. The same faults came back more than once (backs, arms, the crowd; rule 30 is named for each). Each rebuild re-thinks the problem and re-writes the code from cold, on Opus high. Earlier fixes failed because they patched the frame. For example, chat 24 moved the camera only for the firing, and the faults stayed in the crash hold and the climb back (notes, F7). The checks that would have stopped an attempt before it was written were built only after Sam's notes (case study §6).

## Approaches weighed
1. **Reframe: fewer attempts.** Catch the drawing fault before the code that animates it is written, so each shot is thought and coded about once.
2. **Learn first: record where the words go.** Give each ledger row its stage, its effort level, whether it was a first build or rework, and Sam's note count. Then let the numbers pick the change.
3. **Match effort to the stage.** Enforce Opus medium for note rounds at the moment a chat is opened, as CLAUDE.md already says.
4. **Carry less.** Shorter chats or summaries to cut the 9.5% spent re-reading Claude's own output. This is the weakest lever, because length showed no effect on the share.

Chosen: 2, then one change picked by its result, most likely 1. Rework is where most of the money went and where Sam's notes come from. Approach 3 risks quality without evidence that it is safe.

## Proposal
**Learn (changes nothing): about 0.5-1% of a week, one Opus-medium chat.**
- Re-tag this film's 28 rows from its chat records and notes: stage, effort, first build or rework, and which shot.
- From then on, have the ledger write these four fields on every row by itself (from the handover check and the chat-opening step), so the record never again reads "auto, 0 notes".
- Report: how much of Claude's words went on rework, and how much at high effort on note rounds.

**Then one change, chosen by that report:**
- If rework is half or more of Claude's words, the change is a **pre-code gate**. Before any moves code for a shot, one still per beat is drawn and must pass the seeing checks (body, back-view, crowd, held object). It is enforced by the handover check, which refuses a handover whose moves code has no passed stills.
  - Number to beat: the next film's share of Claude's words spent on rework. This film's figure, from the learn step, is the baseline. It must also show fewer repeated notes (rule 30) than this film's count.
- Only if the report shows high effort on note rounds costing more than rework does a separate change go to Sam. That change would set effort when the chat is opened, and it would need its own test on one round's faults.
- Each change is reviewed against the film's results when Sam calls the film complete.

**Honest size:** even halving Claude's words saves about 12% of a week. That would not bring this film near 15% on its own. Start-up reading (11.9%) and the number of chats count too.

**What Sam would notice:** fewer versions of the same shot coming back with old faults, and one extra still-sheet stage per shot, which the checks see and Sam does not.

## Sam test
- Q1 Expert: an expert measures where the work goes before tuning thinking. Effort and caching come second to rework.
- Q2 Best result: the scope is the whole film's 28 chats plus the named rows of the second record (check-repairs), not one chat.
- Q3 Comprehensive: the gate is enforced by the handover check, not by a chat choosing to follow it. Success is measured as a share of rework.
- Q4 Most intelligent: four different approaches weighed. Rework is the largest of them.
- Q5 Risk: the learn step changes nothing. The gate can be removed on its own if it adds cost without cutting rework.
- Q6 Checked: sources named. Items I could not check are listed below.
- Q7 Not the cheap version: it does not cut effort or thinking blindly. The gate costs a stage and buys fewer rebuilds.
- Q8 Nothing temporary: the ledger fields and the gate are permanent, and are reviewed at the film's end.

## Lost / Added
- Added: four ledger fields per chat, filled in automatically; a still-sheet gate before moves code (only if the learn step supports it).
- Lost: nothing from the film. A build stage can no longer go straight to moves code.

## Unchecked
- Which chats worked on shot 4: inferred from chat numbers in the notes, not from tags in the ledger.
- The exact 39-48% and 32-38% figures in the problem file.
- Whether earlier thinking is carried forward in later steps (it affects the 9.5% re-read share).
- All costs are estimated from the chat records ("est"), not the app's own figures.
