# Helper A

## Leak
Yes: learn.md's notes printout and the old verdict's CLAUDE.md guards and 3.5k target. Set aside.

## Results
- Repo start-up is ~13.5k tokens a chat (~4% of a week a film). The ceiling for all three fixes is ~1.8% a film, from 5 chats of one film (learn.md).
- Protest Tiers: 33 chats, 53.56%, median chat 1.78% (notes/ledger/protest-tiers.json). A fault back from one lost rule costs about a chat, more than the CLAUDE.md saving (0.6% a film) earns in three films.
- Branches (git, today): 254. 27 have off-main-line work from the last 3 days.
  - 24 of the 27 hold only notes/ledger/ files (automatic saves).
  - 3 hold real work, unmerged: a slurp profile picture (15 Nov), a Blessed WIP (13 Nov, kept off on purpose) and the audit branch (12 Nov, touches CLAUDE.md).
  - Two saved copies of Sam's messages (5t3vj4eb, phxjozvs) are not on the main line.
- **Error in the problem file:** this copy is shallow (its main-line history starts 11 Nov 17:35). 99 of the 108 "~1,500-commit" branches were last changed before that, so "rewritten histories" is an artefact of the shallow copy.
- The branch rule (P11, commit aa46dafe, 8 Nov) came from one missed animatic; checked "by hand" (rulebook).
- Notes: the record has token totals, not which lines chats read or used. **Gap.**
- CLAUDE.md text that is not rules (My accounts, the finish.py command repeated from tiktok-design.md line 116, 3 "replaces/was" histories) comes to ~0.5k tokens (my count); beyond that means rewording rules.

## The real decision
How every chat starts from all current work and Sam's open notes, reading the least. The listing is long and unreliable for one reason, so reliability is the lever. Chat count and length are bigger, but other jobs.

## Root cause
1. setup.sh tells chats to detach onto the main line.
2. Detached, ledger.py and `handover.py log` push their automatic saves to `claude/chat-XXXX`; ledger.py lines 207-209 rely on "the next chat's branch scan" to merge them.
3. That scan is done by hand. Chats cut it short (`head -30/-40`, learn.md), and the shallow copy hides what is already merged.

Result: a long listing, with real items still stranded.

## Approaches weighed
1. Condense the wording of all three (the problem's frame): ~1.8% at most, with a rule-loss risk.
2. **Reframe:** a tool merges the bookkeeping, and a hook prints only real off-main-line work.
3. **Learn first:** measure what chats read and use before cutting.
4. Fewer or shorter chats: bigger, but out of scope.

Chosen: 3, then 2, then gated parts of 1.

## Proposal
**Learn (changes nothing; Sonnet, ~0.5-1% of a week):** on a full-history copy, a census of every branch (bookkeeping or real work). The notes lines the 5 sampled chats read and used. Every CLAUDE.md sentence tagged as rule, pointer, history or detail.

**Then one change at a time, each its own yes:**
1. **Branch step by the start hook:**
   - setup.sh fetches full history, merges branches that hold only notes/ledger/ files, and prints one line per branch with other unmerged work.
   - CLAUDE.md says "merge what the start note lists"; the rule is unchanged.
   - `handover.py end` refuses while a listed branch is neither merged nor named in the notes.
   - Beat: under 0.2k tokens a chat (2.0k now), and nothing stranded at film end (today: 3 items and 2 message copies).
2. **Notes printout**, only if the census shows at least 1.5k a chat read beyond "Where things stand" and the open notes. No note may be dropped.
3. **CLAUDE.md: move only the ~0.5k that is not rules**, with the every-rule-sentence check. No rule wording is touched.

Cost: ~3-4% of a week once; saves ~0.6-1.5% a film; pays back in 2-3 films.

Sam would notice: the stranded items surface once; up to three questions.

## Sam test
- Q1: Fixes why branches pile up; measures before cutting.
- Q2: All 254 branches counted; the notes gap is learned first.
- Q3: Root cause in the code; the hook runs every chat; `end` refuses.
- Q4: Four different approaches.
- Q5: Each undone alone; no rule wording changes.
- Q6: Sources named; the problem's error flagged.
- Q7: Sized by reliability, not just tokens.
- Q8: Permanent, reviewed at film end.

## Lost / Added
- Lost: the full branch listing, ~0.5k of non-rule text in CLAUDE.md (moved to archive).
- Added: a census chat, a short branch printout with automatic merges, an `end` refusal, and two gated changes.

## Unchecked
- The 108 branches hidden by the shallow copy.
- What the stranded message copies and the audit branch hold beyond the main line.
- Notes line usage.
- Exact token counts for the non-rule text in CLAUDE.md.
