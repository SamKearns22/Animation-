# Proposal: Every notes round goes on the dearest model, even rounds of text, timing and sound

Status: adopted (2026-11-22)

## Problem
CLAUDE.md "Models by stage" puts every round of Sam's notes on Opus at medium effort. On Milburn, chat 18 ran on
Sonnet (the cheaper model) and took 9 notes on animatic 3 (text, timing, sound, a retreat move) with no repeats. If
rounds that only change words, timing or sound can go to Sonnet without more repeats, films cost less with no loss.
Milburn review lesson 8; Sam said Y to looking at it (19 Nov).

## Facts
- CLAUDE.md, "Models and chats": "A round of my notes (deciding, fixing, clips) and building from a clear plan or
  sound: Opus, medium effort. Routine work ... Sonnet."
- notes/archive/milburn.md line 14 (chat 18, Sonnet): 9 notes on animatic 3: five text changes, scene 3 sound removed,
  the goth's retreat move in the ambush, Milburn's name card moved, Hook Text tilted; ambush clip sent.
- The review (lesson 8) says "13 text, timing and sound notes at 2.3% with no repeats"; the ledger
  (notes/ledger/milburn.md, recalibrated 19 Nov to a week of 366 USD) shows chat 18 at 1.27%. The two figures
  differ (unchecked why: the review may predate the recalibration).
- Milburn ledger rows: Opus notes chats 9 (2.5%), 10 (2.17%), 11 (1.82%); chat 13 is listed as Sonnet at 1.5%
  in the ledger but notes/archive/milburn.md line 10 says "chat 13, Opus medium" (the record disagrees; unchecked).
- Notes and repeats columns in the ledger read 0 for every chat (not recorded; lesson 5, dropped by Sam as queued
  elsewhere), so repeat rates per model must be counted from the notes file by hand.
- Rule 30 / CLAUDE.md: a repeated note is a warning.

## Record
CLAUDE.md
notes/archive/milburn.md
notes/archive/milburn-handovers.md
notes/ledger/milburn.md
notes/ledger/blessed.md
notes/proposals/milburn-review.md
notes/proposals/chat-size-and-model.md
notes/proposals/model-switch.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 8b7b1530e4377cc2 -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = chat, V3 = helper B. Picked: V1 (helper A). Critiqued: 5 found, 3 fixed, 2 named.

