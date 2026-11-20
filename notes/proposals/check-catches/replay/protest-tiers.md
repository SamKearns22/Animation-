# Check replay: protest-tiers (today's checks on each chat branch; check-catches Learn)

31 branches, 31 ran (0 refused or broken); pre-flight time 718 s in all, 23 s a run. "Caught" = a fault gone by the next chat; "let through" = still there at the last chat and not named in the notes' Exceptions.
False alarms and "Sam's notes it should have caught" are filled by the replay chat from the film's notes table; "?" = could not tell (the bar: a sourced answer for 80% of check-film pairs).

| check | runs | faults | caught | let through | named | could not test | false alarms | Sam's notes missed |
|---|---|---|---|---|---|---|---|---|
| AUDIT | 8 | 62 | 51 | 18 | 0 | 0 | ? | ? |
| AUDIT (time-stamped jumps/pass-through/swaps) | 6 | 171 | 156 | 39 | 0 | 0 | ? | ? |
| CAMERA FEEL | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| EFFECT SHAPES | 8 | 6 | 7 | 1 | 0 | 0 | ? | ? |
| EXCEPTIONS | 2 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| READABILITY | 3 | 2 | 1 | 1 | 0 | 0 | ? | ? |
| benchmark | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| caption | 6 | 1 | 0 | 1 | 0 | 0 | ? | ? |
| clipcheck | 1 | 1 | 1 | 0 | 0 | 1 | ? | ? |
| house style | 1 | 3 | 3 | 0 | 0 | 0 | ? | ? |
| no | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| no record of the composition sheet being | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| the brief checklist has 30 blank | 3 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| the brief checklist has 4 blank | 4 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| the brief checklist has 8 blank | 4 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| the film hazes a layer but its draw_orde | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |

## What the Protest Tiers replay says (plain)
- The tool's own table came out EMPTY for this film: it wrongly marked all 31 chats "refused" (a word in the checks' normal output trips its refusal test), and it split the many time-stamped jump/pass-through lines into one "check" per timestamp. The table above was rebuilt from the saved run in a scratch copy, grouping those lines as one audit check; the tool itself is unchanged (it goes to Sam as a fix).
- 11 of the 31 chats (the early ones) could not run: that chat's film file did not exist yet ("No module protest_tiers"), so the early chats have no result.
- "Caught" counts per fault line, so it can read higher than "faults" (a fault that reappears is counted each time); read it as "mostly gone by the next chat", not as an exact number.
- Sam's notes for this film are mostly in notes/archive/protest-tiers-reporting.md and the handovers, not in a table; only note 1 (the phone held behind the head) is in the film's own table, and which check should have caught it is not sourced. False alarms and notes missed are therefore "?" for every row: sourced answers under 10%, far below the 80% bar.

## Re-made by the fixed tool (job 4 chat 5, 20 Nov; check-catches change 3)
The tool now scores a run that lists faults even when its output says "refuses" (only a crash with no fault lines is broken), groups all time-stamped audit lines as ONE check (AUDIT) and counts in a check's name as '#', compares a run stopped at a gate only on the checks it listed, and counts each fault once (caught + let through can no longer pass faults). The hand-made table above is kept as chat 4 left it.

31 branches, 21 ran (10 refused or broken); pre-flight time 718 s in all, 34 s a run. "Caught" = a fault gone by the next chat; "let through" = still there at the last chat and not named in the notes' Exceptions.
False alarms and "Sam's notes it should have caught" are filled by the replay chat from the film's notes table; "?" = could not tell (the bar: a sourced answer for 80% of check-film pairs).

| check | runs | faults | caught | let through | named | could not test | false alarms | Sam's notes missed |
|---|---|---|---|---|---|---|---|---|
| AUDIT | 8 | 233 | 176 | 57 | 0 | 0 | ? | ? |
| CAMERA FEEL | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| EFFECT SHAPES | 8 | 6 | 5 | 1 | 0 | 0 | ? | ? |
| EXCEPTIONS | 2 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| READABILITY | 3 | 2 | 1 | 1 | 0 | 0 | ? | ? |
| benchmark | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| caption | 6 | 1 | 0 | 1 | 0 | 0 | ? | ? |
| clipcheck | 1 | 1 | 1 | 0 | 0 | 1 | ? | ? |
| house style | 1 | 3 | 3 | 0 | 0 | 0 | ? | ? |
| no Rehearsal clips sent | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| no record of the composition sheet being | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |
| the brief checklist has # blank | 11 | 3 | 3 | 0 | 0 | 0 | ? | ? |
| the film hazes a layer but its draw_orde | 1 | 1 | 1 | 0 | 0 | 0 | ? | ? |

## Refused or broken (today's pre-flight would not run on this chat's files)
- claude/protest-tiers-c2 (a070d491): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-roughs-c4 (4922f4a5): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-c5 (bac8d049): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-c6 (1d82d59d): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-c7 (e1dedec3): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-sets-c9 (e02b6c34): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-c8 (0bb53b6e): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-sets-c10 (93aabe98): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-sets-c11 (ef34b1b6): ModuleNotFoundError: No module named 'protest_tiers'
- claude/protest-tiers-c12 (a625cf2b): ModuleNotFoundError: No module named 'protest_tiers'
