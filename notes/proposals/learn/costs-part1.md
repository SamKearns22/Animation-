# Costs part 1 (chats 0-16)

Source: get_session usage + last result texts (page 1 only). Chats 9-16: get_session returned 'not found', so no usage or replies; all unchecked.

| idx | chat id | stage | model | % week | usd | cache_read M | cache_write k | output k | history-end k | notes | repeats | renders | cause | evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2FapHZwZ | European protests satire film | opus | 0.2 | 0.485 | 0.65 | 31.2 | 5.3 | 89.7 | 0 | 0 | 0 | bookkeeping-handover | "saved your four-tier brief word for word as the notes" |
| 1 | WjJXBueP | Protest tiers: plan (chat 1 of 8) | opus | 1.53 | 3.752 | 6.62 | 201.0 | 41.0 | 199.4 | 5 | 0 | 0 | other | "Coming back to this chat after 4½ hours cost about 0.5% of your week" |
| 2 | CgYaSUFB | Protest Tiers: chat 2 of 8 (crowd research, sketches) | opus | 3.07 | 7.512 | 19.44 | 243.6 | 104.1 | 300.8 | 2 | 1 | 0 | research | "13 news photos covering every place (Al Jazeera, Reuters, AFP, AP and dpa)" |
| 3 | 17XjNRhV | Framing research: crowds, vistas, wide action (chat 2 of 8) | opus | 1.8 | 4.407 | 9.84 | 158.1 | 64.5 | 222.5 | 0 | 0 | 1 | research | "studied 16 big crowd, scenery and riot shots and marked up what each one does" |
| 4 | QkukuJUL | Framing research chat 3 of 8: lessons + re-staging | opus | 1.0 | 2.448 | 5.61 | 91.0 | 29.9 | 155.4 | 0 | 0 | 0 | other | "12 framing lessons are written as proposals ... four scenes are re-planned" |
| 5 | TWFKPUgZ | Protest Tiers pencil roughs (chat 4 of 8) | opus | 0.23 | 0.564 | 1.11 | 35.4 | 3.0 | 99.7 | 0 | 0 | 0 | other | "You've hit your 5-hour limit · resets 3:50am (UTC)" |
| 6 | xQrZzs91 | Pencil sketches for scenes | opus | 2.25 | 5.517 | 11.05 | 264.3 | 76.7 | 209.3 | 1 | 0 | 0 | unchecked | "1 is a yes, so the Frankfurt crowd stands on our side of the street" |
| 7 | rdxgcQf2 | auto | opus | 0.22 | 0.783 | 1.65 | 38.3 | 7.3 | 97.0 | 1 | 0 | 0 | bookkeeping-handover | "your answers are written into the film's notes and saved to GitHub" |
| 8 | bsyhavXp | auto | opus | 2.59 | 4.362 | 8.97 | 174.0 | 58.6 | 238.6 | 1 | 0 | 1 | new build | "The protests cast is built and drawn once, but I haven't sent it" |
| 9 | xQDM8iTN | Catch up | sonnet | 0.37 | n/a | n/a | n/a | n/a | n/a | ? | ? | ? | unchecked | session not found by get_session |
| 10 | 34R5mkDm | Protests cast chat 7 | opus | 1.87 | n/a | n/a | n/a | n/a | n/a | ? | ? | ? | unchecked | session not found by get_session |
| 11 | vy69nNwE | Protests cast chat 8 | opus | 2.45 | n/a | n/a | n/a | n/a | n/a | ? | ? | ? | unchecked | session not found by get_session |
| 12 | ybTh1KsF | Protests: sets (chat 9) | opus | 1.89 | n/a | n/a | n/a | n/a | n/a | ? | ? | ? | unchecked | session not found by get_session |
| 13 | PYcX2VRw | Protests chat 10: sets fixes, critique, sets sheet | opus | 1.3 | n/a | n/a | n/a | n/a | n/a | ? | ? | ? | unchecked | session not found by get_session |
| 14 | gWvGgNQ1 | Protest Tiers: chat 12 (truck, helicopter, then moves to ani | opus | 1.33 | n/a | n/a | n/a | n/a | n/a | ? | ? | ? | unchecked | session not found by get_session |
| 15 | vEV8PEFy | Protests chat 14: moves fixes, rehearsal clips, animatic 1 | opus | 3.22 | n/a | n/a | n/a | n/a | n/a | ? | ? | ? | unchecked | session not found by get_session |
| 16 | swHqHr7K | Night's work summary | sonnet | 0.33 | n/a | n/a | n/a | n/a | n/a | ? | ? | ? | unchecked | session not found by get_session |

Summary:
- Rows 0-8 measured: 7 of 9 were Opus high planning/research chats; the biggest spenders (2: $7.51, 6: $5.52, 3: $4.41, 8: $4.36) were research or build chats ending on a cost warning.
- Cache reads dominate (up to 19M tokens) because histories reached 200-300k; chat 1 notes a 0.5%-of-week reload after 4.5h idle.
- Chats 9-16 could not be read (not found), so their causes stay unchecked.
