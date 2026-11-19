# Milburn: real usage per chat (get_session, 19 Nov; job 4). 13 of 15 chats; 5c55685c and ce8f146c not found.

Session usage is the app's own count (cache re-read, cache write, fresh input, output tokens, cost_usd). A session's
usage can include turns after its ledger row (e.g. chat 13 was resumed later). Shares use costwatch.py prices.

| chat | ledger % | model | re-read M | write k | output k | $ app | $ ledger@245 | re-read | write | output |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 a58b9d21 | 1.62 | opus | 10.9 | 145 | 41 | 4.16 | 3.97 | 47% | 28% | 25% |
| 2 a6692140 | 2.8 | opus | 16.3 | 257 | 89 | 6.65 | 6.86 | 41% | 28% | 31% |
| 3 866dad74 | 3.08 | opus | 24.3 | 300 | 70 | 7.75 | 7.55 | 51% | 28% | 21% |
| 4 e33e3e79 | 1.2 | opus | 7.9 | 106 | 35 | 3.13 | 2.94 | 44% | 26% | 27% |
| 5 10232ef9 | 3.54 | opus | 26.8 | 251 | 83 | 8.85 | 8.67 | 52% | 22% | 23% |
| 6 3fbce046 | 2.64 | opus | 17.8 | 202 | 88 | 6.95 | 6.47 | 46% | 23% | 31% |
| 7 4ee174a9 | 2.42 | opus | 11.3 | 302 | 59 | 5.86 | 5.93 | 34% | 41% | 25% |
| 9 d2dd63d4 | 4.02 | opus | 21.6 | 476 | 92 | 9.16 | 9.85 | 39% | 38% | 23% |
| 10 ba98bbef | 3.15 | opus | 23.5 | 293 | 84 | 7.94 | 7.72 | 49% | 27% | 24% |
| 11 5b682f67 | 2.7 | opus | 20.1 | 245 | 62 | 6.68 | 6.62 | 51% | 28% | 22% |
| 12 b54e8334 | 0.34 | sonnet | 5.0 | 134 | 13 | 1.17 | 0.83 | 41% | 43% | 16% |
| 13 d34bde53 | 2.29 | sonnet* | 18.8 | 346 | 80 | 5.51 | 5.61 | 42% | 31% | 27% |
| hashtag a3a53ca2 | 0.34 | sonnet | 2.9 | 99 | 11 | 0.79 | 0.83 | 34% | 47% | 19% |

Totals (13 chats): app $74.59; ledger estimate at $245/week $73.84. By token type: re-read 45%, write 30%, output (Claude's words, thinking and tool-call text) 25%, fresh input 1%.
The ledger's per-chat estimates match the app's dollars within a few % (sum $73.84 vs $74.59). So the gap to Sam's meter
(32.4% estimated vs 22.0% on his app) is the dollars-to-%-of-a-week conversion (WEEK_USD 245, marked provisional), not
the per-step estimate. If Milburn's ~$79 real spend is 22% of a week, a week is about $361, not $245.

## Where Milburn's money went, by block (cost-other Learn, job 4 chat 3, 19 Nov)
From the table above and the ledger's step counts (12 chats with both). Start-up floor = the step-1 context re-read at
every later step: ~90k tokens x (steps - 1) x read price, an ESTIMATE (step-1 size was not stored for Milburn; the new
meter stores it from now on). Carried history = the rest of the re-read. New writes = everything put in the cache once
(tool results, Claude's own earlier words, reminders; not split here: the transcripts are gone). Claude's words =
output (text, thinking, tool-call text). Purpose per chat is not in the record beyond the chat titles.

| chat | title | steps | start-up floor | carried history | new writes | Claude's words | $ app |
|---|---|---|---|---|---|---|---|
| 1 | screenplay | 68 | 26% | 21% | 28% | 25% | 4.16 |
| 2 | | 92 | 20% | 20% | 28% | 31% | 6.65 |
| 3 | moves | 130 | 25% | 27% | 28% | 21% | 7.75 |
| 4 | | 59 | 30% | 15% | 27% | 28% | 3.13 |
| 5 | | 136 | 25% | 30% | 23% | 23% | 8.85 |
| 6 | | 92 | 21% | 25% | 23% | 31% | 6.95 |
| 7 | | 71 | 19% | 15% | 41% | 25% | 5.86 |
| 9 | | 98 | 16% | 23% | 38% | 23% | 9.16 |
| 10 | | 123 | 23% | 26% | 27% | 24% | 7.94 |
| 11 | animatic update | 122 | 28% | 23% | 27% | 22% | 6.68 |
| 12 | | 40 | 29% | 12% | 44% | 16% | 1.17 |
| 13 | | 117 | 23% | 19% | 31% | 27% | 5.51 |
| all 12 | | | 23% ($17.29) | 23% ($17.58) | 30% ($22.54) | 25% ($18.97) | 73.81 |

Ranked: new writes 30%, Claude's words 25%, carried history 23%, start-up floor 23%. No one block dominates; the
biggest (new writes) is what each step brings in, which the new meter splits by origin (which tool, Claude's own
edits, reminders) on every chat from now on. The cut is proposed against whichever origin ranks first on the next film.
