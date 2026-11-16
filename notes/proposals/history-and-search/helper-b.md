# Helper B: history re-reads and hand code searches

## Leak
None. page.py is named as background, not as the answer.

## Results
- Re-reading history is 49% of an Opus chat's cost. 26 of 36 chats at 200k+ cost $158 of $176 (cost-diagnosis.md, Job A).
- A median chat is ~78 steps ending ~220k, about $5.6. Checked: ~78 steps × ~150k average history is 11.7M tokens, about $2.6 (Job B).
- 169 of 564 steps (30%) were hand searches; page.py ran 0 times (code-search-count.md). Only one readable chat came after page.py existed. Chats 29 and 31: unchecked.
- **The count mixes two things.** A "hand search" includes reads of any source/*.py, but page.py covers only source/FILM*.py (page.py `files()`). How much searching was in shared tools: unchecked.
- Searching's share of cost, as opposed to steps: unchecked. The ledger stores cost per chat but not steps, history or step types (protest-tiers.json fields). **Nothing records use, so every count so far was done by hand, afterwards.**
- Whether `show` finds the right lines: never measured.
- Film level: Protest Tiers took 33 chats, 53.6% against ~20%; critique, rework and re-render chats were 16.0% (protest-tiers-costs.md).

## The real decision
A film's re-read bill is chats × steps × average history. Step count and rework chats are bigger levers than searching. Searching is the cause of step count that can be measured and forced first.

## Root cause
Tools reach a chat only as text: a pack line or a handover print is read once and then lost under the default habit of grep and sed. Nothing acts at the moment of the search, and nothing records whether the tool was used. Naming page.py in the pack failed for exactly this reason.

## Approaches weighed
1. **Enforce at the step:** a hook that runs before each step refuses hand searches on film files until `page.py show` has run.
2. **Reframe, shorter histories:** hand over at ~150k. This costs more chat starts (~$0.5 each) and more context lost between chats; unmeasured.
3. **Reframe, searching off the main chat:** a helper finds the code and returns only the lines. Each helper pays its own start-up.
4. **Learn first:** the Stop hook records each chat's steps, history and cost by kind of step; then `show` is replayed against past notes.

**Chosen: 4, then 1, separately.** Only 1 does not rely on a chat remembering; 4 shows whether it is worth it and safe. 2 and 3 wait for 4's numbers.

## Proposal
**Learn (permanent; nothing Sam sees):**
- `ledger.py auto` (already the Stop hook) adds to each chat's row: steps, history at the end, and cost by kind of step (film-file search, tool search, page.py, renders, pictures, other). Each step is charged its own re-read plus what it added times the steps after it.
- A one-off replay of `show` on Blessed and Protest Tiers 0-8 notes: did it return the lines the chat later edited?
- Cost: ~1-1.5% of a week.

**Change 1 (only if film-file searching is above ~10% of a round chat's cost and the replay hits at least 80%):**
- `source/codegate.py`, a hook that runs before each step. Until `show` or `find` has run in the chat, it refuses Grep, Read and grep/sed/awk/head on source/FILM*.py, and prints the ready command.
- Afterwards, reads of the lines `show` named pass. Tools and notes are never blocked. On its own error it lets the step through.
- Number to beat: film-file search cost per round chat at a third of the baseline, with Sam's notes and repeat notes per round no higher.
- Build ~1%.

**Later, each separately:** page.py over shared tools if the split shows tool searching is large; the handover line (approach 2) set by the history numbers.

**Estimate (unchecked):** searching is about 15% of an Opus chat's cost. Cutting two-thirds of that on ~27 Opus chats saves ~4% of a week per film, against ~2.5% spent once.

**Sam notices:** cheaper chats, and each film's review shows where the money went.

## Sam test
- Q1: measure, then enforce at the tool call.
- Q2: every chat recorded automatically, not seven by hand.
- Q3: refused in every chat; the ledger proves it.
- Q4: four approaches weighed.
- Q5: learning changes no film; the gate fails open and one line undoes it.
- Q6: sources named; gaps unchecked.
- Q7: fixes the cause, not another reminder.
- Q8: permanent; reviewed at the film's end.

## Lost / Added
- Lost: free greps on film files before `show` (change 1).
- Added: ledger fields, one before-step hook, one replay.

## Unchecked
- The cost share of searching.
- How searching splits between film files and tools.
- Whether `show` finds the right lines.
- Chats 9-32.
- What makes up the app's own 80k.
