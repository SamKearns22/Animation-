## Leak
yes: the title gives the remedy ("measure what each new chat costs ... and set chat size from it"), and the facts lead with a fitted best size near 138 steps, which anchors toward longer chats. It also carries a stale fact that steers the same way: it calls chat-size-and-model "open, not yet decided by Sam", but Sam said Y on 17 Nov (notes/proposals/chat-size-and-model/sam.md); and the cost-watch limits are 250k/370k (.claude/hooks/costwatch.py line 28), not 200k/300k.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 2 | 4 | 3 | 4 | 16 |
| V2 | 4 | 3 | 4 | 4 | 4 | 19 |
| V3 | 2 | 2 | 3 | 2 | 4 | 13 |
## Sam test
Q1: Yes, with the fixes: an expert measures the start, and the re-learning a handover causes, step by step, before re-tuning a rule set on mixed fitted totals; and does not reopen a rule Sam settled two days ago on a flat curve.
Q2: Every chat of every film from now on, measured automatically and checked against the app's real figures (app-costs.tsv), which is wider and truer than the 47 estimated chats; the Milburn transcripts are gone, so nothing better exists for the past.
Q3: The end-of-chat hook writes the figures, so no chat chooses to; root cause shown (the start is never stored and nothing marks first real work). Paper-compliance gap: a wrong "first real work" marker would make the figures look fine; the test fixture now checks it. Worked = the film-end line exists and matches the app within reason.
Q4: Four approaches weighed (learn first, a warm handover, hand over by sum, leave size and work on steps per film); the base-load lever from V1 is routed to the adopted startup-reading job instead of a second fix.
Q5: Learning changes no film. No change rides on this yes: any later change (a required read list in handovers, a different chat size) comes back to Sam through the route with its numbers. The 17 Nov rule stays. Each field can be removed alone.
Q6: Checked: Milburn 22.0% app / 32.4% estimate; the bins and fits; test transcript 45k at step 1, 78k by step 2, about $0.41 (0.17% of a week); near-empty app chats $0.12-0.56 (0.05-0.23%); Sam's 17 Nov Y; limits 250k/370k. Unchecked and named: whether one tool-job transcript stands for film chats; why estimates run 1.47 times the app.
Q7: Sized by the decision: it measures the part (re-learning) that could actually change the answer, not a cheap one-off guess at the start; honest build cost 0.5-1% of a week once.
Q8: Permanent ledger fields, no trial; read at each film's end review when Sam calls the film complete.
## Pick
V2
## Why
V2 is the only version that checked the record well enough to find that Sam already decided chat size on 17 Nov and that the curve is flat from 70 to 130+ steps (about 1.4% of a week a film at most), so it does not reopen a settled rule on noisy fits. It measured a real start directly (0.17% of a week, a third to a quarter of the fits' fixed term) and named the part that is truly unknown and could matter: the steps a new chat spends re-learning what the last chat knew. V1 is well checked and its arithmetic is right (83k x 1,281 steps x $0.18/M is about 7.8% of a week), but its "8% lever" is mostly the app's own instructions and tools, which the adopted startup-reading job (16 Nov) already measured (~25% of a median chat) and handles; a second base-cutting change risks blocked chats and overlaps. V3 rests on the stale "still open" fact, prejudges the answer (120-140 steps) from the leak, and would reopen Sam's rule. Taken from V1: the base-share figure and the check against the app's real costs, with any base finding sent to startup-reading rather than a new fix.
## Faults in the pick
- F1 [fixed] "Cost of reading files the previous chat also read" cannot be computed at the next chat's end, because the earlier transcript is gone by then; each row now stores the files it read and their sizes, so the comparison works.
- F2 [fixed] V2's change 1 (a required read list) would be built on this yes once a number is crossed; now it returns to Sam through the route with its figures, so one yes covers only the measuring.
- F3 [fixed] Figures were estimates only, known to run about 1.47 times high; each film-end line is now checked against the app's real per-chat cost.
- F4 [fixed] V1's base-load share added, routed to the startup-reading job, not a second fix.
- F5 [named] The only direct start measurement is one tool-job chat; film chats may differ until the next film's figures arrive.
- F6 [named] "First real work" is a rule of thumb (first edit or write outside notes, or first render); some chats may start differently.
## Final version
**Learn (changes no film).** The end-of-chat hook (ledger.py auto, through stepcost) adds to every chat's ledger row:
1. Context at step 1.
2. Steps and % of a week up to first real work: the first edit or write outside notes/, or the first render or check on film files.
3. The files read before first real work, with their sizes; at the next chat's end, the cost of re-reading files the film's previous chat also read (re-learning).
4. Base share: step-1 context x steps x re-read price, as % of the chat.
The existing test transcript gets checks for 1-4 (including the first-real-work marker). Build cost about 0.5-1% of a week once, Opus medium; nothing per film after.

**Read at each film's end review**, one line for Sam: "a new chat's start and re-learning cost X% of the film", checked against the app's real per-chat costs (app-costs.tsv).

**Decisions it feeds, each its own proposal through the route, none built on this yes:**
- If start plus re-learning averages over 0.5% a chat: propose a warm handover (the handover names the exact files, line ranges and pictures the next stage needs; the handover check refuses one without them). Number to beat: start cost per chat halved, Sam's notes and repeat faults no higher than the last two films.
- If base share is large: the figures go to the startup-reading job, which owns start-up reading.
- Only if the measured starts put the lowest-cost size outside 70-150 steps does chat size go back to Sam. Otherwise the 17 Nov rule (about 100 steps, up to 150 to finish a stage, the 40-step floor with its two exceptions, warnings at 250k/370k) stands, and Sam gets that one standing answer.

Lost: nothing. Added: four start-up figures on every chat's record; one film-end line.
## For Sam
### Option 1: Measure the start, keep your 17 Nov chat-size rule
Every chat, when it ends, now records on its own how much it cost to get going and how much it spent re-reading what the chat before it already knew. You get one line at each film's end saying what new chats cost that film, checked against your app's real figures. Your chat-size answer from 17 Nov stays as it is; it only comes back to you if the real numbers say it is wrong. If the start turns out costly, a fix (handovers that list exactly what the next chat must read) comes to you as its own question.
Lost: nothing.
Added: four figures per chat on its cost record; one line at film end; about 0.5-1% of a week once to build.
### Option 2: Measure the start and cut what every step carries
The same measuring, plus going after the fixed load every step re-reads (the app's own instructions, tools and our rule files), which adds up to about 8% of a week a film. Bigger in theory, but most of that load is the app's own and cannot be cut by us, and the part we can cut is already being trimmed by the start-up reading job you approved on 16 Nov; removing tools could leave a chat stuck without one it needs.
Lost: possibly tools or connectors a chat sometimes uses.
Added: the same figures, plus cuts to start-up loading, one at a time.
