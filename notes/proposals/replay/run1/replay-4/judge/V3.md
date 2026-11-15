## Leak
None.

## Root cause
Nothing records whether a rule or tool is used or helps, so a skip leaves no trace. Rules are graded only by the chat that wrote them.
- Use is not recorded: page.py is in the job pack (guides/job-packs.md:32). Chats 29 and 31 ran it 0 times and searched code by hand 25 and 26 times (tool-use-29-31.md). Nothing flagged it.
- Results are not recorded: the ledger says "0 rounds, 0 notes" over 32 chats (notes/ledger/protest-tiers.md), despite two rounds of notes (notes/protest-tiers.md). Notes count only when a chat types `--notes` (source/ledger.py:469). So CLAUDE.md's "caught nothing in three films" test cannot run.
- Self-report: the cost stops used chats' own costs, 20-75% low (sam-to-case4.md).
- 13 of 64 rules are checked "by hand" (guides/film-quality-rules.md).
- No independent grading: 8 faults in a "pillar" rule, found only when Sam asked.
- Chats 27, 30 and 31 are titled Opus but recorded as Sonnet (notes/ledger/app-costs.tsv). Nothing checks this.

## Approaches weighed
1. One-off audit: goes stale, and it is temporary (fails Q8).
2. Make every rule a blocking gate: forces use but never proves benefit; taste rules cannot be gated.
3. Red-team each rule on paper: finds flaws in the wording, not what chats do.
4. Trace each of Sam's notes to the rule that missed it: finds holes, not dead weight.
5. **Chosen:** a permanent automatic register built from the chat records. It feeds approaches 2 and 4 with evidence.

## Proposal
**What:** one register entry per rule and tool, with three signatures read from each chat record:
- Arose: the situation came up.
- Used: it was followed (page.py ran).
- Bypass: it was skipped (grep or sed on a film file).

Check FAULT lines and Sam's notes are logged against the rule they belong to.

**Enforced by:**
- The existing Stop hook (`ledger.py auto`) scores every chat from its record, not its claims, at no chat cost.
- Notes come from `handover.py log`'s saved messages, not `--notes`.
- `handover.py end` flags each "arose, not used" rule as a fault, fixed or named before handover.

At film completion, a fresh Sonnet helper applies a fixed table:
- Used under 95% of the times it arose: gate it or rewrite it.
- Missed a note: improve that check first.
- Nothing caught in three films and nothing missed: a removal proposal with "Lost:".

**Shown first:** the signatures must reproduce chats 29 and 31's known counts before Sam's Y.

**Number to beat:**
- Use where the rule arose: at least 95%.
- Notes per round and repeated notes: falling against a baseline from Protest Tiers and two earlier films.

**Cost:**
- About 8-12% of a week, once: build, about 180 signatures, review and backfill.
- Then about 0% per chat and about 1% per film. Unchecked.

**Sam notices:** a scorecard at each film's end, skipped rules caught before his notes, fewer repeated notes, and removals as Y/N with evidence.

## Sam test
- Q1: the expert method: judge agents by their tool records and outcomes.
- Q2: every chat of every film, with a baseline across several films.
- Q3: the hook runs without anyone reading; bypass is counted; results are measured.
- Q4: five different approaches were weighed, and this one powers two of the others.
- Q5: it only flags; nothing is removed without Sam's Y; it is proven on chats 29 and 31 first; one line removes it.
- Q6: sources are named; the rest is marked unchecked.
- Q7: sized to make the removal and fix rules work.
- Q8: permanent, reviewed at each film's completion.

## Lost / Added
- Lost: nothing.
- Added: the register, the scoring hook, "skipped" handover faults, and the scorecard.

## Unchecked
- The tool count.
- How many past records can still be read (the message log has 11 files for 32 chats).
- Whether chats 27, 30 and 31 ran on Sonnet.
- All costs.