## Leak
yes: the title and Problem name the answer ("rounds that only change words, timing or sound can go to Sonnet"), and the Facts quote the review's "no repeats". V2 copies that answer; V1 and V3 set it aside. The Facts also misplace a figure: the ledger page shows chat 18 at 1.9% (old week); 1.27% is the app's 4.654 USD at the 366 USD week (notes/ledger/app-costs.tsv line 88).
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 2 | 2 | 2 | 2 | 4 | 12 |
| V3 | 3 | 3 | 3 | 3 | 4 | 16 |
## Sam test
Q1: Yes, with the fix below: an expert keeps judgement (what Sam means, why the check missed it) on the strong model, hands out only written work, and measures before moving it.
Q2: Evidence is every notes round of Milburn and Blessed (Blessed has 10+ Opus round chats in notes/ledger/blessed.md), plus Protest Tiers if it has rounds; one film alone (V2) is too thin.
Q3: Root cause named (the rule picks a model per stage, a round mixes judgement and carrying-out; nothing counts repeats per model). The change, if made, is refused in code by the handover check, not left to reading. Measured at the end-of-film review.
Q4: Four approaches weighed (by kind of note, by step, learn first, fewer notes reaching Sam); the last is named as its own, bigger route.
Q5: The learning changes nothing. The later change is one yes, removable alone. Risk named: an extra hand-off per round can cost more than it saves.
Q6: Checked: app-costs.tsv (chat 13 Sonnet, 5.508 USD; chat 18 Sonnet, 4.654 USD); the review's own hand count (33 notes, 4 repeats, one of them the name card across Sonnet chats 13 and 18) contradicts its "no repeats". Unchecked: the review's 2.3%, chat 18's steps.
Q7: Sized by repeats, not by price: the saving is about 1% a film and one extra repeat (1.3-2.5% a round) wipes it out, so no change unless the record shows no more repeats.
Q8: Nothing trialled: the rule changes properly on Sam's yes after the count, or stays; reviewed when the film is called done.
## Pick
V1
## Why
V2 bakes in the problem's guess from one film where the "no repeats" claim is false on the record (the name card returned after Sonnet's chat 13 judged it clear by eye), and lets the chat sort notes with no measure. V3 learns first and checks its facts best (chat 13 really ran on Sonnet, per the app), but it puts the sorting, the hardest judgement call, on Sonnet, which is exactly where chat 13 failed, and it bundles a rule change, a model check at the chat's start and automatic note counting into one yes. V1 keeps every judgement on Opus and moves only written-out work, extending a seam CLAUDE.md already has ("an Opus fix ends by opening the Sonnet chat"). Taken from V3: chat 13 as Sonnet (the app's record), Blessed as the second film, the honest note that Sonnet already did look notes. Taken from the review: its hand count of notes and repeats, so the learning starts there and does not count twice.
## Faults in the pick
- F1 [fixed] V1's gate (b), "Sonnet's carried-out fixes repeat no more than Opus's", cannot be measured from the record: no Sonnet chat has ever carried out an Opus-written plan. Replaced by gates the record can measure.
- F2 [fixed] V1 builds its own served-model check; that is the open model-switch proposal's job. Dropped here; this route uses that check once built, so one yes is one change.
- F3 [fixed] The learning counted from scratch; it now starts from the review's hand count and reuses the lesson-5 counting if that has been built.
- F4 [named] An extra chat per round re-reads the film's notes and code; at about 1% saved a film, the hand-off can cost more than it saves. The gate measures it.
- F5 [named] V1's Opus "repeats" (goth's hair, the reverse) were not all checked against the chat that fixed them.
## Final version
**Step 1, learn (changes nothing; one Sonnet chat, about 1% of a week).** For every notes round in Milburn and Blessed (and Protest Tiers if it has rounds), from the chats' own records and the app's model record: notes taken, each note's kind (text, timing, sound, look, pose, staging, build), whether Sam gave it again and which chat's fix failed, cost, and the share of each Opus round spent on carrying-out steps (edits, renders, clips, finishing, sending) against deciding steps. Start from the Milburn review's count (33 notes, 4 repeats); correct its "no repeats" line. Result goes to Sam as one plain table.

**Step 2, only if both hold:** (a) carrying-out is over half of an Opus round's cost, even after paying for one extra chat's reading; (b) on the measured rounds, notes whose fix needed no judgement (written words, timing, sound) never came back. Then one yes: a notes round splits at a written plan. Opus medium reads every note, decides the fix exactly and its phone-size look, and ends. Sonnet carries out only what is written; anything not written goes back to Opus, never guessed. The handover check refuses a Sonnet notes round with no Opus plan, using the served-model check from the model-switch route.

**Numbers to beat** (end-of-film review): repeats per note no higher than the Opus-only rate measured in step 1; cost per note at least 25% below Milburn's Opus rounds. If either misses, the rule goes back.

If (a) or (b) fails: the rule stays as it is, and the effort goes to the bigger lever, fewer notes reaching Sam.
## For Sam
### Option 1: Count first, then let Opus decide and Sonnet carry out
One cheap chat counts, for every notes round of Milburn and Blessed, how many notes came back and what each round cost. Only if the numbers show it pays: the clever model decides every fix and writes it down, and the cheaper model does the renders, clips and sending. You'd notice nothing until the count; after it, a written plan line per note and slightly cheaper rounds.
Lost: nothing until the count; after it, Opus no longer does renders and clips in a notes round.
Added: one counting chat (about 1% of a week); a written plan per round; one extra hand-over per round.
### Option 2: Count first, then let Sonnet take each round and pass looks to Opus
The same count, then the cheaper model takes every round, fixes words, timing and sound itself, and sends notes on looks and poses to Opus. Cheaper, but the cheaper model does the sorting, which is where Milburn's name card note slipped and came back.
Lost: Opus seeing every note; the rule that a notes round is on Opus.
Added: the same count; a second message from Opus when a round has look notes.
