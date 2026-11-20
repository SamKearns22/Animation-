# Check replay: milburn (today's checks on each chat branch; check-catches Learn)

6 branches, 3 ran (3 refused or broken); pre-flight time 18 s in all, 6 s a run. "Caught" = a fault gone by the next chat; "let through" = still there at the last chat and not named in the notes' Exceptions.
False alarms and "Sam's notes it should have caught" are filled by the replay chat from the film's notes table; "?" = could not tell (the bar: a sourced answer for 80% of check-film pairs).

| check | runs | faults | caught | let through | named | could not test | false alarms | Sam's notes missed |
|---|---|---|---|---|---|---|---|---|
| CAMERA FEEL | 3 | 1 | 0 | 1 | 0 | 0 | 0 (film gives no camera to read) | 1: note 5 (reverse framing poor); the check could not read this film's camera |
| EFFECT SHAPES | 3 | 1 | 0 | 1 | 0 | 0 | 0 (film has no effects list) | 0 sourced |
| READABILITY | 3 | 1 | 0 | 1 | 0 | 0 | 0 (film has no props list) | ? |
| SHOT CAST | 3 | 21 | 0 | 21 | 0 | 0 | 21 (all: it says the NEETs are never on screen in 2a; notes 3 and 6 show goth and Swindon seen in 2a, 2b, 3; it cannot read this film's cast list) | 0 |
| caption | 3 | 9 | 2 | 7 | 0 | 0 | ? | 0 sourced |
| clipcheck | 3 | 1 | 0 | 1 | 0 | 3 | 0 (could not test) | 0 sourced |
| house style | 3 | 4 | 0 | 4 | 0 | 0 | 0 (film has no lists for these) | 0 sourced |
| plan | 3 | 15 | 0 | 15 | 0 | 0 | ? | 0 sourced |
| script/mouth | 3 | 48 | 1 | 47 | 0 | 0 | ? | ?: note 6 (no mouth on Swindon); the branch with the fix would not run, so cannot tell |
| the collision and pop-in tests did not r | 3 | 1 | 0 | 1 | 0 | 0 | 0 (film has no scene list) | 0 sourced |

## Refused or broken (today's pre-flight would not run on this chat's files)
- claude/milburn-c2 (72b55c9b):  - HEAD LIFE: milburn speaks (line ?) with no head acting (rule 74: HEAD_LIFE['milburn'] = headlife.HeadLife from the voice, used in the drawing)
- claude/milburn-chat3 (c11a832b): KeyError: 'size' (crashed in plan.py)
- claude/milburn-chat8-swindon-mouth (7c8fbead):  - HEAD LIFE: pat speaks (line ?) with no head acting (rule 74: HEAD_LIFE['pat'] = headlife.HeadLife from the voice, used in the drawing)

## What the Milburn replay says (plain)
- Most "faults" are the check saying the film has no list it needs (cameras, effects, props, cast). The film was built before these lists were required, so they are format gaps, not mistakes in the picture. They tell us nothing about what a check would have caught.
- Real catches: 3 (two caption speed faults and one script/subtitle fault were gone by a later chat). Real misses against Sam's notes: 1 sourced (note 5, framing; the camera check could not read the film). Notes 1-4, 7, 8, 9, 10, 11 are looks and taste or acting: no check owns them.
- 3 of 6 chats would not run today's pre-flight (two on a missing head-acting line, one on a crash), so those rows are "could not test". Sourced answers: 13 of 18 cells (72%), under the 80% bar.
- Sam's notes sourced from notes/archive/milburn.md (the film's notes were archived when it posted).

## Re-made by the fixed tool (job 4 chat 5, 20 Nov; check-catches change 3)
The tool now scores a run that lists faults even when its output says "refuses" (only a crash with no fault lines is broken), groups all time-stamped audit lines as ONE check (AUDIT) and counts in a check's name as '#', compares a run stopped at a gate only on the checks it listed, and counts each fault once (caught + let through can no longer pass faults). The hand-made table above is kept as chat 4 left it.

6 branches, 5 ran (1 refused or broken); pre-flight time 21 s in all, 4 s a run. "Caught" = a fault gone by the next chat; "let through" = still there at the last chat and not named in the notes' Exceptions.
False alarms and "Sam's notes it should have caught" are filled by the replay chat from the film's notes table; "?" = could not tell (the bar: a sourced answer for 80% of check-film pairs).

| check | runs | faults | caught | let through | named | could not test | false alarms | Sam's notes missed |
|---|---|---|---|---|---|---|---|---|
| # shot | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| CAMERA FEEL | 3 | 1 | 0 | 1 | 0 | 0 | ? | ? |
| EFFECT SHAPES | 3 | 1 | 0 | 1 | 0 | 0 | ? | ? |
| HEAD LIFE | 2 | 3 | 3 | 0 | 0 | 0 | ? | ? |
| READABILITY | 3 | 1 | 0 | 1 | 0 | 0 | ? | ? |
| SHOT CAST | 3 | 21 | 0 | 21 | 0 | 0 | ? | ? |
| caption | 3 | 9 | 2 | 7 | 0 | 0 | ? | ? |
| clipcheck | 3 | 1 | 0 | 1 | 0 | 3 | ? | ? |
| house style | 3 | 4 | 0 | 4 | 0 | 0 | ? | ? |
| plan | 3 | 15 | 0 | 15 | 0 | 0 | ? | ? |
| poses | 2 | 13 | 13 | 0 | 0 | 0 | ? | ? |
| script/mouth | 3 | 48 | 1 | 47 | 0 | 0 | ? | ? |
| the collision and pop-in tests did not r | 3 | 1 | 0 | 1 | 0 | 0 | ? | ? |

## Refused or broken (today's pre-flight would not run on this chat's files)
- claude/milburn-chat3 (c11a832b): KeyError: 'size' (crashed in plan.py)
