# Helper B: start-up fixes

## Leak
The problem file carries remedies (the notes printout, the CLAUDE.md guards, the 3.5k target); I set them aside. I also opened `chat.md`; not built on.

## Results
- Repo start-up is ~13.5k tokens a chat, ~4% of a week a film: CLAUDE.md 5.5k, notes 3.6k, branches 2.0k (learn.md, 5 chats). 1k tokens a chat = ~0.3% a film (learn.md).
- Branches (git, today): 254 listed, 135 with a tip not on the main line. **24 of the 26 from the last 2 days hold only automatic ledger commits.** Two hold real work: a profile picture (today) and `blessed.py`.
- **Ledger rows are lost:** 7 of 9 checked chats' rows are missing from the main line (`git grep`). ledger.py (lines 207-209) pushes to the chat's own branch, "which the next chat's branch scan merges"; the scan by hand doesn't.
- The fault behind the branch rule: on 8 Nov a chat missed an unmerged branch and rebuilt work (elder-swindon.md line 283).
- Notes: Where things stand (3,362 characters) plus open notes (1,749) is ~2.2k tokens, so the saving is ~1.4k, not 2.5k. The pack already says to read only those (job-packs.md line 32).
- CLAUDE.md: dates (308 characters) and the accounts, photo search and TikTok parts (1,384) moved word for word save ~0.7k. Under 3.5k means rewording rules.

## The real decision
What must every chat be told at start, automatically and briefly, so it never builds on stale work or drops a note? Inside this job, the bigger lever is the ledger's branches.

## Root cause
- **Branches:** one ledger branch per chat plus old rewritten histories, and a rule done by hand to read them all. Ledger rows fall through.
- **Notes:** no tool prints the right slice.
- **CLAUDE.md:** histories and rare parts load every chat.

## Approaches weighed
1. One tool per item, as the problem frames it.
2. Reframe: stop the clutter at its source (ledger rows go to the main line), then the hook prints only real work.
3. Delete stale branches once: destructive, grows back.
4. Learn first: map each CLAUDE.md sentence to its source fault before any rewording.

Chosen: 2, 1 for notes, 4 for CLAUDE.md.

## Proposal
One yes each, in this order:
1. **Ledger rows reach the main line.** ledger.py pushes rows to the main line (fetch, merge, retry), and a one-off merge brings in the missing rows. Beat: 0 rows missing at film end (today 7 of 9); `ledger.py audit` checks.
2. **Branch printout by setup.sh**. It prints only branches whose files outside `notes/ledger/` differ from the main line and are newer, with age and files. CLAUDE.md: "merge every branch the start lists". Beat: under 0.2k tokens (from 2.0k), and zero real work missed: `handover.py end` re-scans with no filter and flags anything unmerged.
3. **Notes printout.** `handover.py start --film` prints Where things stand and the unticked notes; carried() still checks the whole file. Beat: notes under 2.5k a chat (from 3.6k), and no rise in repeat notes or dropped asks.
4. **CLAUDE.md.** Learn first (changes nothing): a Sonnet chat maps each sentence to its source fault and date. Then move word for word: dates into the rulebook's last table; accounts, photos and the TikTok command into their packs, each leaving a pointer. A check refuses if any old sentence is not found word for word. Beat: under 4.8k tokens, no sentence lost. Rewording is a later question, only where the map shows a duplicate.

**Saving:** ~1.2% a film. **Cost:** ~0.5-1% of a week per change (startup-reading.md); the learn step ~0.3% (estimate). Repays in ~two films. Small against 53.6% a film.

**Sam would notice:** nothing in the films; complete ledger totals; four questions.

## Sam test
- Q1: Removes the cause before filtering.
- Q2: The branch evidence covers all 254 branches; the notes figure is still 5 chats.
- Q3: Hooks and start/end checks run in every chat, not by choice.
- Q4: Four approaches weighed; the reframe was picked.
- Q5: Each change can be undone alone; no rule is reworded without the map.
- Q6: Sources named; the rest is under Unchecked.
- Q7: Sized by the result: the ledger loss is fixed, not only tokens.
- Q8: Every change is permanent and reviewed at film end.

## Lost / Added
- Lost: the full branch list at start; dates and rare sections in CLAUDE.md (kept in the rulebook and packs).
- Added: a main-line ledger push, a branch printout, a notes printout, a sentence check, and one mapping chat.

## Unchecked
- The savings are character counts divided by 2.35, not measured in chats.
- Open notes in a busy round.
- Whether the lost rows explain learn.md's "4 chats not yet read".
- The build costs.
