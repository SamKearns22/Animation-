# Helper A: the five rules written twice in CLAUDE.md

## Leak
The title gives the answer ("Merge"); set aside. The Facts also carry the startup-fixes guard (10-situation test) as given.

## Results
- Saving: the overlapping words in the five pairs are ~300 characters, ~130 tokens (my count of CLAUDE.md today; ratio from learn.md). At learn.md row 1 (5,470 tokens = 1.6% of a week a film) that is **~0.04% of a week a film**. Closes ~0.13k of the 0.2k miss on the 4.8k beat (handover.md).
- Drift inside CLAUDE.md: none found. When Sam changed these rules, all copies changed in one commit (e.g. 0cb979ae, 12 Nov, his note 5). Faults reaching Sam from one copy being stale: **none in the record** (problem file also: unchecked).
- Drift elsewhere, found: the rulebook's last table still says the first line is "Nothing needed" (row 99), dropped from CLAUDE.md on 9 Nov (389cc56f); and "P17" names two different rules (rows 99 and 104).
- Two "duplicates" fixed a case the general wording missed: a 1 Nov plan said "the animatic needs no sign-off" (flying-whales-handovers.md line 274); Sam then added "Every animatic carries..." (3 Nov, in 06e62819). "Every chat starts with the project selected" (9 Nov) was followed on 12 Nov by the create_session wording (51846b42; cause inferred from its title).
- No check guards any of the five (grep of handover.py, propose.py).

## The real decision
Not "save tokens" (0.04% a film), but: can each pair become one sentence that keeps every case it names, proven by a test, with a guard that makes the next rewording safe too? The bigger lever (catching a twin when it is written) is outside "Only do Half A": named, not proposed.

## Root cause
Sam's answers are added as sentences where the chat was working. Nothing checks for an existing twin when a rule is written; "Each rule is written once" (line 58) relies on a chat choosing to look. Some twins were also deliberate: the specific copy fixed a case the general one missed.

## Approaches weighed
1. **Merge each pair into one sentence holding both cases**, guarded by the 10-situation test and a per-pair allowance in the sentence check.
2. **Reframe: a write-time twin check** (any new CLAUDE.md sentence close to an existing one is flagged). Stops the cause; a separate proposal.
3. **Pointers, not merges:** keep the specific copy, cut the general to "see X". Saves less, same guard.
4. **Learn first, keep both** where the history shows the second copy fixed a failure of the first.
Chosen: 1, with 4's history built into it: the specific words ("animatic", "source_url", "wait for my numbers") are kept in the merged sentence, never folded into a general one.

## Proposal
**Learn first (changes nothing):** a Sonnet chat builds the 10-situation test: two real past situations per pair (e.g. note 5, Sam asked to type a prompt; the 1 Nov animatic without sign-off), each with Sam's known right answer. A fresh helper answers all 10 with today's CLAUDE.md. Must beat: 10 of 10. A miss is a fault in today's wording, reported to Sam, not fixed here.

**Then one change per pair, each its own numbered Y (all five in one message):** the pair becomes one sentence; the sentence check gets one allowance row (removed | kept, word for word | Sam's date), refused if the kept sentence is missing. Order: 1 (3 lines), 5 (code names), 4 (proposals) first; 2 and 3 last. Number each must beat: the 10-situation test, same answers as old; sentence check passes; no new sentence the old one lacked a meaning for.

**Enforced by:** the sentence check (already run by handover.py end) and a kittest per allowance row.
**Cost:** ~1.5-2.5% of a week once (a Sonnet chat for the test, an Opus medium chat for the merges; unchecked, from the ~1.7% a chat average in protest-tiers' ledger), saving ~0.04% a film; the test is reused by every later rewording.
**Sam would notice:** one message with 5 numbered Y/N; nothing else.

## Sam test
Q1: Merges only behind a behaviour test; says the saving is tiny.
Q2: Whole CLAUDE.md history (42 commits), not one chat.
Q3: Proof is the test's answers; enforced by the sentence check.
Q4: Four approaches; the root-cause tool is separate.
Q5: Each pair undone alone by its row and commit.
Q6: Sources named; estimates marked unchecked.
Q7: Real guard, not a hand edit; honest cost.
Q8: Permanent; reviewed at film end.

## Lost / Added
Lost: ~300 characters of repeated words; no case.
Added: a 10-situation test; an allowance table in the sentence check.

## Unchecked
Build cost; why 51846b42 was needed (title only); whether the 10 situations can all be found with Sam's right answer recorded.
