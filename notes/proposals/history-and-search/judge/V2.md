## Leak
No solution is stated, but the framing leans toward enforcing page.py ("anything a chat must remember fails").

## Results
- Re-reading history is 49% of Opus chat cost. Chats over 200k: 26 of 36, costing $158 of $176 (notes/cost-diagnosis.md Job A).
- Every step pays the full re-read: 4.7c at 215k. The app's ~80k, re-read on every step, is ~25% of a chat. Most steps add under 2k (cost-diagnosis Job B).
- Hand code searches: 169 of 564 steps (30%) in 7 chats, with 0 page.py runs. That includes the build chat after page.py existed (PT cast chat 5: 18 of 58) (notes/proposals/learn/code-search-count.md). Chats 29 and 31: 25 and 26 searches, 0 runs (notes/proposal-route.md; unchecked here).
- page.py is named only for notes rounds, and only for film files (guides/job-packs.md, rule 61). It does not cover shared tools (source/page.py `files()`).
- Gaps in the record:
  - Searching's share of COST.
  - How searches split between film files and shared tools.
  - Whether `show` holds what a note needs (never used).
  - Chats 9-32 cannot be read.

## The real decision
A film costs roughly steps × history, summed over all its chats. The decision: cut steps that do no film work in every Opus chat (build chats too, not only notes rounds), without relying on memory. Chat count (33) and rework (~30% of Protest Tiers) are bigger levers, but they are separate decisions.

## Root cause
Grep, Read and sed are always in a chat's hands. page.py reaches a chat only as text, and only in one pack. Nothing at the tool boundary checks which one is used. Second cause: `show` is unproven. A chat forced to use a tool that misses will run `show` and then grep anyway.

## Approaches weighed
1. **Gate:** a hook refuses hand searches on film files until `show` has run, and prints the command.
2. **Reframe, fewer steps of every kind:** measure per-step cost by kind from transcripts, then cut the dearest kinds.
3. **Reframe, lower history ceiling** (150k): each fresh chat pays ~80k plus start-up reading, and chat count is already high. Judge it only once the cost curve is measured.
4. **Finder helper chat:** each one starts at roughly ten `show` steps' cost. Rejected.
5. **Learn first:** measure the cost share and where searches point; replay `show`.

Chosen: 5, then 1. Approach 2 is folded into the measuring.

## Proposal
**Learn (read-only, Sonnet, ~1% of a week)**, from the readable chats' events, written to notes/proposals/learn/search-cost.md:
- (a) Searching's share of each chat's per-step cost.
- (b) The search targets: film files, shared tools or kits.
- (c) `show` replayed on every note those chats fixed: do its lines hold the lines the chat finally edited?
- (d) What fills the ~80k start.

**Change 1 (its own Y, ~1%): the gate.** A PreToolUse hook (.claude/settings.json) covers Grep, Read and grep/sed/awk/head on source/FILM*.py.
- Before `show` for that file: refuse, and print `python3 source/page.py FILM show "…"`.
- After `show`: allow ranged reads of up to ~80 lines.
- Edits and new files are never blocked.
- It logs refusals, `show` runs and allowed reads to each chat's ledger row (ledger.py auto), automatically, on either account.
- Prerequisite: `show` hits at least 80% in the replay. If not, `show` is fixed first, as its own change.
- To beat: hand searches under 10% of steps (now 30%), and Opus cost per note below the 7-chat baseline.

**Change 2 (its own Y), only if (b) shows a third or more of searches are on shared tools:** extend page.py and the gate to tools.

**Cost:** ~2-3% once. Estimated saving: 10-15% per Opus chat, ~3-6% per film (unchecked until (a)).

**Sam notices:** cheaper rounds and a per-chat ledger line. Films are the same.

## Sam test
- Q1: Enforce at the tool boundary; measure before forcing a tool.
- Q2: Every readable chat, by kind. The cost gap is measured first.
- Q3: A refusal does the enforcing, not text. Complying on paper (`show`, then greps) shows up in the log.
- Q4: Five different approaches, two of them reframes.
- Q5: Gating waits until the replay proves `show` works. Undoing it is one hook line.
- Q6: Sourced; estimates marked unchecked.
- Q7: Sized to the measured 30%. The cheap version (a pack line) already failed.
- Q8: Permanent. Reviewed when Sam calls the film complete.

## Lost / Added
- Lost: grepping film code before running `show`.
- Added: one hook, a replay, and three counts per ledger row.

## Unchecked
- Searching's share of cost.
- The 3-6% saving.
- How searches split between film files and tools.
- Chats 29 and 31.
- Whether a refusal reliably redirects the chat.
