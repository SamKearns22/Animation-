# Code search by hand vs the code finder (page.py)

**Method.** For each of the seven chats I read its own main-thread tool steps from the session record (assistant events, newest page first, paging back to the start; helper steps skipped, none appeared). A "page.py run" is a Bash command naming page.py. A "hand search" is a Grep call, a Read of a source/*.py file, or a Bash command that greps, awks, `sed -n`s, heads or tails a .py file or the source folder, or loads a source module with `python3 -c`. Edit scripts, renders, git, notes and guide lookups do not count. Most pages were scored by a script; four short pages that came back inline were counted by hand with the same rules. The scripted rule can over-count by a step or two per chat (a command that mixes an edit with a search). Cost is the ledger's "% of a week" from chat-list-blessed.tsv / chat-list.tsv.

| Chat | Date | Cost % | Total steps | page.py runs | Hand searches | Share |
|---|---|---|---|---|---|---|
| Blessed round 2 notes | 12 Nov | 2.40 | 102 | 0 | 34 | 33% |
| Blessed round 2 chat 2 | 12 Nov | 2.28 | 97 | 0 | 32 | 33% |
| Blessed Walliams' face chat 3 | 12 Nov | 2.73 | 86 | 0 | 14 | 16% |
| Blessed journalists' arms | 13 Nov | 3.36 | 132 | 0 | 47 | 36% |
| Blessed press re-placed | 13 Nov | 1.09 | 50 | 0 | 10 | 20% |
| Blessed fix Brand's arm | 13 Nov | 0.86 | 39 | 0 | 14 | 36% |
| Protest Tiers cast chat 5 (after page.py existed) | 14 Nov | 2.59 | 58 | 0 | 18 | 31% |
| **Total** | | **15.31** | **564** | **0** | **169** | **30%** |

Chats 29 and 31 of Protest Tiers (on another account) are not counted here (unchecked); notes/proposal-route.md records them as 0 page.py runs and 25 / 26 hand searches.

## Findings
1. Across these seven chats, 169 of 564 steps (30%) were hand code searches, and the code finder was run 0 times.
2. The 14 Nov evening Protest Tiers chat came after page.py was built and still searched by hand 18 times and ran it 0 times, which matches chats 29 and 31 (0 runs, 25 and 26 hand searches).
3. Each chat's share was 16% to 36% of its STEPS (a step's cost varies with history size, so the share of the 15.31% of a week is unchecked). The finder goes unused unless something forces it.

Dates (checked by chat 4): page.py was built overnight 14 Nov (its own header: ranking item 6, overnight chat 3; the Blessed cleanup chat ran its size test 14 Nov 21:00). The six Blessed chats (12-13 Nov) predate it, so they are the baseline cost of hand searching, not a failure to use it. The git history here starts at a 15 Nov merge, which is why git shows 15 Nov. Protest Tiers cast chat 5 (14 Nov 20:56) and chats 29 and 31 (15 Nov) came after it and ran it 0 times.

Caveat: page.py was committed on 15 Nov (git date), so the 12 to 14 Nov chats could not have run the committed version; chat 7 is still the only one after the 14 Nov build the brief names. Shares are approximate (see method).
