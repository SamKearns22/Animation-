# Startup reading: the learn table (chat 2, Sonnet, 16 Nov; read-only, nothing changed)

**Coverage (read first).** 5 of the 9 readable Protest Tiers chats (0, 1, 4, 5, 7), read from their start with
`list_events`; chat 4 only in part (first steps). Not reached: chats 2, 3, 6, 8 (long, 4-6 pages each). Protest Tiers 9-32:
cannot be opened. Elder Swindon: no readable chat (only its final-post chat exists). So the table is a **sample of 5
chats, not the two films**; it is enough to rank, not to promise exact savings. Tokens = characters / 2.35
(job-e-measurements.md). Money: Opus, a 1k-token piece read at the start costs ~$0.006 to write plus 78 actions x $0.00022
to re-read = **$0.023 per chat**; x32 chats = $0.74 a film; 1% of a week = $2.45 (Facts of the proposal).

## What every chat starts with (measured: usage on each chat's first step)
| chat | tokens in before its first step | after 8 steps | growth |
|---|---|---|---|
| 0 | 79,352 | (7 steps) ~88.7k | +9.4k |
| 1 | 79,780 | 91,329 | +11.5k |
| 4 | 80,192 | not read | |
| 5 | 80,596 | 88,224 | +7.6k |
| 7 | 78,749 | 88,866 | +10.1k |

So **~79.5k is in before any work, and ~9.7k more by the 8th step.** Of the 79.5k: CLAUDE.md ~5.5k (12,857 chars), the
chat's starting message 0.5-2k, the rest **~72k is the app's own** (tool list, system prompt, hook text): the largest item
by far, not ours to shorten.

## Ranked: what the repo controls, tokens per chat and cost per film (32 chats)
| rank | source | tokens per chat (measured) | $ a film | % of a week a film | what a fix must beat |
|---|---|---|---|---|---|
| 1 | CLAUDE.md (loaded by the app) | 5,470 (counted) | 4.03 | 1.6% | 5.5k tokens, no rule sentence lost |
| 2 | Film notes read at start (slices by `sed`/`grep`; chat 1 the whole file) | 2.7k, 2.8k, 4.0k, 4.9k = **3.6k mean** | 2.65 | 1.1% | 3.6k per chat |
| 3 | Branch listing / branch checks | 1.2k, 1.0k, 1.2k, 3.9k, ~2.6k (chat 4, estimated from the listing) = **2.0k mean** | 1.47 | 0.6% | 2.0k per chat |
| 4 | Guide sections (read by a Plan chat only: chat 1: 7.2k; the others 0) | 1.8k mean over the sample (planning chats only) | 1.3 | 0.5% (planning chats only) | not a start-up cost: work reading |
| 5 | Pack (`job-packs.md`) | 0.84k, 1.0k, 0, 0 = **0.5k mean** | 0.34 | 0.14% | 0.5k per chat |
| 6 | `handover.py` and hook printouts | ~0.03k (58 characters seen) | ~0 | ~0 | nothing to win |
| ref | App's own (tool list, system prompt) | ~72k | ~53 | ~22% | cannot be changed from here |

Repo-controlled start-up in all: **~5.5k + ~8k = ~13.5k tokens a chat, ~$0.31 a chat, ~$10 a film, ~4% of a week.**

## What this changes in the verdict's picture
1. **The notes are not read whole.** The verdict assumed ~10-13k tokens of notes in every chat. Measured: the chats read
   notes in slices (headings, "Where things stand"), 2.7-4.9k tokens; only the planning chat read the whole file (4.0k at
   9.4k characters when it was short). A cap check on notes length (change 1) would save a fraction of 3.6k, not 10-13k.
   A tool that **prints just "Where things stand" and the open notes** would save about 2.5k a chat (**~0.7% a film**).
2. **The branch listing is already trimmed by the chats** (`head -30/-40`, filters); the full listing (~2.6k) appeared in
   one of five. Expected saving of a "branches with new work only" step: **~1.5-2k a chat, ~0.5% a film**; the safe,
   cheapest, zero-rule-risk change.
3. **CLAUDE.md is the largest repo item** (1.6% a film). Getting to 3.5k tokens saves 2k a chat, **~0.6% a film**; it
   carries the rule-loss risk, so it stays last and guarded.
4. **Change 4 (pack printout) fails its own condition:** chats read 0-1k of the pack; none read beyond it at start.
   **Drop it.**
5. **Nothing to win in** `handover.py` / hook output.
6. The honest ceiling for all repo-side fixes together: **~1.8% of a week a film** (0.7 + 0.5 + 0.6), against ~53% for a
   film. That is worth doing cheaply, but it is not where the big money is (chat length and the app's own 72k are the
   bigger levers; both are other jobs, Sam 16 Nov).

## The film-total mismatch (33.55% vs 53.6%), settled
`notes/ledger/protest-tiers.md` line 64 ("33.55% ... 0.5x") is **text stored once** by `ledger.py` when the film was
closed (commit 5398a94c, 15 Nov, in the same commit as the chats table) and **never recomputed**. The chats table in the
same ledger adds to **53.56%** (`ledger.totals` returns 53.56 today): 47.33 from the app's real figures, 6.23 estimated
for 4 chats not yet read. **53.6% is right**; the 33.55% line is stale. Consequence: the "0.5x of the last two films"
comparison is wrong too; it is 53.56 against their 65.8 average = **0.8x**. (Fix would be a recompute in `ledger.py`,
a separate small change; not made here.)

## For chat 3 (Opus high): the top fixes, in order, each its own yes
1. Branch step by tool (cheap, no rule risk): ~0.5% a film.
2. Start check prints the notes' "Where things stand" and open notes only (replaces the notes cap as change 1): ~0.7%.
3. CLAUDE.md layered (guards: every-rule-sentence check, ten-situations test): ~0.6%.
4. Dropped: pack printout. Optional small: recompute the ledger's stored compare line.

Gaps named: sample of 5 chats; chat 4 partly; branch count is from chat 4's listing (125 branches then, 252 now, so
today's full listing would cost ~2.5k+); money is derived, not billed.
