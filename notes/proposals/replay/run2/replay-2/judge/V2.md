# Helper A: what to measure next

## Leak
None as a solution. The wording does lean one way: "which chats, how many" assumes the answer is more step-by-step bills of single chats.

## Results
- **Real metered usage per chat already exists** for 66 chats (`notes/ledger/app-costs.tsv`: dollars, cache reads, cache writes, output, final history size). Protest Tiers: 29 chats, $115.94, 285M tokens re-read, 5.55M written, 1.23M output.
- **On one price base, Protest Tiers is not cheaper.** In app dollars: Blessed $100.79 (24 chats), Remakes $88.11 (19), Protest Tiers $115.94 and still running (32 chats) (ledger .json files). The "80%" and "51%" in the problem file and the ledger's "After the film" lines use the old $171 week. Today's $245 base (`costwatch.py`, marked PROVISIONAL) gives 62% / 36% / 51%. The Protest Tiers "33.55%, 0.5x" line is stale; the ledger header says 51.27%.
- **A chat that does almost nothing still costs about 90–100k tokens of context.** Examples: "European protests" 90k history with 5k output, "session 23 handover" 100k with 2k output (app-costs.tsv). `costwatch.py` assumes FRESH = 90,000. Every step re-reads this base. With the fitted prices, re-reads come to about $51, writes about $44 and output about $31 (my arithmetic, ±20%). If you set aside a chat's own work, much of the re-read and write cost is this fixed base repeated across 32 chats.
- **Overruns cluster in a few stages** (protest-tiers.md): moves cost 11.3% against 3.07% planned, round 1 moves 14.0% against 4.45%, and unplanned plan extras 10.1%. Those three are 35% of the 51%.
- **The bills for chats 29 and 31 are estimates.** They are keyword-classified and weighted by call count, by the helper's own account (bills-29-31.md). Counting calls cannot see the fixed base.
- **Gaps in the record:** the notes column is 0 for every film, so Sam's notes per stage are not recorded and "fewer notes" cannot be measured. The model column contradicts the titles (chats 27, 30 and 31 say sonnet while titled Opus; chat 19 says opus while titled Sonnet).

## The real decision
The question is where a whole film's dollars go: fixed start-up per chat, the work itself, or rework. The answer has to sit on one price base, film against film. Two levers are bigger than "which chat's steps to count": how many chats a film uses multiplied by the fixed context each one carries, and the rework in the moves stages.

## Root cause
The step bills measure the wrong unit. A step's price is mostly the context it re-reads, and most of that context is the same 90–100k start-up load in every chat. That makes the cost roughly chats × base × steps, plus rework. Counting calls by kind (the bills) spreads that fixed cost across "ls/grep" and "checks" and hides it. The cross-film comparison Sam was given also mixed two price bases, which is why the "new systems are cheaper" message flipped.

## Approaches weighed
1. **More step bills** (the problem's frame): bill 5–10 more chats, about 1–2% of a week. They are still estimates, still blind to the base, and the decisions would stay the same. Rejected.
2. **Reframe to the whole film, metered:** build one token table per film from data already held, on one base, split into start-up base, work and rework by stage. Measure once what fills the 90–100k (system prompt, tool lists, CLAUDE.md, hook output, handover reads). Chosen.
3. **Rework first (learn-first):** read the moves and round-1-moves chats to find why they ran about 3x over plan. Kept as step 2.
4. **Change now:** cut start-up context or merge chats straight away. Rejected for now: the size of each share is not measured yet, and Q5 calls for evidence first.

## Proposal
**Learn first. These change nothing:**
1. **Whole-film table,** about 0.4% of a week. Re-price all three films on today's base from app-costs.tsv. For each stage, show: number of chats, base tokens (chats × start-up size), work tokens, dollars, and planned against spent. One page in `notes/ledger/`, with a plain three-bar version for Sam: start-up, work, rework.
2. **Start-up autopsy,** about 0.3%. Use one fresh chat's own token records to list what fills its first context and each item's size.
3. **Moves rework,** about 0.5%. Read the two dearest moves-stage chats in full (chat 14 at $7.90, chat 29 at $6.29). For each rebuild, record its cause: a missed check, an unclear brief, or a note from Sam.

Total about 1.2% of a week, against 15% per film.

**Changes after, one at a time, each only if the table shows its share is large:**
- **(a) Shrink start-up context.** Number to beat: the 90–100k base per chat.
- **(b) Fewer, longer chats per stage, up to the amber limit.** Number to beat: 32 chats.
- **(c) Fix the cause of moves rework.** Number to beat: moves spend of 25.3% against 7.5% planned.
- **(d) Fix the ledger record,** with notes and model columns filled from real data. Number to beat: the columns are currently empty or wrong.

Each change is enforced by code or a hook, not by a chat choosing to follow it. Each is measured automatically by `ledger.py` from the app's figures (rule 85) on the next film, against that film's dollars on the same base.

**What Sam would notice:** one honest page on where the money went, then single Y/N offers, each carrying its own number.

## Sam test
- Q1 (Expert): An expert measures tokens by source before cutting steps, and that is what this does.
- Q2 (Best result): It covers all three films and every chat, using metered figures.
- Q3 (Comprehensive): It finds the root cause, the base context. Results come from the app's own figures, not a chat's word.
- Q4 (Most intelligent): Four different approaches were weighed. The reframe wins.
- Q5 (Risk): Learning changes nothing, and each later change can be undone alone.
- Q6 (Checked): Sources are named, and estimates are marked.
- Q7 (Not the cheap version): It is sized to answer the whole-film question. Further step bills would be cheap but blind.
- Q8 (Nothing temporary): The table becomes a permanent ledger page, and changes are permanent or not made at all.

## Lost / Added
- **Lost:** further keyword step bills.
- **Added:** one whole-film table, one start-up autopsy and one rework read.

## Unchecked
- The fitted prices (costwatch.py says ±20%).
- That FRESH really is 90k for every chat (inferred from near-idle chats).
- The provisional $245 week.
- Which model each chat actually ran on.
- The dollars for the 3 chats estimated rather than read from the app.
