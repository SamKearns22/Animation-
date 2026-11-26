## Leak
Yes. The Facts line about "a second flat-colour copy of each frame (one colour per person, hand, prop)" proposes a remedy. It also turns out to exist already: handcheck draws each person a second time in key colours, one layer per sleeve and hand (source/handcheck.py, header; views.PROBE).

## Results
- Brexit Is Done: 62.76% of a week spent against a 52% estimate, over 37 chats, with 15 notes, 7 of them repeats (notes/ledger/brexit-is-done.md).
- 8 of the film's 26 note rows are about movement or contact over time: 13 (a pounce with no reaction), 14 (a fight not vigorous enough), 15 (guests popping out of a void), 19 (hands hovering over the armrests), 22 (a pounce too quick to read), 23.1 (moves comically large), 23.3 (the in-between frames of a gesture), 23.4 (runners swapping who is in front). Source: notes/brexit-is-done.md and notes/archive/brexit-is-done-notes.md, Notes tables.
- What should have caught those 8: for 19, 22 and 23.3, "none". For 23.1 a check existed (movesize) but had only a floor, set from a sheet and never from films Sam had passed. For 23.4 a check existed (cover) but merged the guests, never recorded the wolves, was never run on the film, and was skipped under Override. Same source.
- GTA animatic v5: 7 of 9 notes are drawing-order or passing-through faults in motion (2-6, 8, 9). Source: notes/sam-notes/gta-v5/notes.md.
- Picture critics already have a test bench scored against Sam's real notes. They caught 1-9 of 12 (Blessed) and 1-4 of 7 (Remakes), and the score swung from run to run (notes/critic-bench.tsv). The bench holds no motion notes from Brexit or GTA (source/bench/: Blessed and Remakes only).
- Gap: nobody has measured whether today's packs could catch any of those 8 motion notes. The record cannot yet say how much better seeing would help.
- The engine already holds the facts exactly: every person's plan depth, each hand's own layer, drawing order (handcheck.py, critique.people_boxes). ffmpeg and OpenCV 5.1 are installed (checked).

## The real decision
The tool to pick is not the decision. The decision is how the whole film's chain turns motion (things that only exist across frames) into something a check or a looker can judge, measured against Sam's own motion notes. Bigger levers than outside tools: (1) the engine's exact knowledge, which is unused for looking; (2) check limits set from films Sam passed; (3) checks that actually run on the film.

## Root cause
Every look is a sample. Stills and strips are taken at chosen moments, so faults that live between samples (the in-betweens in 23.3, the duration in 22, the order flip in 23.4, the pop-in in 15) are never in the picture. The motion facts the engine knows are turned into pass/fail numbers. Those numbers are tuned on test sheets, not on Sam's passed films (23.1), or tested only on kit paths and never on the film itself (23.4). Earlier fixes failed because they patched the number, not the looking. No seeing aid was ever scored on motion notes, so nobody knows which aid works.

## Approaches weighed
1. **Outside tools** (motion measuring, pose finders, a video model). Pose finders are trained on photos and are untested on flat drawings. The network blocked a download on 26 Nov. Motion measured from pixels only estimates what the engine already knows exactly. This is the wrong tool (Statement Two), so it is rejected unless step 1 shows a gap the engine cannot fill.
2. **Reframe: turn time into a still.** From the engine's own record, draw one picture per moving span: every drawing laid over the others faintly (onion skin), each hand's and head's path as a line with dots per drawing, and a lane strip showing who is in front of whom over time. Claude reads stills well. This makes the motion itself a still.
3. **Reframe: calibrate, don't look.** Set every motion check's limits from films Sam passed, and run it on the whole film every animatic.
4. **Learn first:** add Sam's saved motion notes to the critic bench, then measure today's pack against them.

Chosen: 4, then 2, then 3, each as its own step.

## Proposal
**Learn (changes nothing, Sonnet, about 1.5% of a week, unchecked).** Build bench cases from the 8 Brexit motion notes and GTA notes 2-6, 8 and 9, using the code as Sam saw it. Score today's critique pack on them. This gives the baseline: motion notes caught out of 15. Also record, for each note, whether the engine's own numbers already showed the fault.

**Change 1 (own yes, Opus high, about 2.5%, unchecked):** a shared motion sheet in critique.py and `final --span` (onion skin, path lines, lane strip), drawn from engine data, one per moving span. It goes in every critique pack and every motion clip, as one picture rather than more pictures. It gets its own kit test. Number to beat: it must catch at least 11 of the 15 motion cases on the bench, lose none of the Blessed and Remakes cases it already catches, and add no more than 2 false alarms per case. If it doesn't, it is not adopted.

**Change 2 (own yes, about 1.5%, unchecked):** every motion check's limits (move size, read time, cover order, gesture path) are measured from Blessed and the other films Sam passed. The bench cases become their kit tests. Number to beat: every saved motion note is caught, and none of the passed films is flagged.

Change 2 is enforced by the kit tests and the Checks line (rule 93: advice, never a lock), and Change 1 by its place in the critique pack. Each change comes out alone. Across later films the cost is about 0.2% of a week per film (unchecked), set against 15%.

Sam would notice: motion clips arrive with one "path picture", and there are fewer notes on movement.

## Sam test
Q1: Yes. An expert uses exact engine truth before guessing from pixels, and scores against real notes.
Q2: The evidence covers two films' motion notes and the existing bench, not one chat.
Q3: Root cause is shown (sampling, uncalibrated limits, checks not run). Results are measured on the bench. Enforcement is in code and the pack, not in a chat choosing to follow it.
Q4: Outside tools, turning time into a still, calibration and learn-first were all weighed.
Q5: Nothing is trusted before the bench result. Each change has its own yes and can be undone alone.
Q6: Facts carry their sources. Costs are unchecked.
Q7: Sized by the catch rate it must reach, not by price. The cheap trap (more stills) is rejected.
Q8: Permanent shared tools with kit tests, reviewed when Sam declares the film complete.

## Lost / Added
Lost: nothing. Outside tools are put off, not ruled out for good.
Added: 15 bench cases, one motion sheet per span, check limits from passed films. About 5.5% of a week once (unchecked).

## Unchecked
Costs. Whether a video model is available. Whether the engine records per-drawing joint positions for every kit (handcheck covers views.person only, not lying.draw).

done
