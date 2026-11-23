# Helper A: staging notes that take several rounds

## Leak
The file name ("staging-stills") and the lesson it points to (milburn-review.md line 51: "draw two small stills") give away a solution. Ignored.

## Results
- The reverse was built three times:
  - chat 6, with no board;
  - chat 10, chat 9's staggered re-stage;
  - chat 11, after Sam asked for "equal and centred, same depth 2.2 m, camera up 1.2 like Milburn's".
  Source: milburn-handovers.md lines 63, 91, 101; milburn.md line 7.
- Note 5 was vague: "the scene composition in scene 4 as proposed is poor" (milburn.md line 233). Nobody asked what "poor" meant. Chat 9 decided "two equal busts, dead centre" was the fault. Sam then asked for roughly that.
- The brief already said "the 180 of shot 1" (milburn.md line 165). Chat 9's diagnosis went against it.
- The board for these shots (rule 11) was put off in chats 6, 7, 9 and 10. It reached Sam only in chat 12, after all three builds (milburn.md lines 9, 240, 246).
- Rule 87 already says: a note that can be read two ways is asked first, and a fix that fails twice sends 2-3 options on one still. It is checked by hand (rulebook line 88), and neither happened.
- Note 5 fell in Sam's night run: "Save any Y or N questions until the end" (milburn.md line 244). That pushed chats to guess.
- Cost (ledger, the app's figures): chat 6 2.84%, chat 9 3.74%, chat 10 3.24%, chat 11 2.73%. These are not the problem file's figures. How much of each was staging: unchecked. Repeats: 1 of the film's 4 (milburn-review.md line 7).
- Gap: no record counts staging notes, or whether each reached Sam as a picture before it was built.

## The real decision
How every staging choice, first or redone, reaches Sam as a picture he can pick from before it is built, in every chat, attended or not. The bigger levers are the board's timing (rule 11) and forcing rule 87's "ask first". A new kind of still is not.

## Root cause
1. The board check runs only before the animatic. It only asks whether a shot was ever on some board (rough.py `board_gate`, lines 668-704). So shots are built and clipped before any board, and a re-stage never needs a new one.
2. A vague taste note was fixed from the chat's own idea of good composition, not checked against the brief or Sam's words. Rule 87 is by hand, and the night run's "save questions" overrode it.

## Approaches weighed
1. **Two stills by hand per staging note** (lesson 3). Relies on a chat choosing to do it; rule 87 already asks for this and was skipped.
2. **Reframe: enforce the board at the build.**
   - Each shot's camera and seats are recorded when its board is sent.
   - A shot changed since its last delivered board gets no move render and no clip until a new board reaches Sam.
   - A re-stage after Sam's note shows 2-3 numbered framings and waits for his number; other work goes on.
3. **Learn first:** measure staging notes on the last four films. Read Sam's chat 7 and chat 11 words (earlier chats can be read).
4. **Taste record:** Sam's staging picks go into the checklist's "Taste, never a fault" list.

Chosen: 3, then 2. Approach 4 waits for its own evidence.

## Proposal
- **Learn (changes nothing, about 0.4% of a week):** go through Milburn, Blessed, Protest Tiers and Patriots 4. For each staging note, record:
  - whether a board was delivered before the build;
  - whether it was a repeat;
  - how many builds it took;
  - its share of the cost.

  Also read Sam's chat 7 and 11 words, to say whether an options board would have caught note 5.
- **Change (only if 2 or more staging repeats were built before a board):** approach 2, inside the existing board tool, refused by the tool itself. A test replays Milburn's record and must refuse chat 6's and chat 10's builds. About 0.7% once, and about 0.15% per re-stage board, against 15% per film.
- **Numbers to beat, counted at film end from the board record and rule 30's repeat marks:**
  - staging repeats per film: 1 now, target 0;
  - staging builds before a board: 2 now, target 0.
- **Sam would notice:** before a re-staged shot moves, one still with numbered framings to pick from.

## Sam test
- Q1: an expert forces the existing step where building starts, rather than adding a new one.
- Q2: the evidence is four films, gathered before any change.
- Q3: the tool refuses, and a replay of Milburn proves it.
- Q4: four different approaches were weighed.
- Q5: one change, which can be undone alone, tried on the real record first.
- Q6: sources named, gaps marked unchecked.
- Q7: sized to stop repeats, not to be the cheapest.
- Q8: permanent, reviewed at film end.

## Lost / Added
- Lost: re-staged clips before Sam picks a framing.
- Added: a board per re-stage, a gate at the build, one measured table.

## Unchecked
- The staging share of each chat's cost.
- Sam's exact chat 7 and 11 words.
- Other films' staging repeats.
- Why the problem file's costs differ from the ledger.
