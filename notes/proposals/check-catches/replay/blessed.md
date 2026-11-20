# Check replay: blessed (today's checks on each chat branch; check-catches Learn)

20 branches, 20 ran (0 refused or broken); pre-flight time 371 s in all, 18 s a run. "Caught" = a fault gone by the next chat; "let through" = still there at the last chat and not named in the notes' Exceptions.
False alarms and "Sam's notes it should have caught" are filled by the replay chat from the film's notes table; "?" = could not tell (the bar: a sourced answer for 80% of check-film pairs).

| check | runs | faults | caught | let through | named | could not test | false alarms | Sam's notes missed |
|---|---|---|---|---|---|---|---|---|
| EXCEPTIONS | 13 | 4 | 4 | 1 | 0 | 0 | ? | ? |
| HEAD LIFE | 3 | 2 | 2 | 0 | 0 | 0 | ? | ? |
| no | 3 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| no record of the composition sheet being | 3 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| poses | 20 | 15 | 14 | 1 | 0 | 0 | ? | ? |
| the brief checklist has 17 blank | 3 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| the notes file has no | 1 | 1 | 0 | 1 | 0 | 0 | ? | ? |

## What the Blessed replay says (plain)
- 20 chats, all ran (the checks here are few: poses, head life, the notes/brief upkeep lines). Rebuilt in a scratch copy because the tool's own table calls every chat "refused"; the tool is unchanged.
- Nearly everything listed is notes upkeep ("brief checklist has blank rows", "no record of ...") and the pose-looked-at line: all gone by a later chat, i.e. they push the chat to do its housekeeping, they do not look at the picture.
- Sam's notes (e.g. 39, the van sitting pose "still horrible", a repeat) are about how a pose looks; no check here judges that, so those are misses by design. Only two of the film's notes are in the archived table I read, so false alarms and misses stay "?": sourced answers well under the 80% bar.

## Re-made by the fixed tool (job 4 chat 5, 20 Nov; check-catches change 3)
The tool now scores a run that lists faults even when its output says "refuses" (only a crash with no fault lines is broken), groups all time-stamped audit lines as ONE check (AUDIT) and counts in a check's name as '#', compares a run stopped at a gate only on the checks it listed, and counts each fault once (caught + let through can no longer pass faults). The hand-made table above is kept as chat 4 left it.

20 branches, 20 ran (0 refused or broken); pre-flight time 371 s in all, 18 s a run. "Caught" = a fault gone by the next chat; "let through" = still there at the last chat and not named in the notes' Exceptions.
False alarms and "Sam's notes it should have caught" are filled by the replay chat from the film's notes table; "?" = could not tell (the bar: a sourced answer for 80% of check-film pairs).

| check | runs | faults | caught | let through | named | could not test | false alarms | Sam's notes missed |
|---|---|---|---|---|---|---|---|---|
| EXCEPTIONS | 13 | 4 | 3 | 1 | 0 | 0 | ? | ? |
| HEAD LIFE | 3 | 2 | 0 | 2 | 0 | 0 | ? | ? |
| no Rehearsal clips sent | 3 | 1 | 0 | 1 | 0 | 0 | ? | ? |
| no record of the composition sheet being | 3 | 1 | 0 | 1 | 0 | 0 | ? | ? |
| poses | 20 | 15 | 14 | 1 | 0 | 0 | ? | ? |
| the brief checklist has # blank | 3 | 1 | 0 | 1 | 0 | 0 | ? | ? |
| the notes file has no | 1 | 1 | 0 | 1 | 0 | 0 | ? | ? |
