# What searching costs a round chat (history-and-search Learn, backfill; chat 7, Sonnet, 16 Nov)

Read-only. Nothing built. **Short answer: gate 2 fails (the code finder `show` hit 50-69%, gate is 80%), so the guard stops. Gate 1 (searching >= 10% of a round chat) probably passes but is estimated, not measured.**

## What could and could not be measured (read first)
- The chat history (`list_events`) does carry each step's usage (checked on Blessed animatic render: every reply has cache read/write and output tokens). But a page of it can only be read in the chat, not fed to a script. One page of 25 assistant lines was ~12k tokens of reading; a 100-step chat is 40+ pages. All 24 readable chats would cost more than the whole backfill is worth, so **no chat was measured step by step**.
- **Measured:** `stepcost.py` on the one real transcript kept in `tests/` (a tool job, 16 steps): 12 of 16 steps were searches, they cost 18.4% (the measure charges a call what it added plus re-reading it at every later step). So a search step costs about a quarter of its step share, at 16 steps.
- **Counted earlier (code-search-count.md):** 7 round chats, 169 of 564 steps (30%) were hand searches, 0 `page.py` runs.
- **Estimated here:** the cost share, from those two (see (a)). Marked estimated everywhere it is used.
- Protest Tiers chats 9-32 (sessions 01Gzna...) cannot be opened; not counted.
- Protest Tiers chats 0-8 are planning, research and sketch chats (no code-fix notes), so searching in them is unmeasured and (e) has nothing to replay there.

## (a) Searching's share of each chat's cost
Step share is counted. Cost share = step share x 0.25 to 1.0, **estimated**: 0.25 is the one measured chat (short, 16 steps); 1.0 is the long-chat limit, where a result is re-read at every later step (a 1,000-1,500-token result re-read ~50 times is about as much as one step's own history read, so 34 searches in a 100-step chat is ~17-33% of its cost). Round chats are long, so the middle of the range is the better guess.

| Blessed (film chats) | % of week | steps | hand searches | step share | est. cost share |
|---|---|---|---|---|---|
| round 2 notes | 2.40 | 102 | 34 | 33% | 8-33% |
| round 2 chat 2 | 2.28 | 97 | 32 | 33% | 8-33% |
| Walliams' face, chat 3 | 2.73 | 86 | 14 | 16% | 4-16% |
| journalists' arms | 3.36 | 132 | 47 | 36% | 9-36% |
| press re-placed | 1.09 | 50 | 10 | 20% | 5-20% |
| fix Brand's arm | 0.86 | 39 | 14 | 36% | 9-36% |
| **Blessed, 6 chats** | 12.72 | 506 | 151 | 30% | **7-30%** |

| Protest Tiers | % of week | steps | hand searches | step share | est. cost share |
|---|---|---|---|---|---|
| cast chat 5 (after `page.py` existed) | 2.59 | 58 | 18 | 31% | 8-31% |
| chats 0-8 others (plan, research, sketches) | 10.4 | not counted | not counted | unchecked | unchecked |

**Totals (7 counted chats, 15.31% of a week):** 169 of 564 steps = 30%; cost-weighted step share 29.5%; estimated cost share **7-30%**. **Gate 1 number: searching ~7-30% of a round chat, middle ~15% (estimated; gate >= 10%).** Not proven: the low end is under the gate.

## (b) Search targets (unchecked as a split)
Only the film's-own-file part is known: the counts above are searches on `source/blessed*.py` / `protest_tiers*.py` plus a few on shared tools (`moves.py`, `checks`, kit files). The exact split of film files / shared tools / kits needs the step-by-step read that was not done, so it is unchecked. The earlier plan's "extend the finder to shared tools" decision therefore has no number yet. Sizes that matter: Blessed code is 410k characters in 8 files (~100k tokens); the biggest are `blessed.py` 117k chars, `blessed_sets.py` 95k, `blessed_cast.py` 68k.

## (c) Whole-file .py reads and their size
Not counted per chat (unchecked): the 7 earlier chats show 0 whole-file reads in the counting rule (hand search = a Read of a .py), but the file did not separate whole from ranged. What one would cost: `blessed.py` ~29k tokens, `blessed_sets.py` ~24k, `blessed_cast.py` ~17k, `protest_tiers.py` ~30k, `protest_tiers_sets.py` ~26k; written once, then re-read every later step, so one whole read of `blessed.py` at step 20 of 100 is ~29k x (12.5 + 80) read-units, about as much as 25-30 normal searches. Whether chats did this is unchecked.

## (d) What fills the ~80k start (partly measured)
- Observed: the Sonnet animatic-render chat for Blessed (a tiny job, 0.19%) sat at **~100k tokens** of history at its last reply, so ~95k+ is start, before any work.
- Known sizes: CLAUDE.md 12.9k chars (~3.2k tokens); film-quality rules 38.5k chars (~9.6k tokens, read only when named); a film's notes 25k chars (~6k); the film's page 25-45k chars (~6-11k); job packs 4.6k chars (~1.1k).
- So the repo's own reading is ~10-25k tokens. **The rest (~60-80k) is the app's own: system instructions, tool descriptions, the skill and agent lists, MCP instructions.** Unchecked as a split; not something a repo change can cut except by fewer tools/skills listed.

## (e) `page.py FILM show "note words"` replayed on fixed notes
Method: Blessed notes 1-46 (archive/blessed-notes-animatics-1-2.md): for the 26 whose fix names a piece of code, `show` was run on Sam's exact note words (current code) and a hit means its ~40 lines contain what the fix names. **The real "lines finally edited" are not kept** (git history starts 15 Nov), so the fix's own words are the stand-in. Two scores:
- **Loose** (any code word the fix names, e.g. `camera`, `chair`): **18 of 26 hit = 69%.**
- **Strict** (only distinctive names: HEAD_K, chin_long, ears_hidden, press_spots, cot_top, LINES, G2_PART, music, gates2, checks): **7 of 14 hit = 50%.**
- Hits (strict): notes 1, 12, 19, 27, 32, 38, 45. Misses: 2 (chin_long: lives in a TUNE table), 9 (ears_hidden: show gave `_turned_long`, 10 lines from the real line), 18 (cot_top was new code), 30, 31 (gates2 not in the note's words), 35 (the word "shall" is inside the LINES table), 37 (dock: `show` gave `_stills`, `dock` only as a runner-up).
- Pattern: it points at the right area but misses (1) values in tables/constants, (2) a setting inside a function, (3) notes that name the shot, not the thing, (4) code that did not exist yet. These can be fixed in `show` (rank tables and shot names; show lines holding a note's words inside the head function).
- Protest Tiers: nothing to replay (chats 0-8 fixed no notes).

## The two gate numbers
1. **Searching's share of a round chat: ~15% (range 7-30%, estimated). Gate >= 10%: probably passes, not proven.**
2. **`show` hit rate: 50% strict, 69% loose. Gate >= 80%: FAILS** (and would at either score).
Result: the guard stops. Per the plan, `show` is fixed first, as its own change. Because gate 2 fails either way, gate 1's uncertainty does not change the decision.

## Unchecked
Per-chat cost by kind from the history; targets split (b); whole-vs-ranged reads (c); the start split inside the app's share (d); Protest Tiers 9-32; replay against the lines finally edited.
